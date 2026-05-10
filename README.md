# jiwa

Falcon + Jinja2 Kanban MVP with MySQL persistence.

## Features

- Backlog page to create and manage task ideas
- Board page with columns:
  - to be started
  - in progress
  - needs reviewing
  - merged
  - completed
- Promote backlog tasks to board
- Move tasks between columns
- Optional REST API for task CRUD

## Setup

1. Create and activate a virtual environment:
   - Windows PowerShell:
     - `python -m venv .venv`
     - `.venv\Scripts\Activate.ps1`
2. Install dependencies:
   - `pip install -r requirements.txt`
3. Configure environment:
   - Copy `.env.example` to `.env`
   - Set MySQL credentials and database name
4. Ensure MySQL database exists:
   - Example: `CREATE DATABASE kanban_mvp CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`

## Run locally (localhost:3000)

- `python app.py`
- Open [http://127.0.0.1:3000](http://127.0.0.1:3000)

## Dev launcher (multi-pane workflow)

### PowerShell / Windows Terminal

- `.\scripts\dev.ps1`
- This bootstraps `.venv`, installs dependencies, ensures `.env`, and opens panes for:
  - Falcon app (`localhost:3000`)
  - Falcon request log stream (`logs/falcon.log`)
  - Continuous pytest loop

### tmux (Linux/macOS/WSL)

- `chmod +x scripts/dev-tmux.sh`
- `./scripts/dev-tmux.sh`
- This creates a 4-pane tmux session with:
  - Falcon app on `localhost:3000`
  - `tail -f` on Falcon logs
  - Continuous pytest loop
  - API polling (`/api/tasks`)

## REST API (optional)

- `GET /api/tasks`
- `GET /api/tasks?status=backlog`
- `POST /api/tasks`
- `PATCH /api/tasks/{id}`
- `DELETE /api/tasks/{id}`
