import { useState, useEffect, useCallback } from 'react';

const MazeGame = ({ onBack, onComplete }) => {
  const [playerPos, setPlayerPos] = useState({ x: 0, y: 0 });
  const [visitedCells, setVisitedCells] = useState(new Set(['0-0']));
  const [currentEvent, setCurrentEvent] = useState(null);
  const [score, setScore] = useState(0);
  const [money, setMoney] = useState(50000); // Starting salary
  const [gameStatus, setGameStatus] = useState('playing'); // playing, won, lost
  const [age, setAge] = useState(22); // Starting age
  const [playerDecisions, setPlayerDecisions] = useState([]);

  // 10x10 Maze grid - 0: path, 1: wall, 2: decision point, 3: event, 4: goal
  const maze = [
    [0, 0, 2, 1, 0, 0, 3, 1, 0, 0],
    [1, 0, 1, 1, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 2, 1, 1, 1, 1, 0],
    [0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 0, 1, 2, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [0, 0, 2, 0, 0, 3, 0, 0, 0, 0],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 4],
  ];

  const events = {
    'market_crash': {
      title: 'Market Crash!',
      description: 'The stock market dropped 20%. Your investments took a hit.',
      effect: (money) => money * 0.8,
      icon: 'fa-chart-line-down',
      color: '#e74c3c',
      type: 'bad'
    },
    'job_promotion': {
      title: 'Job Promotion!',
      description: 'Great work! You got promoted with a 25% raise.',
      effect: (money) => money * 1.25,
      icon: 'fa-briefcase',
      color: '#27ae60',
      type: 'good'
    },
    'inheritance': {
      title: 'Inheritance',
      description: 'You received an unexpected inheritance of $20,000.',
      effect: (money) => money + 20000,
      icon: 'fa-gift',
      color: '#f39c12',
      type: 'good'
    },
    'medical_emergency': {
      title: 'Medical Emergency',
      description: 'Unexpected medical bills cost you $15,000.',
      effect: (money) => money - 15000,
      icon: 'fa-heart-pulse',
      color: '#e74c3c',
      type: 'bad'
    },
    'side_hustle': {
      title: 'Side Hustle Success!',
      description: 'Your side business earned you an extra $10,000.',
      effect: (money) => money + 10000,
      icon: 'fa-rocket',
      color: '#3498db',
      type: 'good'
    },
    'car_repair': {
      title: 'Car Repair',
      description: 'Your car broke down. Repairs cost $3,000.',
      effect: (money) => money - 3000,
      icon: 'fa-car-burst',
      color: '#e67e22',
      type: 'bad'
    }
  };

  const decisions = [
    {
      id: 'invest_risky',
      title: 'Investment Opportunity',
      question: 'A friend offers you a "guaranteed" investment opportunity. What do you do?',
      choices: [
        { 
          text: 'Invest 30% of your savings',
          effect: (money) => Math.random() > 0.5 ? money * 1.5 : money * 0.7,
          feedback: 'High risk, high reward - or high loss!',
          risk: 'high',
          ageImpact: 2
        },
        { 
          text: 'Invest 10% in diversified index funds',
          effect: (money) => money * 1.12,
          feedback: 'Smart! Diversification reduces risk.',
          risk: 'medium',
          ageImpact: 3
        },
        { 
          text: 'Keep it in savings account',
          effect: (money) => money * 1.02,
          feedback: 'Safe, but inflation might eat your gains.',
          risk: 'low',
          ageImpact: 1
        }
      ]
    },
    {
      id: 'emergency_fund',
      title: 'Emergency Fund Decision',
      question: 'You have $5,000. Where should it go?',
      choices: [
        { 
          text: 'New gaming setup',
          effect: (money) => money - 5000,
          feedback: 'Fun now, but no safety net for emergencies.',
          risk: 'high',
          ageImpact: 1
        },
        { 
          text: 'Emergency fund (3 months expenses)',
          effect: (money) => money,
          feedback: 'Perfect! You\'re prepared for the unexpected.',
          risk: 'low',
          ageImpact: 4
        },
        { 
          text: 'Half emergency fund, half investments',
          effect: (money) => money * 1.05,
          feedback: 'Good balance of safety and growth.',
          risk: 'medium',
          ageImpact: 3
        }
      ]
    },
    {
      id: 'retirement',
      title: 'Retirement Planning',
      question: 'Your employer offers 401(k) matching. What do you do?',
      choices: [
        { 
          text: 'Ignore it, retirement is far away',
          effect: (money) => money,
          feedback: 'You\'re leaving free money on the table!',
          risk: 'high',
          ageImpact: 1
        },
        { 
          text: 'Contribute to get full match',
          effect: (money) => money * 1.15,
          feedback: 'Excellent! Never leave free money behind.',
          risk: 'low',
          ageImpact: 5
        },
        { 
          text: 'Max out contributions',
          effect: (money) => money * 1.20,
          feedback: 'Amazing! Your future self will thank you.',
          risk: 'low',
          ageImpact: 6
        }
      ]
    },
    {
      id: 'debt_payoff',
      title: 'Credit Card Debt',
      question: 'You have $10,000 in credit card debt at 18% APR. What\'s your strategy?',
      choices: [
        { 
          text: 'Pay minimum, invest the rest',
          effect: (money) => money * 0.85,
          feedback: 'Bad idea. Interest costs more than investment gains.',
          risk: 'high',
          ageImpact: 1
        },
        { 
          text: 'Aggressive payoff, pause investing',
          effect: (money) => money * 1.10,
          feedback: 'Smart! High-interest debt is an emergency.',
          risk: 'low',
          ageImpact: 4
        },
        { 
          text: 'Balance transfer to 0% card, pay aggressively',
          effect: (money) => money * 1.15,
          feedback: 'Brilliant strategy! Save on interest.',
          risk: 'low',
          ageImpact: 5
        }
      ]
    },
    {
      id: 'housing',
      title: 'Housing Decision',
      question: 'Time to think about housing. What\'s your move?',
      choices: [
        { 
          text: 'Buy a house you can barely afford',
          effect: (money) => money * 0.75,
          feedback: 'House poor! Too much income tied to housing.',
          risk: 'high',
          ageImpact: 2
        },
        { 
          text: 'Rent and invest the difference',
          effect: (money) => money * 1.08,
          feedback: 'Good if you invest wisely. Flexibility has value.',
          risk: 'medium',
          ageImpact: 3
        },
        { 
          text: 'Buy within 28% of gross income rule',
          effect: (money) => money * 1.12,
          feedback: 'Perfect! Building equity without overextending.',
          risk: 'low',
          ageImpact: 5
        }
      ]
    }
  ];

  const getRandomEvent = () => {
    const eventKeys = Object.keys(events);
    const randomKey = eventKeys[Math.floor(Math.random() * eventKeys.length)];
    return { ...events[randomKey], id: randomKey };
  };

  const getRandomDecision = () => {
    const randomDecision = decisions[Math.floor(Math.random() * decisions.length)];
    return randomDecision;
  };

  const handleKeyPress = useCallback((e) => {
    if (currentEvent || gameStatus !== 'playing') return;

    let newX = playerPos.x;
    let newY = playerPos.y;

    switch(e.key) {
      case 'ArrowUp':
        newY = Math.max(0, playerPos.y - 1);
        break;
      case 'ArrowDown':
        newY = Math.min(9, playerPos.y + 1);
        break;
      case 'ArrowLeft':
        newX = Math.max(0, playerPos.x - 1);
        break;
      case 'ArrowRight':
        newX = Math.min(9, playerPos.x + 1);
        break;
      case ' ':
        e.preventDefault();
        const cellType = maze[playerPos.y][playerPos.x];
        if (cellType === 2) {
          setCurrentEvent({ type: 'decision', data: getRandomDecision() });
        } else if (cellType === 3) {
          const event = getRandomEvent();
          setCurrentEvent({ type: 'event', data: event });
        }
        return;
      default:
        return;
    }

    // Check if new position is valid (not a wall)
    if (maze[newY][newX] !== 1) {
      setPlayerPos({ x: newX, y: newY });
      setVisitedCells(prev => new Set([...prev, `${newX}-${newY}`]));

      // Check for goal
      if (maze[newY][newX] === 4) {
        setGameStatus('won');
        onComplete(score + money);
      }

      // Trigger events automatically
      if (maze[newY][newX] === 3 && !visitedCells.has(`${newX}-${newY}`)) {
        const event = getRandomEvent();
        setCurrentEvent({ type: 'event', data: event });
      }
    }
  }, [playerPos, currentEvent, gameStatus, maze, visitedCells, score, money, onComplete]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [handleKeyPress]);

  const handleDecisionChoice = (choice) => {
    const newMoney = Math.round(choice.effect(money));
    setMoney(newMoney);
    setAge(age + choice.ageImpact);
    setScore(score + (choice.ageImpact * 100));
    setPlayerDecisions(prev => [...prev, {
      decision: currentEvent.data.question,
      choice: choice.text,
      feedback: choice.feedback
    }]);
    setCurrentEvent(null);

    if (newMoney <= 0) {
      setGameStatus('lost');
    }
  };

  const handleEventAcknowledge = () => {
    const newMoney = Math.round(currentEvent.data.effect(money));
    setMoney(newMoney);
    setCurrentEvent(null);

    if (newMoney <= 0) {
      setGameStatus('lost');
    }
  };

  const getCellClass = (x, y) => {
    const cellType = maze[y][x];
    const isVisited = visitedCells.has(`${x}-${y}`);
    
    if (cellType === 1) return 'maze-wall';
    if (cellType === 4) return 'maze-goal';
    if (cellType === 2) return isVisited ? 'maze-decision visited' : 'maze-decision';
    if (cellType === 3) return isVisited ? 'maze-event visited' : 'maze-event';
    return isVisited ? 'maze-path visited' : 'maze-path';
  };

  return (
    <div className="maze-container">
      <div className="maze-header">
        <button className="back-button" onClick={onBack}>← Back</button>
        <h2>Financial Maze Navigator</h2>
        <p className="maze-subtitle">Navigate to retirement while making smart financial decisions!</p>
      </div>

      <div className="maze-stats">
        <div className="stat-box">
          <i className="fa-solid fa-sack-dollar"></i>
          <div>
            <span className="stat-label">Net Worth</span>
            <span className="stat-value">${money.toLocaleString()}</span>
          </div>
        </div>
        <div className="stat-box">
          <i className="fa-solid fa-calendar-days"></i>
          <div>
            <span className="stat-label">Age</span>
            <span className="stat-value">{age} years</span>
          </div>
        </div>
        <div className="stat-box">
          <i className="fa-solid fa-star"></i>
          <div>
            <span className="stat-label">Score</span>
            <span className="stat-value">{score}</span>
          </div>
        </div>
      </div>

      <div className="maze-game-area">
        <div className="maze-grid">
          {maze.map((row, y) => (
            <div key={y} className="maze-row">
              {row.map((cell, x) => (
                <div
                  key={`${x}-${y}`}
                  className={`maze-cell ${getCellClass(x, y)} ${
                    playerPos.x === x && playerPos.y === y ? 'has-player' : ''
                  }`}
                >
                  {playerPos.x === x && playerPos.y === y && (
                    <div className="player-character">
                      <i className="fa-solid fa-person-walking"></i>
                    </div>
                  )}
                  {cell === 4 && (
                    <div className="goal-icon">
                      <i className="fa-solid fa-flag-checkered"></i>
                    </div>
                  )}
                  {cell === 2 && !visitedCells.has(`${x}-${y}`) && (
                    <div className="decision-icon">
                      <i className="fa-solid fa-path"></i>
                    </div>
                  )}
                  {cell === 3 && !visitedCells.has(`${x}-${y}`) && (
                    <div className="event-icon">
                      <i className="fa-solid fa-burst"></i>
                    </div>
                  )}
                </div>
              ))}
            </div>
          ))}
        </div>

        <div className="maze-controls">
          <p><i className="fa-solid fa-keyboard"></i> Use Arrow Keys to move</p>
          <p><i className="fa-solid fa-hand-pointer"></i> Press Space at decision points</p>
        </div>
      </div>

      {currentEvent && currentEvent.type === 'event' && (
        <div className="modal-overlay">
          <div className={`event-modal ${currentEvent.data.type}`}>
            <div className="event-icon-large">
              <i className={`fa-solid ${currentEvent.data.icon}`} style={{ color: currentEvent.data.color }}></i>
            </div>
            <h3>{currentEvent.data.title}</h3>
            <p>{currentEvent.data.description}</p>
            <button className="btn btn-primary" onClick={handleEventAcknowledge}>
              Continue <i className="fa-solid fa-arrow-right"></i>
            </button>
          </div>
        </div>
      )}

      {currentEvent && currentEvent.type === 'decision' && (
        <div className="modal-overlay">
          <div className="decision-modal">
            <h3>{currentEvent.data.title}</h3>
            <p className="decision-question">{currentEvent.data.question}</p>
            <div className="decision-choices">
              {currentEvent.data.choices.map((choice, index) => (
                <button
                  key={index}
                  className={`choice-btn risk-${choice.risk}`}
                  onClick={() => handleDecisionChoice(choice)}
                >
                  <span className="choice-text">{choice.text}</span>
                  <span className={`risk-badge ${choice.risk}`}>
                    {choice.risk === 'high' ? '⚡ High Risk' : 
                     choice.risk === 'medium' ? '⚖️ Medium Risk' : 
                     '🛡️ Low Risk'}
                  </span>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {gameStatus === 'won' && (
        <div className="modal-overlay">
          <div className="game-over-modal victory">
            <div className="victory-animation">
              <i className="fa-solid fa-trophy"></i>
            </div>
            <h2>Congratulations! You Reached Retirement!</h2>
            <div className="final-stats">
              <p><strong>Final Net Worth:</strong> ${money.toLocaleString()}</p>
              <p><strong>Retirement Age:</strong> {age} years</p>
              <p><strong>Financial Score:</strong> {score + money}</p>
            </div>
            <button className="btn btn-success" onClick={onBack}>
              Back to Home <i className="fa-solid fa-house"></i>
            </button>
          </div>
        </div>
      )}

      {gameStatus === 'lost' && (
        <div className="modal-overlay">
          <div className="game-over-modal defeat">
            <div className="defeat-animation">
              <i className="fa-solid fa-circle-xmark"></i>
            </div>
            <h2>Game Over - Bankruptcy!</h2>
            <p>Your net worth dropped to zero. Better financial decisions next time!</p>
            <button className="btn btn-primary" onClick={onBack}>
              Try Again <i className="fa-solid fa-rotate-right"></i>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default MazeGame;
