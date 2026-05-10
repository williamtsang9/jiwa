#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SESSION_NAME="${SESSION_NAME:-jiwa-dev}"
HOST_NAME="${APP_HOST:-127.0.0.1}"
APP_PORT="${APP_PORT:-3000}"

cd "$ROOT_DIR"

if ! command -v tmux >/dev/null 2>&1; then
  echo "tmux is required for this script."
  exit 1
fi

if [ ! -d ".venv" ]; then
  python -m venv .venv
fi

source .venv/bin/activate
pip install -r requirements.txt

if [ ! -f ".env" ]; then
  cp .env.example .env
fi

mkdir -p logs
touch logs/falcon.log

if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
  tmux kill-session -t "$SESSION_NAME"
fi

tmux new-session -d -s "$SESSION_NAME" -n "dev"
tmux send-keys -t "$SESSION_NAME":0.0 "cd '$ROOT_DIR' && source .venv/bin/activate && APP_HOST=$HOST_NAME APP_PORT=$APP_PORT python app.py" C-m

tmux split-window -v -t "$SESSION_NAME":0.0
tmux send-keys -t "$SESSION_NAME":0.1 "cd '$ROOT_DIR' && tail -f logs/falcon.log" C-m

tmux split-window -h -t "$SESSION_NAME":0.1
tmux send-keys -t "$SESSION_NAME":0.2 "cd '$ROOT_DIR' && source .venv/bin/activate && while true; do pytest -q; sleep 3; done" C-m

tmux split-window -h -t "$SESSION_NAME":0.0
tmux send-keys -t "$SESSION_NAME":0.3 "cd '$ROOT_DIR' && while true; do curl -s http://$HOST_NAME:$APP_PORT/api/tasks; echo; sleep 2; done" C-m

tmux select-layout -t "$SESSION_NAME":0 tiled
tmux attach-session -t "$SESSION_NAME"
