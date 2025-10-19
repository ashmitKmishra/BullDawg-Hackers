# Auth0 MFA Setup Guide

## ⚠️ IMPORTANT: Manual Configuration Required

The Auth0 Action has been created and deployed via MCP server, but it needs to be **manually bound to the Post-Login flow** in the Auth0 Dashboard. Follow these steps:

## Step 1: Bind Action to Post-Login Flow

1. Go to [Auth0 Dashboard](https://manage.auth0.com/)
2. Navigate to **Actions** → **Flows**
3. Click on **Login** flow
4. You should see your action "Enforce MFA for Benefits Advisor" in the **Custom** tab on the right side
5. **Drag and drop** the action into the flow between "Start" and "Complete"
6. Click **Apply** to save the flow

## Step 2: Enable MFA Methods in Auth0

1. In Auth0 Dashboard, go to **Security** → **Multi-factor Auth**
2. Enable at least one MFA method:
   - ✅ **SMS** (requires Twilio configuration or Auth0's built-in SMS)
   - ✅ **Authenticator Apps** (Google Authenticator, Authy, etc.) - RECOMMENDED
   - ✅ **Email** (simplest for testing)
   - ✅ **WebAuthn with FIDO2 security keys** (most secure)
3. Under "Define policies" select: **Require Multi-factor Auth** → **Always**
4. Click **Save**

## Step 3: Configure MFA Policy

1. Still in **Security** → **Multi-factor Auth**
2. Scroll to **Factor Priorities**
3. Arrange the factors in your preferred order
4. Under **Enrollment Policies**:
   - Choose "Prompt users to enroll at first login"
   - OR "Require enrollment at first login" (RECOMMENDED for this app)

## Step 4: Test the Flow

### Test New User Signup with MFA:

1. Open your app: http://localhost:3000 (or 3001)
2. Click "Log In"
3. Click "Sign up" on Auth0 Universal Login
4. Enter email and create password
5. **You should immediately be prompted to set up MFA**
6. Choose your MFA method (Authenticator App recommended)
7. Complete MFA setup:
   - For Authenticator App: Scan QR code with Google Authenticator/Authy
   - For SMS: Enter phone number and verify code
   - For Email: Verify code sent to your email
8. You'll be redirected back to the app
9. You should see:
   - ✅ Green checkmark: "MFA is enabled on your account"
   - Welcome message for new user

### Test Returning User Login with MFA:

1. Log out from the app
2. Click "Log In" again
3. Enter your credentials
4. **You should be prompted for MFA code**
5. Enter the code from your Authenticator app (or SMS/Email)
6. You'll be logged in successfully

### Test User Without MFA (if testing with existing account):

1. In Auth0 Dashboard, go to **User Management** → **Users**
2. Find your test user
3. Remove any MFA factors (if present)
4. Save
5. Try logging in - you should be forced to enroll in MFA

## Step 5: Verify Action is Working

After binding the action, you can verify it's working by:

1. Check the **Actions** → **Flows** → **Login** - the action should appear in the flow
2. Check the **Monitoring** → **Logs** after a login attempt
3. Look for logs related to "Enforce MFA for Benefits Advisor"
4. The logs should show MFA prompts and enrollment

## Common Issues and Solutions

### Issue: Not prompted for MFA on signup
**Solution:** 
- Ensure the action is in the Login flow
- Check that MFA is enabled in Security settings
- Verify the action code has `api.multifactor.enable('any')`

### Issue: "Enable MFA" button just logs me back in
**Solution:**
- This is expected behavior - MFA must be set up during the Auth0 login flow
- The action forces MFA enrollment at the Auth0 level
- User cannot bypass it

### Issue: Custom claims not showing in token
**Solution:**
- Ensure the action is deployed AND bound to the flow
- Check that custom claim namespace uses https:// format
- Verify the action code includes `api.idToken.setCustomClaim()`

### Issue: MFA status shows "Not Enrolled" even after setup
**Solution:**
- Clear browser cache and cookies
- Log out completely and log back in
- The custom claim is only added AFTER completing MFA
- Check browser console for user object to see if claim exists

## Verification Checklist

Before testing, ensure:

- [ ] Auth0 Action "Enforce MFA for Benefits Advisor" is created (✅ Done via MCP)
- [ ] Action is deployed (✅ Done via MCP)
- [ ] Action is bound to Login flow (⚠️ MANUAL STEP REQUIRED)
- [ ] At least one MFA method is enabled (⚠️ MANUAL STEP REQUIRED)
- [ ] MFA policy is set to "Always" or at first login (⚠️ MANUAL STEP REQUIRED)
- [ ] Application callbacks are configured (✅ Done via MCP)
- [ ] Development server is running on port 3000 or 3001

## Current Status

✅ **Completed:**
- Auth0 Action created: `Enforce MFA for Benefits Advisor` (ID: 4197a3cf-7c79-43a9-8426-688efd1426eb)
- Action deployed to post-login trigger
- Application configured with correct callbacks
- React components created (LoginButton, LogoutButton, Profile, MFAEnrollment)
- UI styled and ready

⚠️ **Manual Steps Needed:**
1. Bind action to Login flow in Auth0 Dashboard
2. Enable MFA methods in Security settings
3. Configure MFA policy

## Expected User Experience After Setup

### First-Time User:
1. Clicks "Log In" → redirected to Auth0
2. Signs up with email/password
3. **Immediately sees MFA enrollment screen**
4. Chooses MFA method and completes setup
5. Redirected to app with MFA enabled
6. Sees green checkmark confirming MFA

### Returning User (with MFA):
1. Clicks "Log In" → redirected to Auth0
2. Enters credentials
3. **Prompted for MFA code**
4. Enters code from authenticator/SMS/email
5. Logged in successfully
6. App shows MFA is active

### User Without MFA (should not be possible after setup):
1. Forced to enroll in MFA at login
2. Cannot proceed without completing MFA setup

## Technical Details

**Action Code Location:** Auth0 Dashboard → Actions → Library → "Enforce MFA for Benefits Advisor"

**Action Trigger:** post-login (v3)

**Action Logic:**
- Checks if MFA was completed in current session
- If not, forces MFA enrollment
- Adds custom claims to tokens
- Tracks new vs returning users
- Prevents login without MFA

**Custom Claims Added:**
- `https://auth0.com/mfa_enrolled` - Boolean indicating MFA status
- `https://auth0.com/is_new_user` - Boolean for first-time users

## Support

If you encounter issues:
1. Check Auth0 Dashboard → Monitoring → Logs
2. Check browser console for errors
3. Verify all manual steps are completed
4. Test with a fresh incognito window
5. Clear cookies and try again

---

**Next Steps:** Complete the manual configuration steps above, then test the complete flow!
