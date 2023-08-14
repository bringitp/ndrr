#!/bin/bash

CONTAINER_NAME=keycloak

start_keycloak() {
  echo "Starting Keycloak..."
  docker run -d --name $CONTAINER_NAME -p 8180:8180 \
    -e KEYCLOAK_ADMIN=admin -e KEYCLOAK_ADMIN_PASSWORD=admin \
    quay.io/keycloak/keycloak:latest start-dev --http-port 8180 --http-relative-path /auth --proxy=reencrypt  # --proxy=reencrypt に変更


  echo "Keycloak is now running."
}

stop_keycloak() {
  echo "Stopping Keycloak..."
  docker stop $CONTAINER_NAME
  docker rm $CONTAINER_NAME
  echo "Keycloak has been stopped and removed."
}

case "$1" in
  start)
    start_keycloak
    ;;
  stop)
    stop_keycloak
    ;;
  restart)
    stop_keycloak
    start_keycloak
    ;;
  *)
    echo "Usage: $0 {start|stop|restart}"
    exit 1
esac

exit 0


