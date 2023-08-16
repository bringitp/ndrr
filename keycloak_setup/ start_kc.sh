#!/bin/bash

# Start Keycloak in the background
docker-compose up -d

# Check the logs for the desired message
docker-compose logs -f keycloak | while read line; do
    if [[ $line == *"Added user 'admin' to realm 'master'"* ]]; then
        echo "OK"
        break
    fi
done
