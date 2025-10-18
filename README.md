# Benefits & Financial Wellness Advisor

An AI-powered Benefits and Financial Wellness Advisor for early-career talent, featuring secure authentication with Multi-Factor Authentication (MFA).

## 🚀 Project Overview

This application helps new employees:
- Choose optimal health, dental, vision, and other group benefits
- Learn foundational financial topics (budgeting, emergency savings, debt management)
- Access AI-powered recommendations tailored to personal goals
- Build financial literacy through interactive tools

## 🔐 Security Features

✅ **Auth0 Integration**
- Secure user authentication and session management
- Universal Login with customizable branding

✅ **Multi-Factor Authentication (MFA)**
- **Required for all users** - cannot be bypassed
- Supported methods: Authenticator apps, SMS, Email
- Automatic enrollment during signup
- Industry-standard security compliance

✅ **Account Management**
- Separate Login and Sign Up flows
- Existing account detection with helpful error messages
- Secure logout with proper session cleanup

## 🛠️ Tech Stack

- **Frontend:** React 19.1.1 + Vite 7.1.7
- **Authentication:** Auth0 with @auth0/auth0-react
- **Styling:** CSS3 with modern design patterns
- **Security:** MFA enforced via Auth0 security policies

## 📦 Installation & Setup

### Prerequisites
- Node.js 18+ and npm
- Auth0 account (already configured)

### Quick Start

1. **Clone and install dependencies:**
```bash
git clone <repository-url>
cd BullDawg-Hackers
npm install
```

2. **Start development server:**
```bash
npm run dev
```

3. **Open the application:**
```
http://localhost:5173
```

### Available Scripts

```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
npm run lint     # Run ESLint
```

## 🔧 Auth0 Configuration

The application is pre-configured with:
- **Domain:** `dev-4zwtflcwcdswqbd2.us.auth0.com`
- **Client ID:** `ImdLbfq0EBdJCnkDMLcTDzT3K5fX7t9m`
- **Application Type:** Single Page Application (SPA)
- **MFA Policy:** Always required

### Environment Variables (Production)
For production deployment, create a `.env` file:
```
VITE_AUTH0_DOMAIN=your-auth0-domain
VITE_AUTH0_CLIENT_ID=your-client-id
```

## 🎯 User Experience

### New User Flow:
1. Click **"Sign Up"** → Auth0 signup form
2. Enter email and password
3. **Immediately prompted to set up MFA** (required)
4. Choose MFA method (Authenticator app recommended)
5. Complete setup and login to application

### Returning User Flow:
1. Click **"Log In"** → Auth0 login form
2. Enter credentials
3. **Enter MFA code** (required every login)
4. Access application dashboard

### Error Handling:
- Duplicate account attempts show friendly error message
- Users redirected to appropriate login/signup flow
- Clear visual feedback for authentication states

## 📁 Project Structure

```
src/
├── components/
│   ├── LoginButton.jsx    # Login/Signup buttons with Auth0 integration
│   ├── LogoutButton.jsx   # Secure logout functionality
│   └── Profile.jsx        # User profile display
├── App.jsx                # Main application with auth flow
├── main.jsx               # Auth0Provider wrapper
├── App.css                # Component styling
└── index.css              # Global styles
```

## 🔒 Security Implementation

### Authentication Flow:
1. **Auth0 Universal Login** handles all authentication
2. **PKCE (Proof Key for Code Exchange)** for SPA security
3. **Refresh token rotation** for enhanced security
4. **OIDC compliant** token handling

### MFA Enforcement:
- Configured at Auth0 tenant level with "Always" policy
- Cannot be disabled or bypassed by users
- Multiple factor options available
- Automatic enrollment for new users

## 🚧 Development Status

### ✅ Completed Features:
- Auth0 authentication integration
- Multi-Factor Authentication (required)
- User registration and login flows
- Session management and logout
- Error handling and user feedback
- Responsive UI design

### 🔮 Planned Features:
- Benefits selection wizard
- Financial wellness dashboard
- Budget calculator and planning tools
- Emergency fund recommendations
- Debt management guidance
- AI-powered personalized advice

## 🤝 Contributing

This project is part of a larger development effort. When contributing:

1. Work on feature branches (main authentication is on `Auth0` branch)
2. Ensure new features don't break authentication flow
3. Follow existing code patterns and styling
4. Test authentication flows after changes

## 📄 License

Private project for BullDawg Hackers team.

## 🆘 Support

For issues related to:
- **Authentication:** Check Auth0 Dashboard logs
- **MFA Setup:** Users will be automatically prompted
- **Development:** Check console for detailed error messages

---

**Ready for team to build main application features on top of this secure authentication foundation!** 🎉
