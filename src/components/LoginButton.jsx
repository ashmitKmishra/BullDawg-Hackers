import { useAuth0 } from "@auth0/auth0-react";
import React from "react";

const LoginButton = () => {
  const { loginWithRedirect } = useAuth0();

  const handleLogin = () => {
    loginWithRedirect({
      authorizationParams: {
        screen_hint: 'login',
        acr_values: 'http://schemas.openid.net/pape/policies/2007/06/multi-factor',
        scope: 'openid profile email',
      }
    });
  };

  const handleSignUp = () => {
    loginWithRedirect({
      authorizationParams: {
        screen_hint: 'signup',
        acr_values: 'http://schemas.openid.net/pape/policies/2007/06/multi-factor',
        scope: 'openid profile email',
      }
    });
  };

  return (
    <div className="auth-buttons">
      <button onClick={handleLogin} className="login-btn">Log In</button>
      <button onClick={handleSignUp} className="signup-btn">Sign Up</button>
    </div>
  );
};

export default LoginButton;
