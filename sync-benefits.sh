#!/bin/bash

# Quick setup and sync script for Backend+HR branch

echo "======================================"
echo "BullDawg Hackers - Backend+HR Setup"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "LincHack" ]; then
    echo "❌ Virtual environment 'LincHack' not found!"
    echo "Please create it first: python3 -m venv LincHack"
    exit 1
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source LincHack/bin/activate

# Install Python dependencies
echo "✓ Installing Python dependencies..."
cd backend
pip install -q -r requirements.txt

echo ""
echo "======================================"
echo "Ready to sync PDF data to Supabase"
echo "======================================"
echo ""
echo "Make sure you have:"
echo "  1. Uploaded a PDF via the backend (python main.py)"
echo "  2. A JSON file in backend/categorized_data/"
echo ""
read -p "Press ENTER to continue with sync..."

# Run sync script
python sync_to_supabase.py

cd ..

echo ""
echo "======================================"
echo "Sync Complete!"
echo "======================================"
echo ""
echo "Next steps:"
echo "  1. Start the API server: npm run server"
echo "  2. Start the frontend: npm run dev"
echo "  3. View benefits in the HR dashboard"
echo ""
