FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build

WORKDIR /app
COPY src/ /app/src/

RUN dotnet restore src/Worker/Worker.csproj
RUN dotnet publish -c Release -o out src/Worker/Worker.csproj

FROM mcr.microsoft.com/dotnet/runtime:6.0
WORKDIR /app
COPY --from=build /app/out .

CMD ["dotnet", "Worker.dll"]