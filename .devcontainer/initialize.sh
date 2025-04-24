#!/bin/bash
# Initialize environment for DemoMaker

echo "🔧 Setting up DemoMaker development environment..."

# Install development dependencies
echo "📦 Installing development dependencies..."
pip install --no-cache-dir -r requirements-dev.txt

# Create .env file from sample if it doesn't exist
if [ ! -f .env ]; then
    echo "🔑 Creating .env file from sample.env template..."
    cp sample.env .env
    echo "✅ Created .env file. Don't forget to customize it with your API keys!"
else
    echo "ℹ️ Found existing .env file. Using existing configuration."
fi

echo "🚀 DemoMaker environment setup complete!"
