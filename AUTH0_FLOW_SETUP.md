# 🔧 How to Enable MFA in Auth0 (Correct Method)

## Important Clarification
You're right - "Flows" under Actions is different from "Forms". Since your Auth0 plan may not have the Actions > Flows feature, let's use the **built-in MFA settings** which is simpler and works on all plans.

## Simple Method: Enable MFA Directly (Works on All Plans)

### Step 1: Enable Multi-Factor Authentication

1. **Open Auth0 Dashboard**
   - Go to: https://manage.auth0.com/
   - Log in to your tenant: `dev-4zwtflcwcdswqbd2.us.auth0.com`

2. **Navigate to Security → Multi-factor Auth**
   ```
   Left Sidebar:
   
   🚀 Getting Started
   📊 Activity
   📱 Applications
   🔐 Authentication
   👥 Organizations
   👤 User Management
   🎨 Branding
   ✅ Security  ← CLICK HERE
      ├── Attack Protection
      ├── Multi-factor Auth  ← THEN CLICK HERE
      ├── Security Center
      └── Monitoring
   � Monitoring
   � Actions
   �🛒 Marketplace
   🧩 Extensions
   ⚙️ Settings
   ```

3. **Enable MFA Factors**
   - Toggle ON at least one of these:
     - ✅ **One-time Password** (Google Authenticator, Authy) ← RECOMMENDED FOR TESTING
     - ✅ **SMS** (requires phone number)
     - ✅ **Email** (simplest for testing)
     - ✅ **Push Notifications via Auth0 Guardian**
     - ✅ **WebAuthn with FIDO Security Keys**

4. **Configure MFA Policy**
   - Scroll down to **"Define policies"**
   - Select: **"Always"** - This requires MFA for every login
   - OR Select: **"Adaptive"** - Smart MFA based on risk
   
5. **Click "Save"** at the bottom of the page

### Step 2: Configure When Users Enroll

1. Still on the Multi-factor Auth page
2. Look for **"Factor Selection"** or **"Enrollment Policy"**
3. Choose one:
   - **"Prompt users to enroll in MFA on first login"**
   - **"Require enrollment at first login"** ← RECOMMENDED

4. **Save** the changes

## What This Will Do

Once you enable MFA with the "Always" policy:

- ✅ **New users** signing up will be prompted to set up MFA immediately after creating their account
- ✅ **Existing users** without MFA will be prompted to enroll on their next login
- ✅ **All users** will need to provide MFA code every time they log in
- ✅ The app will automatically receive the MFA status in the user token

## Optional: Advanced Configuration with Actions (If Available)

If you DO have access to **Actions → Library** (not Flows):

1. Go to **Actions** → **Library**
2. Find the action: **"Enforce MFA for Benefits Advisor"**
3. Make sure it shows as "Deployed"
4. You may need a paid Auth0 plan to actually USE actions in the auth flow

**Note:** The built-in MFA settings above work just as well and don't require Actions!

## Testing After Enabling MFA

Once you've enabled MFA in Security settings:

1. **Logout completely** from your app
2. Clear browser cookies or use **Incognito/Private mode**
3. Go to http://localhost:3001
4. Click **"Log In"**
5. Try signing up with a new email
6. **You should immediately be prompted to set up MFA** after entering credentials
7. Choose an MFA method and complete setup
8. You'll be redirected back to the app
9. The app should show: ✅ "MFA is enabled on your account"

## Quick Visual Reference

When you're in Auth0 Dashboard and looking at your application (screenshot you provided):

You can see:
- ✅ Application Name: "Benefits & Financial Wellness Advisor"
- ✅ Domain: dev-4zwtflcwcdswqbd2.us.auth0.com
- ✅ Client ID: ImdLbfq0EBdJCnkDMLcTDzT3K5fX7t9m

Now you just need to:
1. Click **"Security"** in the left sidebar
2. Click **"Multi-factor Auth"**
3. Enable at least one MFA method
4. Set policy to **"Always"**
5. Save

That's it! No Actions/Flows/Forms needed.

## Current Action Status

✅ **Action Created**: Enforce MFA for Benefits Advisor (ID: 4197a3cf-7c79-43a9-8426-688efd1426eb)
✅ **Action Deployed**: Version 1 is live and built
⚠️ **Action NOT in Flow**: Needs to be manually added (see steps above)

## Troubleshooting

### "I don't see my action in the Custom panel"
- Refresh the page
- Make sure the action is deployed (check Actions → Library)
- Verify you're looking at the "Login" flow, not other flows

### "The Apply button is disabled"
- Make sure you've actually dragged the action into the flow
- The flow must have at least Start → Your Action → Complete

### "I still don't see MFA prompt after setup"
- Double-check the action is in the flow AND you clicked Apply
- Verify MFA is enabled in Security settings with "Always" policy
- Clear all cookies and try in incognito
- Check Auth0 Dashboard → Monitoring → Logs for errors

## Alternative Method: Use Auth0 Rules (If Flows Not Available)

If you don't have access to "Flows" (some Auth0 plans restrict this):

### Option B: Create a Rule Instead

1. Go to **Auth Pipeline** → **Rules** in the Auth0 Dashboard
2. Click **"Create Rule"**
3. Choose **"Empty Rule"**
4. Name it: **"Enforce MFA for Benefits Advisor"**
5. Copy the code from `auth0-rule-enforce-mfa.js` in this repo
6. Paste it into the rule editor
7. Click **"Save Changes"**
8. The rule will automatically be active

Rules work similarly to Actions but are the older method. They'll achieve the same result!

---

## Quick Check: Do You Have Actions Flows?

To check if your Auth0 plan supports Actions Flows:

1. Look at the left sidebar in Auth0 Dashboard
2. Click on **"Actions"**
3. Do you see these options?
   - ✅ **Flows** ← You have it! Follow the main guide above
   - ❌ Only see **Library** and **Triggers** ← Use the Rules method instead

---

**Next Steps:**
1. Add action to flow OR create rule (choose one method)
2. Enable MFA in Security settings
3. Test the login flow
4. Let me know the results!
