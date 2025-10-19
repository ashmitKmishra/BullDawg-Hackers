import { useState, useEffect, useRef } from 'react';
import { GoogleGenerativeAI } from '@google/generative-ai';
import './AIChatbot.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001/api';

const AIChatbot = ({ onClose, onAction }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [employees, setEmployees] = useState([]);
  const [benefits, setBenefits] = useState([]);
  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);

  const genAI = new GoogleGenerativeAI('AIzaSyBfdRckjfyDIkl4s8NoWPI9eqdEpOsv6bo');

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Fetch initial data
    fetchEmployees();
    fetchBenefits();
    
    // Welcome message
    const welcomeMessage = {
      role: 'assistant',
      content: "Hello Sarah! 👋 I'm CoverCompass AI, your intelligent HR assistant. I'm here to help you manage your HR tasks efficiently. I can help you:\n\n• Add new employees to the system\n• Create and manage benefit policies\n• Enroll employees in benefits\n• Search for employee or policy information\n• View statistics and insights\n\nWhat would you like to do today?"
    };
    setMessages([welcomeMessage]);
  }, []);

  const fetchEmployees = async () => {
    try {
      const res = await fetch(`${API_URL}/employees`);
      const data = await res.json();
      setEmployees(data);
    } catch (error) {
      console.error('Error fetching employees:', error);
    }
  };

  const fetchBenefits = async () => {
    try {
      const res = await fetch(`${API_URL}/benefits`);
      const data = await res.json();
      setBenefits(data);
    } catch (error) {
      console.error('Error fetching benefits:', error);
    }
  };

  const extractActionFromResponse = async (userInput, aiResponse) => {
    const lowerInput = userInput.toLowerCase();
    const lowerResponse = aiResponse.toLowerCase();
    
    // Check for add employee with extracted data
    if (lowerInput.includes('add employee') || lowerInput.includes('new employee') || lowerInput.includes('create employee')) {
      // Try to extract employee data from the conversation
      const emailMatch = userInput.match(/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/);
      const nameMatch = userInput.match(/name is ([^,.\n]+)|called ([^,.\n]+)|named ([^,.\n]+)/i);
      const departmentMatch = userInput.match(/department:?\s*([^,.\n]+)|in (?:the )?([a-z]+) department/i);
      const positionMatch = userInput.match(/position:?\s*([^,.\n]+)|as (?:a |an )?([^,.\n]+)/i);
      
      if (emailMatch || nameMatch) {
        const employeeData = {
          name: nameMatch ? (nameMatch[1] || nameMatch[2] || nameMatch[3]).trim() : '',
          email: emailMatch ? emailMatch[0] : '',
          department: departmentMatch ? (departmentMatch[1] || departmentMatch[2]).trim() : '',
          position: positionMatch ? (positionMatch[1] || positionMatch[2]).trim() : ''
        };
        
        // If we have enough data, add the employee
        if (employeeData.name && employeeData.email) {
          try {
            const res = await fetch(`${API_URL}/employees`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(employeeData)
            });
            
            if (res.ok) {
              await fetchEmployees();
              return { 
                type: 'EMPLOYEE_ADDED', 
                data: employeeData,
                message: `✅ Successfully added ${employeeData.name} to the system!`
              };
            }
          } catch (error) {
            console.error('Error adding employee:', error);
          }
        }
      }
      
      return { type: 'ADD_EMPLOYEE' };
    }
    
    // Check for add benefit with extracted data
    if (lowerInput.includes('add benefit') || lowerInput.includes('new benefit') || lowerInput.includes('create benefit') || 
        lowerInput.includes('add policy') || lowerInput.includes('new policy') || lowerInput.includes('create policy')) {
      
      const nameMatch = userInput.match(/(?:benefit|policy) (?:called|named) ([^,.\n]+)|name:?\s*([^,.\n]+)/i);
      const costMatch = userInput.match(/\$?(\d+(?:\.\d{2})?)\s*(?:per month|\/month|monthly)?/);
      const descriptionMatch = userInput.match(/description:?\s*([^.\n]+)/i);
      
      if (nameMatch) {
        const benefitData = {
          name: (nameMatch[1] || nameMatch[2]).trim(),
          description: descriptionMatch ? descriptionMatch[1].trim() : '',
          cost: costMatch ? costMatch[1] : '0'
        };
        
        try {
          const res = await fetch(`${API_URL}/benefits`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(benefitData)
          });
          
          if (res.ok) {
            await fetchBenefits();
            return { 
              type: 'BENEFIT_ADDED', 
              data: benefitData,
              message: `✅ Successfully created the benefit "${benefitData.name}"!`
            };
          }
        } catch (error) {
          console.error('Error adding benefit:', error);
        }
      }
      
      return { type: 'ADD_BENEFIT' };
    }
    
    // Check for statistics/dashboard request
    if (lowerInput.includes('statistic') || lowerInput.includes('dashboard') || lowerInput.includes('overview') ||
        lowerInput.includes('how many') || lowerInput.includes('total')) {
      return { 
        type: 'SHOW_STATS',
        data: {
          totalEmployees: employees.length,
          totalBenefits: benefits.length
        }
      };
    }
    
    // Check for view employees
    if (lowerInput.includes('show employees') || lowerInput.includes('list employees') || lowerInput.includes('view employees')) {
      return { type: 'VIEW_EMPLOYEES', data: employees };
    }
    
    // Check for view benefits
    if (lowerInput.includes('show benefits') || lowerInput.includes('list benefits') || lowerInput.includes('view benefits') ||
        lowerInput.includes('show policies') || lowerInput.includes('list policies')) {
      return { type: 'VIEW_BENEFITS', data: benefits };
    }
    
    return null;
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    const currentInput = input;
    setInput('');
    setIsLoading(true);

    try {
      const model = genAI.getGenerativeModel({ model: 'gemini-2.0-flash-exp' });
      
      // Create context-aware prompt with current data
      const systemContext = `You are CoverCompass AI, an intelligent assistant for the CoverageCompass HR Benefits Management System. 
      You're helping Sarah Johnson, the HR Manager, manage employees and benefit policies.
      
      Current System Status:
      - Total Employees: ${employees.length}
      - Total Benefits/Policies: ${benefits.length}
      
      You can help with:
      1. Adding new employees - Ask for: name, email, department, and position
         Example: "I want to add John Doe, john.doe@lfg.com, IT department, as a Software Engineer"
      
      2. Creating benefit policies - Ask for: benefit name, description, and monthly cost
         Example: "Add a benefit called Health Insurance with description 'Comprehensive medical coverage' for $200 per month"
      
      3. Viewing statistics and information about employees and benefits
      
      4. Searching for specific employees or benefits
      
      Be professional, friendly, and concise. When the user wants to perform an action:
      - If they provide complete information, confirm what you understood
      - If information is missing, ask for the specific missing details
      - Guide them through the process step by step
      - Use emojis sparingly for a professional yet friendly tone
      
      Available employees: ${employees.map(e => e.name).join(', ') || 'None yet'}
      Available benefits: ${benefits.map(b => b.name).join(', ') || 'None yet'}
      
      Current conversation:`;
      
      const conversationHistory = messages.map(msg => 
        `${msg.role === 'user' ? 'User' : 'Assistant'}: ${msg.content}`
      ).join('\n');
      
      const fullPrompt = `${systemContext}\n${conversationHistory}\nUser: ${currentInput}\nAssistant:`;
      
      const result = await model.generateContent(fullPrompt);
      const response = await result.response;
      const text = response.text();
      
      const assistantMessage = { role: 'assistant', content: text };
      setMessages(prev => [...prev, assistantMessage]);
      
      // Check if we should trigger any actions
      const action = await extractActionFromResponse(currentInput, text);
      if (action) {
        if (action.message) {
          // Add success message
          const successMessage = { role: 'assistant', content: action.message };
          setMessages(prev => [...prev, successMessage]);
        }
        
        if (action.type === 'SHOW_STATS') {
          const statsMessage = { 
            role: 'assistant', 
            content: `📊 Here's your current dashboard:\n\n👥 Total Employees: ${action.data.totalEmployees}\n🏥 Total Benefits & Policies: ${action.data.totalBenefits}\n\nWould you like me to show you more details about any of these?`
          };
          setMessages(prev => [...prev, statsMessage]);
        } else if (action.type === 'VIEW_EMPLOYEES' && action.data) {
          const employeeList = action.data.map(e => 
            `• ${e.name} - ${e.email} (${e.department}${e.position ? ', ' + e.position : ''})`
          ).join('\n');
          const listMessage = { 
            role: 'assistant', 
            content: `👥 Here are all employees:\n\n${employeeList || 'No employees yet.'}`
          };
          setMessages(prev => [...prev, listMessage]);
        } else if (action.type === 'VIEW_BENEFITS' && action.data) {
          const benefitList = action.data.map(b => 
            `• ${b.name} - ${b.cost === 0 || b.cost === '0' ? 'Price varies' : '$' + b.cost + '/month'}`
          ).join('\n');
          const listMessage = { 
            role: 'assistant', 
            content: `🏥 Here are all benefits/policies:\n\n${benefitList || 'No benefits yet.'}`
          };
          setMessages(prev => [...prev, listMessage]);
        }
        // Removed automatic navigation to avoid tab switching
      }
      
    } catch (error) {
      console.error('Error calling Gemini API:', error);
      const errorMessage = { 
        role: 'assistant', 
        content: "I apologize, but I'm having trouble connecting right now. Please try again or use the manual controls in the navigation menu." 
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const quickActions = [
    { label: '➕ Add Employee', prompt: 'I want to add a new employee' },
    { label: '🏥 Add Benefit', prompt: 'I want to create a new benefit policy' },
    { label: '📊 Show Statistics', prompt: 'Show me the current statistics' },
    { label: '� List Employees', prompt: 'Show me all employees' }
  ];

  if (isMinimized) {
    return (
      <div className="chatbot-minimized" onClick={() => setIsMinimized(false)}>
        <div className="chatbot-minimized-content">
          <span className="chatbot-icon">🤖</span>
          <span className="chatbot-minimized-text">CoverCompass AI</span>
          {isLoading && <span className="chatbot-pulse"></span>}
        </div>
      </div>
    );
  }

  return (
    <div className="chatbot-container" ref={chatContainerRef}>
      <div className="chatbot-header">
        <div className="chatbot-header-left">
          <span className="chatbot-avatar">🤖</span>
          <div className="chatbot-header-text">
            <h3>CoverCompass AI</h3>
            <p className="chatbot-status">
              <span className="status-dot"></span>
              Online
            </p>
          </div>
        </div>
        <div className="chatbot-header-actions">
          <button 
            className="chatbot-minimize-btn" 
            onClick={() => setIsMinimized(true)}
            title="Minimize"
          >
            ─
          </button>
          <button 
            className="chatbot-close-btn" 
            onClick={onClose}
            title="Close"
          >
            ✕
          </button>
        </div>
      </div>

      <div className="chatbot-messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.role}`}>
            <div className="message-avatar">
              {message.role === 'assistant' ? '🤖' : '👤'}
            </div>
            <div className="message-content">
              <div className="message-text">{message.content}</div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message assistant">
            <div className="message-avatar">🤖</div>
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chatbot-quick-actions">
        {quickActions.map((action, index) => (
          <button
            key={index}
            className="quick-action-btn"
            onClick={() => {
              setInput(action.prompt);
            }}
          >
            {action.label}
          </button>
        ))}
      </div>

      <div className="chatbot-input-container">
        <textarea
          className="chatbot-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message... (Press Enter to send)"
          rows="2"
          disabled={isLoading}
        />
        <button 
          className="chatbot-send-btn" 
          onClick={handleSend}
          disabled={isLoading || !input.trim()}
        >
          {isLoading ? '⏳' : '➤'}
        </button>
      </div>
    </div>
  );
};

export default AIChatbot;
