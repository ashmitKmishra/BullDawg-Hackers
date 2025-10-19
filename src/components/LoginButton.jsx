import { useAuth0 } from "@auth0/auth0-react";
import React from "react";

const LoginButton = () => {
  const { loginWithRedirect } = useAuth0();

  const handleLogin = () => {
    loginWithRedirect({
      authorizationParams: {
        screen_hint: 'login',
        prompt: 'login',
        acr_values: 'http://schemas.openid.net/pape/policies/2007/06/multi-factor',
        scope: 'openid profile email offline_access'
      },
      appState: { returnTo: '/questionnaire' }
    });
  };

  const handleSignUp = () => {
    loginWithRedirect({
      authorizationParams: {
        screen_hint: 'signup',
        prompt: 'login',
        acr_values: 'http://schemas.openid.net/pape/policies/2007/06/multi-factor',
        scope: 'openid profile email offline_access'
      },
      appState: { returnTo: '/questionnaire' }
    });
  };

  return (
    <div className="auth-buttons" style={{ display: 'flex', gap: '0.75rem' }}>
      <button onClick={handleLogin} className="login-btn">Log In</button>
      <button onClick={handleSignUp} className="signup-btn">Sign Up</button>
    </div>
  );
};

export default LoginButton;
