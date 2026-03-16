.PHONY: help dev dev-backend dev-frontend test lint format build docker-build docker-run db-init sample-data

help:
	@echo "Available targets:"
	@echo "  help                 Show this help message"
	@echo "  dev                  Start both backend and frontend in parallel"
	@echo "  dev-backend          Start backend only (http://localhost:8000)"
	@echo "  dev-frontend         Start frontend only (http://localhost:5173)"
	@echo "  test                 Run backend and frontend tests"
	@echo "  lint                 Check for linting errors (backend and frontend)"
	@echo "  format               Auto-fix formatting issues (backend and frontend)"
	@echo "  build                Build frontend for production"
	@echo "  docker-build         Build Docker images"
	@echo "  docker-run           Start docker-compose"
	@echo "  db-init              Initialize SQLite database only"
	@echo "  sample-data          Generate sample heroine/NPCs/scenes"

dev:
	@echo "Starting backend and frontend..."
	@(cd backend && source .venv/bin/activate && uvicorn main:app --reload --port 8000) & \
	(cd frontend && bun run dev)

dev-backend:
	@echo "Starting backend on http://localhost:8000"
	@cd backend && source .venv/bin/activate && uvicorn main:app --reload --port 8000

dev-frontend:
	@echo "Starting frontend on http://localhost:5173"
	@cd frontend && bun run dev

test:
	@echo "Running backend tests..."
	@cd backend && source .venv/bin/activate && pytest tests/ -v --cov=. --cov-report=html
	@echo "Running frontend tests..."
	@cd frontend && bunx vitest run

lint:
	@echo "Checking backend lint..."
	@cd backend && bunx ruff check .
	@echo "Checking frontend lint..."
	@cd frontend && bunx eslint src/

format:
	@echo "Formatting backend..."
	@cd backend && bunx black . && bunx ruff check --fix .
	@echo "Formatting frontend..."
	@cd frontend && bunx eslint src/ --fix && bunx prettier --write src/

build:
	@echo "Building frontend for production..."
	@cd frontend && bun run build

docker-build:
	@echo "Building Docker images..."
	@docker-compose build

docker-run:
	@echo "Starting Docker containers..."
	@docker-compose up -d

db-init:
	@echo "Initializing SQLite database..."
	@cd backend && source .venv/bin/activate && python -m database.init

sample-data:
	@echo "Generating sample data..."
	@cd backend && source .venv/bin/activate && python -m sample_data.generate