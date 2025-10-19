# Auth0 MFA Setup - Quick Guide

## Step 1: Add Action to Login Flow

1. Go to: https://manage.auth0.com/
2. Click **Actions** in left sidebar
3. Click **Flows**
4. Click **Login**
5. In the right panel, find "Enforce MFA for Benefits Advisor" under Custom tab
6. **Drag it** between Start and Complete
7. Click **Apply** button

## Step 2: Enable MFA

1. Click **Security** in left sidebar
2. Click **Multi-factor Auth**
3. Toggle ON **"One-time Password"** (for authenticator apps like Google Authenticator)
4. Scroll down to "Define policies"
5. Select **"Always"**
6. Click **Save**

## Step 3: Test

1. Go to http://localhost:3001
2. Click "Log In"
3. Sign up with new email
4. You'll be prompted to set up MFA immediately
5. Scan QR code with Google Authenticator
6. Done!

---

**That's it!** After these steps, all users must set up MFA when they sign up.
