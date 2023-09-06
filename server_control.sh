#!/bin/bash

# Check the command-line argument
if [ "$1" = "start" ]; then
    if [ "$2" = "debug" ]; then
        # Start the UVicorn server in debug mode with logging to STDOUT
        uvicorn chat_app.app.main:app --host 0.0.0.0 --port 7777 --reload
    else
        # Start the UVicorn server in the background  Requests per second:    26.82 [#/sec] (mean)
        nohup uvicorn chat_app.app.main:app --host 0.0.0.0 --port 7777 > server.log 2>&1 &
        # Requests per second:    26.87 [#/sec] (mean)
        #nohup hypercorn chat_app.app.main:app -b 0.0.0.0:7777 > server.log 2>&1 &

        # Save the process ID to a file
        echo $! > server.pid
        echo "Server started in the background. PID: $(cat server.pid)"
    fi
elif [ "$1" = "stop" ]; then
    # Read the process ID from the file
    pid=$(cat server.pid)
    
    # Check if the process is running
    if ps -p $pid > /dev/null; then
        # If running, stop the process gracefully
        echo "Stopping server with PID $pid..."
        kill $pid
        
        # Remove the PID file
        rm server.pid
        echo "Server stopped."
    else
        echo "Server is not running."
    fi
else
    echo "Usage: $0 [start [debug]|stop]"
fi
