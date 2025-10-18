# ✅ SIMPLE MFA SETUP - DO THIS NOW

## What You Need to Do (5 Minutes)

Since you're looking at the Auth0 Dashboard with your application open, here's the EXACT steps:

### 1. Click "Security" in Left Sidebar
   
   Look at the left side of your Auth0 Dashboard → Click **"Security"**

### 2. Click "Multi-factor Auth"

   Under Security, you'll see several options. Click **"Multi-factor Auth"**

### 3. Enable ONE MFA Method

   You'll see a list of MFA options. Toggle ON **ONE** of these:
   
   - ✅ **One-time Password** (Best for testing - use Google Authenticator app)
   - ✅ **Email** (Easiest for testing - no app needed)
   - ⚪ SMS (requires phone setup)
   
   **Recommendation:** Enable "One-time Password" first

### 4. Set Policy to "Always"

   Scroll down to **"Define policies"**
   
   Select: **"Always"** or **"Always require Multi-factor Authentication"**

### 5. Click "Save"

   At the bottom of the page, click the **"Save"** button

## That's It!

Now test it:

1. Go to http://localhost:3001 (your app should already be running)
2. Log out if you're logged in
3. Click "Log In"
4. Sign up with a NEW email address
5. **YOU WILL BE PROMPTED TO SET UP MFA**
6. Scan QR code with Google Authenticator (if you chose One-time Password)
7. OR enter code sent to your email (if you chose Email)
8. Complete setup
9. You're logged in with MFA active! ✅

## Why This Works Without Actions/Flows

Auth0's built-in MFA settings automatically:
- Force MFA enrollment for new users
- Prompt existing users to enroll
- Require MFA on every login when policy is "Always"
- Add MFA status to user tokens

The Action we created earlier was extra security, but **not required** when you use the built-in MFA settings with "Always" policy.

## Direct Link

Use this direct link to get to MFA settings:

https://manage.auth0.com/dashboard/us/dev-4zwtflcwcdswqbd2/security/mfa

(Replace `dev-4zwtflcwcdswqbd2` with your tenant name if different)

---

**Questions?** Check the main AUTH0_FLOW_SETUP.md for troubleshooting!
