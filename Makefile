.PHONY: help dev build test lint clean docker-build docker-run

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Development
dev: ## Start development servers (frontend + backend)
	@echo "Starting development servers..."
	@echo "Backend will start on http://localhost:8000"
	@echo "Frontend will start on http://localhost:5173"
	@make -j2 dev-backend dev-frontend

dev-backend: ## Start backend server only
	cd backend && bun run dev

dev-frontend: ## Start frontend dev server only
	cd frontend && bun run dev

# Build
build: ## Build frontend and prepare backend
	@echo "Building frontend..."
	cd frontend && bun run build
	@echo "Backend is interpreted Python - no build step needed"

# Testing
test: ## Run all tests
test-backend:
	cd backend && bunx pytest tests/ -v --cov=.
test-frontend:
	cd frontend && bunx vitest run

test-watch:
	cd backend && bunx pytest tests/ -v --cov=. --watch

# Linting
lint: lint-backend lint-frontend
lint-backend:
	cd backend && bunx ruff check .
	cd backend && bunx black --check .
lint-frontend:
	cd frontend && bunx eslint src/
	cd frontend && bunx svelte-check

format: format-backend format-frontend
format-backend:
	cd backend && bunx black .
	cd backend && bunx ruff check --fix .
format-frontend:
	cd frontend && bunx eslint src/ --fix
	cd frontend && bunx prettier --write src/

# Docker
docker-build: ## Build Docker images
	docker build -t pixel-heart-backend -f backend/Dockerfile .
	docker build -t pixel-heart-frontend -f frontend/Dockerfile .

docker-run: ## Run with docker-compose
	docker-compose up -d

docker-stop:
	docker-compose down

# Cleanup
clean: ## Clean build artifacts
	rm -rf frontend/dist/
	rm -rf backend/.pytest_cache/
	rm -rf backend/htmlcov/
	rm -rf .coverage

# Database
db-init: ## Initialize SQLite database
	cd backend && bunx python -c "from database.init import init_db; init_db()"

db-reset: db-init ## Reset database (drops and recreates)
	rm -f backend/*.db

# Utility
create-migration:
	cd backend && bunx alembic revision --autogenerate -m "$(msg)"

# Data generation
sample-data: ## Generate sample heroine and universe for testing
	cd backend && bunx python scripts/generate_sample_data.py
