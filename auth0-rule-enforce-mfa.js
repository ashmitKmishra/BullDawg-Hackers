// Auth0 Rule: Enforce MFA for All Users
// 
// This is an ALTERNATIVE to Actions if you don't have access to Flows
// To use this:
// 1. Go to Auth0 Dashboard → Auth Pipeline → Rules
// 2. Click "Create Rule"
// 3. Choose "Empty Rule"
// 4. Name it: "Enforce MFA for Benefits Advisor"
// 5. Paste this code
// 6. Click "Save Changes"

function enforceMFA(user, context, callback) {
  // Check if user has completed MFA in this session
  const completedMfa = context.authentication && 
                       context.authentication.methods &&
                       context.authentication.methods.find(method => method.name === 'mfa');

  // Get enrolled MFA factors from user
  const enrolledFactors = user.multifactor || [];
  
  // If user hasn't completed MFA in this session
  if (!completedMfa) {
    // If user has no MFA factors enrolled, force enrollment
    if (enrolledFactors.length === 0) {
      context.multifactor = {
        provider: 'any',
        allowRememberBrowser: false
      };
    } else {
      // User has MFA but didn't use it, challenge them
      context.multifactor = {
        provider: 'any',
        allowRememberBrowser: false
      };
    }
  }

  // Add custom claims to the token
  const namespace = 'https://auth0.com/';
  
  // Add MFA status claim
  if (completedMfa) {
    context.idToken[namespace + 'mfa_enrolled'] = true;
    context.accessToken[namespace + 'mfa_enrolled'] = true;
  } else {
    context.idToken[namespace + 'mfa_enrolled'] = false;
    context.accessToken[namespace + 'mfa_enrolled'] = false;
  }
  
  // Track if this is a new user (first login)
  const isNewUser = context.stats.loginsCount === 1;
  context.idToken[namespace + 'is_new_user'] = isNewUser;
  
  // Store first login timestamp for new users
  if (isNewUser) {
    user.app_metadata = user.app_metadata || {};
    user.app_metadata.first_login = new Date().toISOString();
    
    auth0.users.updateAppMetadata(user.user_id, user.app_metadata)
      .then(() => callback(null, user, context))
      .catch(err => callback(err));
  } else {
    callback(null, user, context);
  }
}
