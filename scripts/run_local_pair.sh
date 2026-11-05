#!/bin/sh
# Base vs instruction-tuned Nemo on this machine, one model at a time. Free, about 45 minutes on an
# M1 Pro. A dummy key is set because the local server needs none and .env must not be sent to it.
set -e
export OPENROUTER_API_KEY=local
pid=$(scripts/local_server.sh data/external/gguf/Mistral-Nemo-Base-2407.Q4_K_M.gguf | tail -1)
uv run memsyco run --config config/local_nemo.yaml --run-id local-base-20261105 | tail -3
kill "$pid"; sleep 5
pid=$(scripts/local_server.sh data/external/gguf/Mistral-Nemo-Instruct-2407-Q4_K_M.gguf | tail -1)
uv run memsyco run --config config/local_nemo_instruct.yaml --run-id local-instruct-20261105 | tail -3
kill "$pid"
