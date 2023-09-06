#!/bin/bash

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
    for pid_file in server_*.pid; do
        pid=$(cat "$pid_file")
        if ps -p $pid > /dev/null; then
            echo "Stopping server with PID $pid..."
            kill $pid
            rm "$pid_file"
            echo "Server with PID $pid stopped."
        fi
    done
else
    echo "Usage: $0 [start [debug]|stop]"
fi
