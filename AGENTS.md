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