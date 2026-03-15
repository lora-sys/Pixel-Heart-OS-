#!/usr/bin/env bash
# Install dependencies - works with both Bun and npm

echo "📦 Installing frontend dependencies..."

cd frontend

# Try Bun first
if command -v bun &> /dev/null; then
    echo "Using Bun..."
    bun install
else
    echo "Bun not found, using npm..."
    npm install
fi

cd ..

echo ""
echo "✅ Dependencies installed!"
echo ""
echo "⚠️  Note: Phantom dependencies may need to be added:"
echo "   - @sveltejs/adapter-auto (should be auto-detected by SvelteKit)"
echo "   - All dependencies should be listed in package.json"
