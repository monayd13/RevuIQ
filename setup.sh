#!/bin/bash

echo "🚀 RevuIQ Setup Script"
echo "======================="
echo ""

# Check Python version
echo "📌 Checking Python version..."
python3 --version || { echo "❌ Python 3 not found. Please install Python 3.8+"; exit 1; }

# Check Node.js version
echo "📌 Checking Node.js version..."
node --version || { echo "❌ Node.js not found. Please install Node.js 18+"; exit 1; }

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt || { echo "❌ Failed to install Python dependencies"; exit 1; }
echo "✅ Python dependencies installed"

# Install frontend dependencies
echo ""
echo "📦 Installing frontend dependencies..."
cd frontend
npm install || { echo "❌ Failed to install frontend dependencies"; exit 1; }
cd ..
echo "✅ Frontend dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created. Please add your API keys!"
    echo "⚠️  Edit .env and add your GOOGLE_PLACES_API_KEY"
else
    echo ""
    echo "✅ .env file already exists"
fi

# Create logs directory
mkdir -p logs
echo "✅ Logs directory created"

# Initialize database
echo ""
echo "📊 Initializing database..."
python3 -c "from backend.database import init_db; init_db()" || { echo "❌ Failed to initialize database"; exit 1; }
echo "✅ Database initialized"

# Make scripts executable
chmod +x start_all.sh stop_all.sh check_status.sh
echo "✅ Scripts made executable"

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your GOOGLE_PLACES_API_KEY"
echo "2. Run: ./start_all.sh"
echo "3. Open: http://localhost:3000"
echo ""
echo "Happy coding! 🚀"
