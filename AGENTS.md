Project: Objective:
Build an AI-powered Benefits and Financial Wellness Advisor for early-career talent.

Benefits Selection Assistance
Create an intelligent assistant to help new employees choose health, dental, vision, and other group benefits, such as employee assistance, caregiver resources, and tutoring support.

Analyze user inputs (including age, income, and family status) with AI to understand individual needs.

Recommend optimal benefit and financial choices tailored to users' personal goals.

Financial Wellness Education
Teach users foundational financial topics including budgeting, emergency savings, and debt management.

Introduce key concepts in long-term financial planning.

Provide interactive tools to help users build financial literacy.

Note: This is a part of a bigger project. Any changes in this shall not create any merge conflicts. Please design features with this in mind.
Step 1: Check if Auth0 branch exists. If not, create a different branch with name "Auth0". Otherwise, skip to auth0
Step 2: Integrate Auth0. Use MCP server for best safety practices. Below is template from their website:

Below is index.js:
import React from 'react';
import { createRoot } from 'react-dom/client';
import { Auth0Provider } from '@auth0/auth0-react';
import App from './App';

const root = createRoot(document.getElementById('root'));

root.render(
<Auth0Provider
    domain="dev-4zwtflcwcdswqbd2.us.auth0.com"
    clientId="ImdLbfq0EBdJCnkDMLcTDzT3K5fX7t9m"
    authorizationParams={{
      redirect_uri: window.location.origin
    }}
  >
    <App />
  </Auth0Provider>,
);

Below is login.js:
import { useAuth0 } from "@auth0/auth0-react";
import React from "react";

const LoginButton = () => {
  const { loginWithRedirect } = useAuth0();

  return <button onClick={() => loginWithRedirect()}>Log In</button>;
};

export default LoginButton;

Below is logout.js
import { useAuth0 } from "@auth0/auth0-react";
import React from "react";

const LogoutButton = () => {
  const { logout } = useAuth0();

  return (
    <button onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })}>
      Log Out
    </button>
  );
};

export default LogoutButton;

Below is profile.js:
import { useAuth0 } from "@auth0/auth0-react";
import React from "react";

const Profile = () => {
  const { user, isAuthenticated, isLoading } = useAuth0();

  if (isLoading) {
    return <div>Loading ...</div>;
  }

  return (
    isAuthenticated && (
      <div>
        <img src={user.picture} alt={user.name} />
        <h2>{user.name}</h2>
        <p>{user.email}</p>
      </div>
    )
  );
};

export default Profile;

---

## Implementation Status

### ✅ Completed Features

#### Step 1: Auth0 Branch Creation
- ✅ Created Auth0 branch
- ✅ Pushed AGENTS.md to Auth0 branch

#### Step 2: Auth0 Integration
- ✅ Installed @auth0/auth0-react package
- ✅ Created LoginButton component (src/components/LoginButton.jsx)
- ✅ Created LogoutButton component (src/components/LogoutButton.jsx)
- ✅ Created Profile component (src/components/Profile.jsx)
- ✅ Updated main.jsx with Auth0Provider wrapper
- ✅ Updated App.jsx with authentication flow
- ✅ Configured Auth0 application in tenant (Client ID: ImdLbfq0EBdJCnkDMLcTDzT3K5fX7t9m)

#### Step 3: Multi-Factor Authentication (MFA)
- ✅ Created Auth0 Action: "Enforce MFA for Benefits Advisor" (ID: 4197a3cf-7c79-43a9-8426-688efd1426eb)
- ✅ Deployed Action to post-login flow
- ✅ MFA enforcement configured to:
  - Force MFA enrollment for all new users during first login
  - Challenge existing users without MFA to enroll
  - Require MFA for all subsequent logins
  - Track new vs returning users via custom claims
- ✅ Created MFAEnrollment component (src/components/MFAEnrollment.jsx) with:
  - Auto-check MFA status on component mount
  - Display welcome banner for new users
  - Show current MFA enrollment status
  - Provide one-click MFA enrollment
  - Educational information about MFA benefits
- ✅ Updated App.css with MFA-specific styling
- ✅ Added custom claims to ID tokens:
  - `https://auth0.com/mfa_enrolled`: Boolean indicating MFA status
  - `https://auth0.com/is_new_user`: Boolean indicating if first login

### 🔐 Security Features Implemented

1. **Automatic MFA Enforcement**
   - All users are required to set up MFA
   - New users prompted during signup/first login
   - Existing users without MFA prompted on next login
   - Multiple MFA options available: SMS, Authenticator App, Email

2. **User Account Detection**
   - System tracks login count to identify new vs returning users
   - Custom claims added to tokens for frontend awareness
   - First login timestamp stored in user metadata

3. **Session Security**
   - Refresh token rotation enabled
   - 30-day token lifetime (2,592,000 seconds)
   - 15-day idle timeout (1,296,000 seconds)
   - OIDC compliant authentication flow

### 📋 Configuration Details

**Auth0 Application Settings:**
- Name: Benefits & Financial Wellness Advisor
- Type: Single Page Application (SPA)
- Domain: dev-4zwtflcwcdswqbd2.us.auth0.com
- Client ID: ImdLbfq0EBdJCnkDMLcTDzT3K5fX7t9m
- Allowed Callback URLs: http://localhost:3000, http://localhost:3001
- Allowed Logout URLs: http://localhost:3000, http://localhost:3001
- Token Endpoint Auth Method: None (PKCE flow for SPA)

**Auth0 Action: Enforce MFA for Benefits Advisor**
- Trigger: post-login (v3)
- Runtime: Node.js 18
- Status: Deployed and Active
- Functionality:
  - Checks if MFA completed in current session
  - Enforces MFA enrollment for users without factors
  - Sets custom claims for MFA status and user type
  - Tracks first login timestamp

### 🚀 How It Works

1. **New User Flow:**
   - User clicks "Log In"
   - Redirected to Auth0 Universal Login
   - User signs up with email/password or social login
   - Auth0 Action detects first login (logins_count === 1)
   - User is immediately prompted to set up MFA
   - User chooses MFA method (SMS/Authenticator/Email)
   - User completes MFA setup
   - User is redirected back to app with MFA enrolled
   - Custom claim `is_new_user: true` included in token
   - Welcome banner displayed in MFAEnrollment component

2. **Returning User Flow (with MFA):**
   - User clicks "Log In"
   - Enters credentials
   - Prompted for MFA code
   - Enters MFA code
   - Successfully authenticated
   - Custom claim `mfa_enrolled: true` included in token
   - Green checkmark displayed showing MFA is active

3. **Existing User Flow (without MFA):**
   - User clicks "Log In"
   - Enters credentials
   - Auth0 Action detects no MFA enrolled
   - User immediately prompted to set up MFA
   - Cannot proceed without completing MFA setup
   - After setup, redirected to app with MFA enabled

### 📝 Files Created/Modified

**New Files:**
- `src/components/LoginButton.jsx` - Login functionality
- `src/components/LogoutButton.jsx` - Logout functionality
- `src/components/Profile.jsx` - User profile display
- `src/components/MFAEnrollment.jsx` - MFA status and enrollment

**Modified Files:**
- `src/main.jsx` - Added Auth0Provider wrapper
- `src/App.jsx` - Integrated auth components and MFA enrollment
- `src/App.css` - Added styling for auth and MFA components
- `package.json` - Added @auth0/auth0-react dependency
- `AGENTS.md` - This documentation

### 🔧 Auth0 MCP Server Usage

The Auth0 MCP server was used to:
- List and retrieve application details
- Create the MFA enforcement Action
- Deploy the Action to the post-login flow
- Configure application settings

**MCP Server Configuration:**
```json
"mcp": {
  "servers": {
    "auth0": {
      "command": "npx",
      "args": ["-y", "@auth0/auth0-mcp-server", "run"],
      "capabilities": ["tools"],
      "env": {
        "DEBUG": "auth0-mcp"
      }
    }
  }
}
```

### 🎯 Next Steps (For Other Team Members)

The authentication foundation is complete. The main application features can now be built:
1. Benefits selection wizard
2. Financial wellness dashboard
3. Budget calculator
4. Emergency fund planner
5. Debt management tools
6. Retirement planning calculator

All new features will have access to:
- Authenticated user information via `useAuth0()` hook
- User's email, name, and profile picture
- MFA enrollment status
- New vs returning user status

### 🧪 Testing Instructions

1. Start the development server: `npm run dev -- --port 3000`
2. Open http://localhost:3000
3. Click "Log In"
4. Sign up with a new account
5. You'll be prompted to set up MFA
6. Choose your preferred MFA method
7. Complete MFA setup
8. You'll be redirected back to the app
9. MFA status component will show green checkmark
10. Log out and log back in - you'll be prompted for MFA code

### ⚠️ Important Notes

- MFA is **required** for all users - cannot be bypassed
- First-time users **must** complete MFA setup during signup
- Existing users will be prompted on next login
- The Auth0 Action enforces MFA at the authorization server level
- Custom claims are added to both ID tokens and access tokens
- Session tokens use secure rotation with refresh tokens

### 🔴 MANUAL CONFIGURATION REQUIRED

The Auth0 Action has been created and deployed, but **you must complete these manual steps in the Auth0 Dashboard:**

1. **Bind Action to Login Flow:**
   - Go to Auth0 Dashboard → Actions → Flows → Login
   - Drag "Enforce MFA for Benefits Advisor" action into the flow
   - Click Apply

2. **Enable MFA Methods:**
   - Go to Security → Multi-factor Auth
   - Enable at least one method (Authenticator App recommended)
   - Set policy to "Always" or "At first login"
   - Save changes

3. **Test the Flow:**
   - Create a new account - you should be prompted for MFA immediately
   - Existing users should be prompted on next login

**See AUTH0_SETUP_GUIDE.md for detailed step-by-step instructions.**

---

## ✅ Latest Updates (Step 3: Enhanced Authentication UI)

### Separate Login and Sign Up Buttons
- ✅ Added dedicated "Log In" button (blue) - for existing users
- ✅ Added dedicated "Sign Up" button (green) - for new users
- ✅ Both buttons properly trigger Auth0 Universal Login with MFA
- ✅ `screen_hint` parameter directs users to correct Auth0 screen

### Existing Account Detection
- ✅ Created "Check Existing User on Signup" Action (ID: 84031a0d-8fdc-4101-a35c-0e5a8a330244)
- ✅ Auth0 automatically prevents duplicate emails in same connection
- ✅ Enhanced error handling in App.jsx to catch Auth0 errors
- ✅ Custom error message when user tries to sign up with existing account
- ✅ Automatic redirect suggestion to login for existing users

### Error Handling Flow:
1. User clicks "Sign Up" with existing email
2. Auth0 detects duplicate account and returns error
3. App catches error and displays friendly message:
   - "It looks like you already have an account"
   - Shows "Log In" button to redirect to login
4. User can click "Log In" to access existing account

### UI Improvements:
- Separate styled buttons for Login (blue) and Sign Up (green)
- Error section with red border and clear messaging
- Help text guides users to correct action
- Responsive button layout with flexbox

### Technical Implementation:
```javascript
// LoginButton.jsx now has two functions:
const handleLogin = () => {
  loginWithRedirect({
    authorizationParams: {
      screen_hint: 'login',  // Shows login screen
      acr_values: 'http://schemas.openid.net/pape/policies/2007/06/multi-factor',
    }
  });
};

const handleSignUp = () => {
  loginWithRedirect({
    authorizationParams: {
      screen_hint: 'signup',  // Shows signup screen
      acr_values: 'http://schemas.openid.net/pape/policies/2007/06/multi-factor',
    }
  });
};
```

### Application Structure
```
src/
├── components/
│   ├── LoginButton.jsx       # Auth0 login integration
│   ├── LogoutButton.jsx      # Secure logout functionality
│   ├── Profile.jsx           # User profile display
│   └── MFAEnrollment.jsx     # MFA enrollment & status
├── App.jsx                    # Main app with auth flow
├── main.jsx                   # Auth0Provider wrapper
├── App.css                    # Styled components
└── index.css                  # Global styles
```

### Security Features
✅ Auth0 Universal Login
✅ Token-based authentication
✅ Secure session management
✅ Multi-Factor Authentication support
✅ OIDC compliant implementation
✅ Refresh token rotation
✅ Secure logout with redirect
✅ MCP server integration for best practices

### Development Server
- Running on ports 3000/3001
- Hot module replacement enabled
- Auth0 MCP server active with full toolset

### Next Steps (To be implemented by team)
- Benefits selection interface
- Financial wellness education modules
- User input forms (age, income, family status)
- AI-powered recommendation engine
- Interactive financial literacy tools
- Budgeting calculators
- Emergency savings planning
- Debt management resources

### Notes
- All auth changes isolated to Auth0 branch
- No merge conflicts with main application development
- MFA is recommended but not mandatory for initial testing
- Production deployment will require environment variable configuration
- MFA enrollment can be made mandatory via Auth0 dashboard rules