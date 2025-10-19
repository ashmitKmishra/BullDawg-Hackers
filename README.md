# CoverageCraft 🛡️

> AI-Powered Insurance & Benefits Recommendation Platform

A fully animated, production-ready web application that analyzes user data and insurance documents to provide personalized coverage recommendations using AWS Bedrock and Claude AI.

## ✨ Features

### 🎨 Beautiful UI/UX
- Smooth page transitions with Framer Motion
- Animated progress tracking throughout user journey
- Interactive cards with hover effects
- Gradient designs and modern glassmorphism
- Fully responsive (mobile, tablet, desktop)

### 📊 Smart Questionnaire
- 5-step comprehensive data collection
- Real-time progress bar (0-100%)
- Back/forward navigation
- Multiple input types (text, number, select, textarea)
- Collects 10+ data points for AI analysis

### 🤖 AI-Powered Dashboard
- Coverage summary with key metrics
- Prioritized recommendations
- Coverage gap analysis
- Animated cost breakdown charts
- Wellness tips and action items

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

## 🛠️ Tech Stack

- **Frontend**: React 19 + Vite
- **Animations**: Framer Motion
- **Routing**: React Router v6
- **Styling**: Custom CSS with CSS Variables
- **AI Backend** (planned): AWS Bedrock + Claude
- **Auth** (planned): Auth0

## 📁 Project Structure

```
src/
├── pages/
│   ├── Welcome.jsx       # Landing page
│   ├── Signup.jsx        # Account creation
│   ├── Questionnaire.jsx # 5-step form
│   ├── Dashboard.jsx     # AI insights
│   └── pages.css         # Shared styles
├── App.jsx               # Router setup
└── main.jsx              # Entry point
```

## 🎯 User Flow

1. **Welcome Page** → Animated landing with feature showcase
2. **Signup** → Quick account creation (20% progress)
3. **Questionnaire** → 5 steps collecting user data (20-100% progress)
4. **Dashboard** → AI-generated recommendations and insights

## 🎨 Design System

- **Primary Color**: Indigo (`#4f46e5`)
- **Accent Color**: Emerald (`#6ee7b7`)
- **Dark Theme**: Gradient background with translucent cards
- **Typography**: Inter font family
- **Animations**: Smooth 0.2-0.6s transitions

## 📝 Data Points Collected

1. Personal info (name, age, gender)
2. Family status (marital, dependents)
3. Employment (job type, income, PTO)
4. Financial health (savings, spending)
5. Health conditions
6. Lifestyle activity level
7. Vision care needs
8. Dental care needs

## 🔮 Roadmap

- [ ] AWS Bedrock integration
- [ ] PDF insurance document parsing
- [ ] Auth0 authentication
- [ ] Real-time AI recommendations
- [ ] Export reports as PDF
- [ ] Email notifications
- [ ] Mobile app

## 📄 License

MIT

---

Built with ❤️ by BullDawg Hackers
