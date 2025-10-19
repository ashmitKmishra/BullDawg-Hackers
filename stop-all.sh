#!/bin/bash

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Stopping all services...${NC}"

# Read PIDs from file if it exists
if [ -f "logs/pids.txt" ]; then
    while read pid; do
        if ps -p $pid > /dev/null 2>&1; then
            echo -e "${YELLOW}Stopping process $pid...${NC}"
            kill $pid 2>/dev/null
            sleep 1
            # Force kill if still running
            if ps -p $pid > /dev/null 2>&1; then
                kill -9 $pid 2>/dev/null
            fi
            echo -e "${GREEN}✓ Process $pid stopped${NC}"
        fi
    done < logs/pids.txt
    rm logs/pids.txt
else
    echo -e "${YELLOW}No PID file found, stopping by port...${NC}"
    
    # Stop by port
    echo -e "${YELLOW}Stopping services on ports 3001, 5173, 8000...${NC}"
    
    # Kill process on port 3001 (Express)
    lsof -ti:3001 | xargs kill -9 2>/dev/null
    
    # Kill process on port 5173 (React)
    lsof -ti:5173 | xargs kill -9 2>/dev/null
    
    # Kill process on port 8000 (Python)
    lsof -ti:8000 | xargs kill -9 2>/dev/null
fi

echo -e "${GREEN}All services stopped!${NC}"
