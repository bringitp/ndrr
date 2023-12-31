#!/bin/bash

# Function to stop UVicorn server by PID
stop_uvicorn() {
    local pid=$1
    if ps -p $pid > /dev/null; then
        echo "Stopping server with PID $pid..."
        kill $pid
        echo "Server with PID $pid stopped."
    fi
}

# Function to stop all UVicorn servers
stop_all_uvicorn() {
    local uvicorn_pids=$(pgrep -f "uvicorn chat_app.app.main:app --host 0.0.0.0 --port")
    for pid in $uvicorn_pids; do
        stop_uvicorn $pid
    done
}

# Check the command-line argument
if [ "$1" = "start" ]; then
    if [ "$2" = "debug" ]; then
        # Start the UVicorn server in debug mode with logging to STDOUT
        uvicorn chat_app.app.main:app --host 0.0.0.0 --port 7777 --reload
    else
        # Get the number of CPU cores
        core_count=5

        # Start UVicorn servers in the background with incremental port numbers
        for ((i=0; i<core_count; i++)); do
            port=$((7777 + i))
            nohup uvicorn chat_app.app.main:app --host 0.0.0.0 --port $port > server_$port.log 2>&1 &
            echo $! > server_$port.pid
            echo "Server started in the background. PID: $(cat server_$port.pid), Port: $port"
        done
    fi
elif [ "$1" = "stop" ]; then
    if [ "$2" = "all" ]; then
        # Stop all UVicorn processes gracefully
        stop_all_uvicorn
    else
        # Stop specific servers by PID
        shift
        for pid in "$@"; do
            stop_uvicorn $pid
        done
    fi
else
    echo "Usage: $0 [start [debug]|stop [all|PID1 PID2 ...]]"
fi

