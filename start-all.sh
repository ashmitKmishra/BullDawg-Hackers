#!/bin/bash

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}HR Manager - Unified System${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command_exists node; then
    echo -e "${RED}❌ Node.js is not installed${NC}"
    exit 1
fi

if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Node.js found: $(node --version)${NC}"
echo -e "${GREEN}✓ Python found: $(python3 --version)${NC}"
echo ""

# Check environment files
echo -e "${YELLOW}Checking environment configuration...${NC}"

if [ ! -f ".env" ]; then
    echo -e "${RED}❌ Root .env file not found${NC}"
    echo -e "${YELLOW}Please create .env with Supabase credentials${NC}"
    exit 1
fi

if [ ! -f "backend/.env" ]; then
    echo -e "${RED}❌ backend/.env file not found${NC}"
    echo -e "${YELLOW}Please create backend/.env with GEMINI_API_KEY${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Environment files found${NC}"
echo ""

# Create log directory
mkdir -p logs

# Start Express API
echo -e "${BLUE}Starting Express API (port 3001)...${NC}"
node server.js > logs/express.log 2>&1 &
EXPRESS_PID=$!
echo -e "${GREEN}✓ Express API started (PID: $EXPRESS_PID)${NC}"

# Wait a moment
sleep 2

# Start Python Backend
echo -e "${BLUE}Starting Python Backend (port 8000)...${NC}"
cd backend
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt > ../logs/pip-install.log 2>&1
else
    source venv/bin/activate
fi
python main.py > ../logs/python.log 2>&1 &
PYTHON_PID=$!
cd ..
echo -e "${GREEN}✓ Python Backend started (PID: $PYTHON_PID)${NC}"

# Wait a moment
sleep 2

# Start React Frontend
echo -e "${BLUE}Starting React Frontend (port 5173)...${NC}"
npm run dev > logs/react.log 2>&1 &
REACT_PID=$!
echo -e "${GREEN}✓ React Frontend started (PID: $REACT_PID)${NC}"

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}All services started successfully!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo -e "${BLUE}Services:${NC}"
echo -e "  React Frontend:  ${GREEN}http://localhost:5173${NC}"
echo -e "  Express API:     ${GREEN}http://localhost:3001${NC}"
echo -e "  Python Backend:  ${GREEN}http://localhost:8000${NC}"
echo ""
echo -e "${BLUE}Process IDs:${NC}"
echo -e "  Express: $EXPRESS_PID"
echo -e "  Python:  $PYTHON_PID"
echo -e "  React:   $REACT_PID"
echo ""
echo -e "${BLUE}Logs:${NC}"
echo -e "  Express: logs/express.log"
echo -e "  Python:  logs/python.log"
echo -e "  React:   logs/react.log"
echo ""
echo -e "${YELLOW}To view logs in real-time:${NC}"
echo -e "  tail -f logs/express.log"
echo -e "  tail -f logs/python.log"
echo -e "  tail -f logs/react.log"
echo ""
echo -e "${YELLOW}To stop all services:${NC}"
echo -e "  ./stop-all.sh"
echo -e "  or manually: kill $EXPRESS_PID $PYTHON_PID $REACT_PID"
echo ""

# Save PIDs to file for stop script
echo "$EXPRESS_PID" > logs/pids.txt
echo "$PYTHON_PID" >> logs/pids.txt
echo "$REACT_PID" >> logs/pids.txt

echo -e "${GREEN}Press Ctrl+C to stop watching logs, services will continue running${NC}"
echo -e "${BLUE}Watching combined logs...${NC}"
echo ""

# Follow logs
tail -f logs/*.log
