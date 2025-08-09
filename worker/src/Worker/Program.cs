using System;
using System.Data.Common;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using Newtonsoft.Json;
using Npgsql;
using StackExchange.Redis;

namespace Worker
{
    public class Program
    {
        public static int Main(string[] args)
        {
            try
            {
                var pgsql = OpenDbConnection("Server=db;Username=postgres;Password=postgres;");
                var redis = OpenRedisConnection("redis").GetDatabase();

                var definition = new { vote = "", voter_id = "" };
                while (true)
                {
                    string json = redis.ListRightPopAsync("votes").Result;
                    if (json != null)
                    {
                        var vote = JsonConvert.DeserializeAnonymousType(json, definition);
                        Console.WriteLine($"Processing vote for '{vote.vote}' by '{vote.voter_id}'");
                        UpdateVote(pgsql, vote.voter_id, vote.vote);
                    }
                }
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine(ex.ToString());
                return 1;
            }
        }

        private static NpgsqlConnection OpenDbConnection(string connectionString)
        {
            NpgsqlConnection connection;

            while (true)
            {
                try
                {
                    connection = new NpgsqlConnection(connectionString);
                    connection.Open();
                    break;
                }
                catch (SocketException)
                {
                    Console.Error.WriteLine("Waiting for db");
                    Thread.Sleep(1000);
                }
                catch (DbException)
                {
                    Console.Error.WriteLine("Waiting for db");
                    Thread.Sleep(1000);
                }
            }

            Console.Error.WriteLine("Connected to db");

            var command = connection.CreateCommand();
            command.CommandText = @"CREATE TABLE IF NOT EXISTS votes (
                                        id SERIAL PRIMARY KEY,
                                        vote VARCHAR(255) NOT NULL,
                                        voter_id VARCHAR(255),
                                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                    )";
            command.ExecuteNonQuery();

            return connection;
        }

        private static ConnectionMultiplexer OpenRedisConnection(string hostname)
        {
            // Use IP address to workaround hhttps://github.com/StackExchange/StackExchange.Redis/issues/410
            var ipAddress = GetIp(hostname);
            Console.WriteLine($"Found redis at {ipAddress}");

            while (true)
            {
                try
                {
                    Console.Error.WriteLine("Connected to redis");
                    return ConnectionMultiplexer.Connect(ipAddress);
                }
                catch (RedisConnectionException)
                {
                    Console.Error.WriteLine("Waiting for redis");
                    Thread.Sleep(1000);
                }
            }
        }

        private static string GetIp(string hostname)
            => Dns.GetHostEntryAsync(hostname)
                .Result
                .AddressList
                .First(a => a.AddressFamily == AddressFamily.InterNetwork)
                .ToString();

        private static void UpdateVote(NpgsqlConnection connection, string voterId, string vote)
        {
            var command = connection.CreateCommand();
            try
            {
                // Use UPSERT logic: INSERT or UPDATE if voter already exists
                command.CommandText = @"
                    INSERT INTO votes (vote, voter_id, timestamp, created_at) 
                    VALUES (@vote, @voter_id, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                    ON CONFLICT (voter_id) 
                    DO UPDATE SET 
                        vote = EXCLUDED.vote, 
                        timestamp = CURRENT_TIMESTAMP";
                command.Parameters.AddWithValue("@vote", vote);
                command.Parameters.AddWithValue("@voter_id", voterId);
                command.ExecuteNonQuery();
                Console.WriteLine($"Successfully upserted vote: {vote} from {voterId}");
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine($"Error inserting vote: {ex.Message}");
            }
            finally
            {
                command.Dispose();
            }
        }
    }
}