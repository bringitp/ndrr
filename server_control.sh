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

# Check the command-line argument
if [ "$1" = "start" ]; then
    if [ "$2" = "debug" ]; then
        # Start the UVicorn server in debug mode with logging to STDOUT
        uvicorn chat_app.app.main:app --host 0.0.0.0 --port 7777 --reload
    else
        # Get the number of CPU cores
        core_count=2

        # Start UVicorn servers in the background with incremental port numbers
        for ((i=0; i<core_count; i++)); do
            port=$((7777 + i))
            nohup uvicorn chat_app.app.main:app --host 0.0.0.0 --port $port > server_$port.log 2>&1 &
            echo $! > server_$port.pid
            echo "Server started in the background. PID: $(cat server_$port.pid), Port: $port"
        done
    fi
elif [ "$1" = "stop" ]; then
    # Stop all server processes gracefully
    if [ "$2" = "all" ]; then
        for pid_file in server_*.pid; do
            pid=$(cat "$pid_file")
            stop_uvicorn $pid
            rm "$pid_file"
        done
    else
        # Stop a specific server by PID
        for pid_file in "${@:2}"; do
            pid=$(cat "$pid_file")
            stop_uvicorn $pid
            rm "$pid_file"
        done
    fi
else
    echo "Usage: $0 [start [debug]|stop [all|PID1 PID2 ...]]"
fi

