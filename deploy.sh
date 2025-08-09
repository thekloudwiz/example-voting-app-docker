#!/bin/bash

# Modern Voting App Deployment Script
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check if Docker daemon is running
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker daemon is not running. Please start Docker first."
        exit 1
    fi
    
    print_success "All prerequisites are met!"
}

# Function to clean up old containers
cleanup() {
    print_status "Cleaning up old containers..."
    
    # Stop and remove containers if they exist
    docker-compose down --remove-orphans 2>/dev/null || true
    
    # Remove old images (optional)
    if [ "$1" = "--clean-images" ]; then
        print_status "Removing old images..."
        docker image prune -f
    fi
    
    print_success "Cleanup completed!"
}

# Function to build and start services
deploy() {
    print_status "Building and starting modern voting app..."
    
    # Build and start services
    docker-compose up -d --build
    
    if [ $? -eq 0 ]; then
        print_success "Services started successfully!"
    else
        print_error "Failed to start services!"
        exit 1
    fi
}

# Function to wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    # Wait for vote app
    print_status "Checking vote app..."
    for i in {1..30}; do
        if curl -s http://localhost:5000/api/health >/dev/null 2>&1; then
            print_success "Vote app is ready!"
            break
        fi
        if [ $i -eq 30 ]; then
            print_warning "Vote app health check timeout"
        fi
        sleep 2
    done
    
    # Wait for result app
    print_status "Checking result app..."
    for i in {1..30}; do
        if curl -s http://localhost:5001/api/health >/dev/null 2>&1; then
            print_success "Result app is ready!"
            break
        fi
        if [ $i -eq 30 ]; then
            print_warning "Result app health check timeout"
        fi
        sleep 2
    done
}

# Function to show service status
show_status() {
    print_status "Service Status:"
    echo ""
    docker-compose ps
    echo ""
    
    print_status "Service URLs:"
    echo "🗳️  Vote App:           http://localhost:5000"
    echo "📊 Results App:        http://localhost:5001"
    echo "🔍 Redis Insight:      http://localhost:8001 (with --monitoring)"
    echo "🐘 pgAdmin:            http://localhost:8080 (with --monitoring)"
    echo ""
}

# Function to run tests
run_tests() {
    print_status "Running comprehensive tests..."
    
    if command_exists python3; then
        python3 test-modern-app.py
    elif command_exists python; then
        python test-modern-app.py
    else
        print_warning "Python not found. Skipping automated tests."
        print_status "You can manually test the applications using the URLs above."
    fi
}

# Function to show logs
show_logs() {
    print_status "Showing service logs..."
    docker-compose logs -f
}

# Function to stop services
stop_services() {
    print_status "Stopping services..."
    docker-compose down
    print_success "Services stopped!"
}

# Function to show help
show_help() {
    echo "Modern Voting App Deployment Script"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  start           Start the modern voting app (default)"
    echo "  stop            Stop all services"
    echo "  restart         Restart all services"
    echo "  status          Show service status"
    echo "  logs            Show service logs"
    echo "  test            Run comprehensive tests"
    echo "  clean           Clean up containers and images"
    echo "  help            Show this help message"
    echo ""
    echo "Options:"
    echo "  --monitoring    Include monitoring services (Redis Insight, pgAdmin)"
    echo "  --clean-images  Remove old Docker images during cleanup"
    echo "  --no-test       Skip running tests after deployment"
    echo ""
    echo "Examples:"
    echo "  $0                          # Start with default settings"
    echo "  $0 start --monitoring       # Start with monitoring services"
    echo "  $0 restart --clean-images   # Restart and clean old images"
    echo "  $0 test                     # Run tests only"
    echo ""
}

# Main script logic
main() {
    local command="${1:-start}"
    local monitoring=false
    local clean_images=false
    local run_test=true
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --monitoring)
                monitoring=true
                shift
                ;;
            --clean-images)
                clean_images=true
                shift
                ;;
            --no-test)
                run_test=false
                shift
                ;;
            start|stop|restart|status|logs|test|clean|help)
                command=$1
                shift
                ;;
            *)
                shift
                ;;
        esac
    done
    
    # Set Docker Compose profiles
    if [ "$monitoring" = true ]; then
        export COMPOSE_PROFILES="monitoring"
        print_status "Monitoring services enabled"
    fi
    
    case $command in
        start)
            echo "🚀 Starting Modern Voting App"
            echo "=============================="
            check_prerequisites
            cleanup $( [ "$clean_images" = true ] && echo "--clean-images" )
            deploy
            wait_for_services
            show_status
            if [ "$run_test" = true ]; then
                echo ""
                run_tests
            fi
            ;;
        stop)
            echo "🛑 Stopping Modern Voting App"
            echo "============================="
            stop_services
            ;;
        restart)
            echo "🔄 Restarting Modern Voting App"
            echo "==============================="
            check_prerequisites
            cleanup $( [ "$clean_images" = true ] && echo "--clean-images" )
            deploy
            wait_for_services
            show_status
            ;;
        status)
            show_status
            ;;
        logs)
            show_logs
            ;;
        test)
            run_tests
            ;;
        clean)
            cleanup $( [ "$clean_images" = true ] && echo "--clean-images" )
            ;;
        help)
            show_help
            ;;
        *)
            print_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
