#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-status}"
COMPOSE_FILE="${COMPOSE_FILE:-./server/jellyfin/docker-compose.yml}"
CONTAINER_NAME="${JELLYFIN_CONTAINER_NAME:-jellyfin}"
SYSTEMD_UNIT="${JELLYFIN_SYSTEMD_UNIT:-jellyfin}"

has_cmd() {
  command -v "$1" >/dev/null 2>&1
}

compose_up() {
  if has_cmd docker && docker compose version >/dev/null 2>&1; then
    docker compose -f "$COMPOSE_FILE" up -d 2>/dev/null
    return 0
  fi
  return 1
}

compose_down() {
  if has_cmd docker && docker compose version >/dev/null 2>&1; then
    docker compose -f "$COMPOSE_FILE" down 2>/dev/null
    return 0
  fi
  return 1
}

compose_status() {
  if has_cmd docker && docker compose version >/dev/null 2>&1; then
    docker compose -f "$COMPOSE_FILE" ps 2>/dev/null
    return 0
  fi
  return 1
}

container_start() {
  if has_cmd docker; then
    docker start "$CONTAINER_NAME" >/dev/null 2>&1
    return 0
  fi
  return 1
}

container_stop() {
  if has_cmd docker; then
    docker stop "$CONTAINER_NAME" >/dev/null 2>&1
    return 0
  fi
  return 1
}

container_status() {
  if has_cmd docker; then
    docker ps --filter "name=${CONTAINER_NAME}" --format "table {{.Names}}\t{{.Status}}" 2>/dev/null
    return 0
  fi
  return 1
}

systemd_start() {
  if has_cmd systemctl; then
    sudo systemctl start "$SYSTEMD_UNIT"
    return 0
  fi
  return 1
}

systemd_stop() {
  if has_cmd systemctl; then
    sudo systemctl stop "$SYSTEMD_UNIT"
    return 0
  fi
  return 1
}

systemd_status() {
  if has_cmd systemctl; then
    systemctl --no-pager --full status "$SYSTEMD_UNIT"
    return 0
  fi
  return 1
}

start_jellyfin() {
  if [[ -f "$COMPOSE_FILE" ]] && compose_up; then
    echo "Jellyfin started via docker compose ($COMPOSE_FILE)"
    return 0
  fi
  if container_start; then
    echo "Jellyfin container started: $CONTAINER_NAME"
    return 0
  fi
  if systemd_start; then
    echo "Jellyfin systemd unit started: $SYSTEMD_UNIT"
    return 0
  fi
  echo "Unable to start Jellyfin. Install Docker or systemd unit '$SYSTEMD_UNIT'." >&2
  return 1
}

stop_jellyfin() {
  if [[ -f "$COMPOSE_FILE" ]] && compose_down; then
    echo "Jellyfin stopped via docker compose ($COMPOSE_FILE)"
    return 0
  fi
  if container_stop; then
    echo "Jellyfin container stopped: $CONTAINER_NAME"
    return 0
  fi
  if systemd_stop; then
    echo "Jellyfin systemd unit stopped: $SYSTEMD_UNIT"
    return 0
  fi
  echo "Unable to stop Jellyfin. No supported runtime found." >&2
  return 1
}

status_jellyfin() {
  if [[ -f "$COMPOSE_FILE" ]] && compose_status; then
    return 0
  fi
  if container_status; then
    return 0
  fi
  if systemd_status; then
    return 0
  fi
  echo "Unable to determine Jellyfin status. No supported runtime found." >&2
  return 1
}

case "$ACTION" in
  start)
    start_jellyfin
    ;;
  stop)
    stop_jellyfin
    ;;
  status)
    status_jellyfin
    ;;
  *)
    echo "Usage: $0 {start|stop|status}" >&2
    exit 1
    ;;
esac
