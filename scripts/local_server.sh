#!/bin/sh
# Start llama-server on a GGUF file and wait until it is ready. Usage: local_server.sh <file.gguf>
llama-server -m "$1" --port 8080 -ngl 99 -c 4096 --parallel 1 --log-disable > /dev/null 2>&1 &
pid=$!
until curl -sf http://127.0.0.1:8080/health > /dev/null; do
  kill -0 "$pid" 2>/dev/null || { echo "server failed"; exit 1; }
  sleep 2
done
echo "$pid"
