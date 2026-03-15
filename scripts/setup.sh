#!/usr/bin/env bash
# Quick setup script for Pixel Heart OS

set -e

echo "🚀 Pixel Heart OS Setup"
echo "========================"

# Check Bun
if ! command -v bun &> /dev/null; then
    echo "❌ Bun not found. Install from https://bun.sh"
    exit 1
fi
echo "✅ Bun $(bun --version)"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found"
    exit 1
fi
echo "✅ Python $(python3 --version)"

# Setup frontend
echo "📦 Installing frontend dependencies..."
cd frontend
bun install
cd ..

# Setup backend
echo "🐍 Setting up backend..."
cd backend
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt
cd ..

# Init database
echo "🗄️  Initializing database..."
cd backend
source .venv/bin/activate
python -m database.init
cd ..

# Copy env file if needed
if [ ! -f "backend/.env" ]; then
    cp backend/.env.example backend/.env
    echo "⚠️  Please edit backend/.env and add your ANTHROPIC_API_KEY"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit backend/.env and set ANTHROPIC_API_KEY"
echo "2. Run: make dev   (or start servers manually)"
echo "3. Open http://localhost:5173"
echo ""
echo "Happy developing! 🎮"
