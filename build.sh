#!/bin/bash
set -e

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🚀 Training ML models..."
python setup.py

echo "✅ Build complete!"
