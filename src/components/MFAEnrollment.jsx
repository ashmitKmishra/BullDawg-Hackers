import { useAuth0 } from "@auth0/auth0-react";
import React, { useState, useEffect } from "react";

const MFAEnrollment = () => {
  const { user, getAccessTokenSilently, loginWithRedirect } = useAuth0();
  const [enrollmentStatus, setEnrollmentStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [isNewUser, setIsNewUser] = useState(false);

  useEffect(() => {
    // Automatically check MFA status when component mounts
    if (user) {
      checkMFAEnrollment();
    }
  }, [user]);

  const checkMFAEnrollment = async () => {
    setLoading(true);
    try {
      // Check if user has MFA enrolled from the custom claim
      const hasMFA = user?.["https://auth0.com/mfa_enrolled"] || false;
      const isNew = user?.["https://auth0.com/is_new_user"] || false;
      
      setIsNewUser(isNew);
      setEnrollmentStatus(hasMFA ? "enrolled" : "not_enrolled");
      
      console.log("MFA Status:", hasMFA ? "Enrolled" : "Not Enrolled");
      console.log("User Type:", isNew ? "New User" : "Returning User");
    } catch (error) {
      console.error("Error checking MFA enrollment:", error);
      setEnrollmentStatus("error");
    } finally {
      setLoading(false);
    }
  };

  const promptMFAEnrollment = () => {
    // Force re-login to trigger MFA enrollment
    loginWithRedirect({
      authorizationParams: {
        prompt: 'login',
        screen_hint: 'signup'
      }
    });
  };

  return (
    <div className="mfa-section">
      <h3>Multi-Factor Authentication</h3>
      <p>Secure your account with an additional layer of protection</p>
      
      {isNewUser && (
        <div className="welcome-banner">
          <strong>Welcome, new user!</strong> We recommend setting up MFA to secure your account.
        </div>
      )}
      
      {loading ? (
        <p>Checking MFA status...</p>
      ) : enrollmentStatus === "enrolled" ? (
        <div className="mfa-status enrolled">
          <span>✓</span> MFA is enabled on your account
          <p>Your account is protected with multi-factor authentication.</p>
        </div>
      ) : enrollmentStatus === "not_enrolled" ? (
        <div className="mfa-status not-enrolled">
          <p>⚠️ MFA is not enabled. Enhance your security by enabling it now.</p>
          <p><strong>Note:</strong> You'll be prompted to set up MFA (SMS, Authenticator App, or Email) during your next login.</p>
          <button onClick={promptMFAEnrollment}>Enable MFA Now</button>
        </div>
      ) : enrollmentStatus === "error" ? (
        <div className="mfa-status error">
          <p>Unable to check MFA status. Please try again later.</p>
        </div>
      ) : null}
      
      <div className="mfa-info">
        <h4>Why enable MFA?</h4>
        <ul>
          <li>Protect your financial and benefits information</li>
          <li>Prevent unauthorized access to your account</li>
          <li>Meet industry security standards</li>
          <li>Required for handling sensitive personal data</li>
        </ul>
      </div>
    </div>
  );
};

export default MFAEnrollment;
