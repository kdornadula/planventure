# Building the Planventure API with GitHub Copilot

This guide will walk you through creating a Flask-based REST API with SQLAlchemy and JWT authentication using GitHub Copilot to accelerate development.

## Prerequisites

- Python 3.8 or higher
- VS Code with GitHub Copilot extension
- Bruno API Client (for testing API endpoints)
- Git installed

## Project Structure

We'll be working in the `api-start` branch and creating a structured API with:

- Authentication system
- Database models
- CRUD operations for trips
- JWT token protection

## Step 1: Project Setup

### Prompts to Configure Flask with SQLAlchemy

Open Copilot Chat and type:

```
@workspace Update the Flask app with SQLAlchemy and basic configurations
```

When the code is generated, click "Apply in editor" to update your `app.py` file.

### Update Dependencies

In Copilot Chat, type:

```
update requirements.txt with necessary packages for Flask API with SQLAlchemy and JWT
```

Install the updated dependencies:

```bash
pip install -r requirements.txt
```

### Create .env File

Create a `.env` file for environment variables and add it to `.gitignore`.

## Step 2: Database Models

### User Model

In Copilot Edits, type:

```
Create SQLAlchemy User model with email, password_hash, and timestamps. add code in new files
```

Review and accept the generated code.

### Initialize Database Tables

Ask Copilot to create a database initialization script:

```
update code to be able to create the db tables with a python shell script
```

Run the initialization script:

```bash
python create_db.py
```

To reset the database (WARNING: deletes all data):

```bash
python create_db.py --reset
```

### Install SQLite Viewer Extension

1. Go to VS Code extensions
2. Search for "SQLite viewer"
3. Install the extension
4. Click on `init_db.py` to view the created tables

### Trip Model

In Copilot Edits, type:

```
Create SQLAlchemy Trip model with user relationship, destination, start date, end date, coordinates and itinerary
```

Accept changes and run the initialization script again:

```bash
python create_db.py
```

### Commit Your Changes

Use Source Control in VS Code:

1. Stage all changes
2. Click the sparkle icon to generate a commit message with Copilot
3. Click commit

## Step 3: Authentication System

### Password Hashing Utilities

In Copilot Edits, type:

```
Create password hashing and salt utility functions for the User model
```

Review, accept changes, and install required packages:

```bash
pip install bcrypt
```

### JWT Token Functions

In Copilot Edits, type:

```
Setup JWT token generation and validation functions
```

Review, accept changes, and install the JWT package:

```bash
pip install flask-jwt-extended
```

### Registration Route

In Copilot Edits, type:

```
Create auth routes for user registration with email validation
```

Review and accept the changes.

### Test Registration Route

Use Bruno API Client:

1. **Download and Install Bruno**

   - Download from [Bruno GitHub Releases](https://github.com/usebruno/bruno/releases)
   - Install the desktop application

2. **Create New Collection - IMPORTANT PATH SETUP**

   - Open Bruno
   - Click "Create Collection"
   - Name it "Planventure API"
   - **Choose folder location**: Select a simple path like `/Users/gayathridornadula/Desktop/bruno-collections` or `/Users/gayathridornadula/Documents/bruno-collections`
   - **DO NOT** choose the planventure-api project folder to avoid path conflicts

3. **Alternative: Use Bruno in a separate directory**

   - Create a new folder: `mkdir ~/Desktop/bruno-planventure`
   - Open Bruno and create collection in this folder
   - This avoids conflicts with your project structure

4. **Create Registration Request**

   - Right-click collection → "New Request"
   - Name: "User Registration" (avoid spaces if issues persist, use "User_Registration")
   - Method: POST
   - URL: `http://localhost:5000/auth/register`

5. **Set Headers**

   - Click "Headers" tab
   - Add: `Content-Type: application/json`

6. **Add Request Body**
   - Click "Body" tab
   - Select "JSON"
   - Add JSON body:

```json
{
  "email": "user@example.com",
  "password": "test1234"
}
```

7. **Send Request**
   - Click "Send" button
   - Verify you get a 201 status with user data and JWT tokens

### Test Login Route

1. **Create Login Request**

   - Right-click collection → "New Request"
   - Name: "User Login"
   - Method: POST
   - URL: `http://localhost:5000/auth/login`

2. **Set Headers**

   - Add: `Content-Type: application/json`

3. **Add Request Body**
   - Select JSON body type
   - Add same credentials:

```json
{
  "email": "user@example.com",
  "password": "test1234"
}
```

4. **Send and Verify**
   - Should return 200 status with user info and fresh JWT tokens

### Test Email Validation

1. **Create Email Validation Request**

   - New Request: "Validate Email"
   - Method: POST
   - URL: `http://localhost:5000/auth/validate-email`

2. **Test Different Emails**

```json
{
  "email": "test@example.com"
}
```

### Bruno Tips for API Testing

1. **Environment Variables Setup - Multiple Methods**

   **Method 1: Collection Menu (Most Common)**

   - Click on your collection name "Planventure API"
   - Look for "Environments" tab or button
   - Click "Add Environment" or "+"

   **Method 2: File Menu**

   - Go to **File** → **New Environment**
   - Or **File** → **Collection Settings** → **Environments**

   **Method 3: Right-click Collection**

   - Right-click your collection → **"Manage Environments"**
   - Or Right-click → **"Settings"** → **"Environments"**

   **Method 4: If Nothing Works - Manual Token Copy**

   - After login, copy the `access_token` from response
   - In each protected request, manually paste in Authorization header:
   - `Authorization: Bearer paste-your-token-here`

   **Video Resources:**

   - [Bruno Official Documentation](https://docs.usebruno.com/)
   - [Bruno Environment Variables Tutorial](https://www.youtube.com/results?search_query=bruno+api+environment+variables)
   - Search YouTube for: "Bruno API Client tutorial environment variables"

   **Environment Variables to Create:**

   - `base_url` = `http://localhost:5000`
   - `access_token` = (leave empty initially)

2. **Fallback Method - No Environment Variables**
   If you can't find environment settings, you can still test:

   - Use full URLs: `http://localhost:5000/auth/register`
   - Copy JWT token from login response manually
   - Paste into Authorization header for each protected request

3. **Automatic JWT Token Management**
   - In "Tests" tab of login request, add this script:

```javascript
// Automatically save JWT token from login response
if (res.status === 200) {
  const response = JSON.parse(res.body);
  if (response.tokens && response.tokens.access_token) {
    bru.setEnvVar("access_token", response.tokens.access_token);
    bru.setEnvVar("refresh_token", response.tokens.refresh_token);
    console.log("✅ JWT tokens updated automatically");
  }
}
```

4. **Use Tokens in All Protected Routes**

   - In Headers for ALL protected requests: `Authorization: Bearer {{access_token}}`
   - The token automatically updates every time you login
   - No manual copying needed!

5. **Token Refresh Setup (Advanced)**
   - Create a "Refresh Token" request
   - Method: POST, URL: `{{base_url}}/auth/refresh`
   - Body: `{"refresh_token": "{{refresh_token}}"}`
   - Tests script:

```javascript
if (res.status === 200) {
  const response = JSON.parse(res.body);
  bru.setEnvVar("access_token", response.access_token);
}
```

6. **Pre-request Scripts for Auto-refresh**
   - In collection settings, add pre-request script:

```javascript
// Auto-refresh expired tokens
if (bru.getEnvVar("access_token")) {
  // Add logic to check token expiry and refresh if needed
}
```

### Bruno JWT Token Automation - Step by Step Guide

**IMPORTANT: Follow these exact steps for automatic JWT token management**

#### Step 1: Create Environment Variable

1. **Open Bruno and go to your "Planventure API" collection**
2. **Look for "Environments" in the left sidebar** (below your collection)
3. **If you can't find it, try:** Right-click collection → "Settings" → "Environments"
4. **Click "Create Environment"**
5. **Name it:** "Development"
6. **Add these variables:**
   - Variable: `base_url`, Value: `http://localhost:5000`
   - Variable: `access_token`, Value: (leave this EMPTY for now)
7. **Click "Save"**
8. **Make sure "Development" environment is SELECTED/ACTIVE**

#### Step 2: Update Your Login Request

1. **Open your "User Login" request**

   - In Bruno, click on your "User Login" request in the left sidebar

2. **Change the URL to use environment variable:**

   - Look at the top of the request where you see the URL field
   - You should see something like: `http://localhost:5000/auth/login`
   - **Clear this field completely**
   - **Type exactly:** `{{base_url}}/auth/login`
   - The URL field should now show: `{{base_url}}/auth/login`

3. **Visual Guide for URL Change:**

   ```
   BEFORE: http://localhost:5000/auth/login
   AFTER:  {{base_url}}/auth/login
   ```

4. **Go to the "Tests" tab** (next to Headers, Body, etc.)

   - Look for tabs at the top: "Params", "Headers", "Body", "Tests"
   - Click on "Tests"

5. **Add this EXACT script:**

```javascript
// Check if login was successful
if (res.status === 200) {
  try {
    // Parse the response
    const response = JSON.parse(res.body);

    // Extract the access token
    if (response.tokens && response.tokens.access_token) {
      // Save token to environment
      bru.setEnvVar("access_token", response.tokens.access_token);
      console.log("✅ Access token saved successfully!");
      console.log(
        "Token:",
        response.tokens.access_token.substring(0, 20) + "..."
      );
    } else {
      console.log("❌ No tokens found in response");
    }
  } catch (error) {
    console.log("❌ Error parsing response:", error);
  }
} else {
  console.log("❌ Login failed with status:", res.status);
}
```

6. **Save the request in Bruno:**

   **Method 1: Keyboard Shortcut (Easiest)**

   - Press `Ctrl+S` (Windows/Linux) or `Cmd+S` (Mac)

   **Method 2: Auto-save**

   - Bruno usually auto-saves changes automatically
   - Look for any unsaved indicator (like a dot or asterisk) next to the request name
   - If you see it, the request needs to be saved

   **Method 3: Manual Save**

   - Look for a "Save" button in the toolbar
   - Or go to File → Save

   **Method 4: Close and Reopen**

   - If changes aren't saving, close the request tab
   - Click on the request again from the left sidebar
   - Re-add your changes and try saving again

   **How to verify it's saved:**

   - Close Bruno completely
   - Reopen Bruno and your collection
   - Open the Login request
   - Check if the Tests script is still there
   - The URL should still show `{{base_url}}/auth/login`

#### Troubleshooting Token Automation

**If you don't see a Console tab in Bruno:**

**Bruno Version Differences:**

- **Newer Bruno versions** may not have a visible Console tab
- **Older Bruno versions** have Console at the bottom
- **Some versions** show console output in different locations

**Alternative Debugging Methods:**

1. **Check Response Tab Instead:**

   - After login, look at the "Response" tab
   - Scroll down to see if there are any script execution messages
   - Some versions show console output here

2. **Look for Output Panel:**

   - Check bottom of Bruno window for any output/logs panel
   - Look for "Logs", "Output", or "Script Results" tabs
   - May be collapsed - try expanding bottom panel

3. **Check Browser DevTools (if Bruno is Electron-based):**

   - Press F12 or Ctrl+Shift+I in Bruno
   - Look at Console tab in DevTools
   - Script output might appear there

4. **Manual Token Verification (Most Reliable):**

   - After login, copy the `access_token` from response manually
   - Go to Environments → Development → `access_token` field
   - Paste the token manually
   - Click Save
   - Test if `{{access_token}}` works in a test request

5. **Simple Test Method:**

   - Create a test request: GET `{{base_url}}/health`
   - Add header: `Authorization: Bearer {{access_token}}`
   - If this works after login → automation is working
   - If this fails → token isn't being saved

6. **Alternative Script for Debugging:**
   Replace your Tests script with this version that forces a visual indicator:

```javascript
// Enhanced debugging script
if (res.status === 200) {
  const data = JSON.parse(res.body);
  if (data.tokens && data.tokens.access_token) {
    bru.setEnvVar("access_token", data.tokens.access_token);
    // This should show in response somewhere
    alert("Token saved successfully!");
  } else {
    alert("No tokens found in response!");
  }
} else {
  alert("Login failed with status: " + res.status);
}
```

**Quick Verification Steps (No Console Needed):**

1. **Login with your script**
2. **Go to Environments → Development**
3. **Check if `access_token` has a long string value**
4. **If YES → automation is working**
5. **If NO → try manual copy-paste method**

**Manual Method (Always Works):**

1. Login and copy the `access_token` from response
2. Go to Environments → Development
3. Paste token into `access_token` field
4. Save environment
5. Use `{{access_token}}` in Authorization headers

## Step 4: Trip Routes

### Create Trip Routes Blueprint

In Copilot Edits, type:

```

Create Trip routes blueprint with CRUD operations

```

Review and accept the changes.

> **Note**: Ensure that `verify_jwt_in_request` is set to `verify_jwt_in_request(optional=True)` if needed

### Test Trip Routes

Use Bruno API Client to test:

1. **CREATE a new trip**
   - Method: POST
   - URL: `{{base_url}}/trips`
   - Headers: `Authorization: Bearer {{access_token}}`
   - Body:

```json
{
  "destination": "Paris, France",
  "start_date": "2024-06-01",
  "end_date": "2024-06-07",
  "latitude": 48.8566,
  "longitude": 2.3522
}
```

2. **GET a trip by ID**

   - Method: GET
   - URL: `{{base_url}}/trips/1`
   - Headers: `Authorization: Bearer {{access_token}}`

3. **GET all user trips**
   - Method: GET
   - URL: `{{base_url}}/trips`
   - Headers: `Authorization: Bearer {{access_token}}`

### Bruno Collection Export/Import

1. **Export Collection**

   - Right-click collection → "Export"
   - Save as `planventure-api.json`
   - Share with team members

2. **Import Collection**
   - Click "Import Collection"
   - Select the exported JSON file

## Step 5: Finalize API

### Configure CORS for Frontend Access

In Copilot Edits, type:

```
Setup CORS configuration for React frontend
```

Review and accept the changes.

### Add Health Check Endpoint

In Copilot Edits, type:

```
Create basic health check endpoint
```

Review and accept the changes.

### Commit Final Changes

Use Source Control with Copilot to create your final commit.

### Create README

Ask Copilot to write a comprehensive README for your API project.

## Common Issues and Solutions

### Login Working But Getting Errors - Troubleshooting

1. **Check Flask Console Output**

   - Look for error messages in your terminal where Flask is running
   - Check for any `❌ Login error:` messages

2. **Verify Database**

   - Run: `python create_db.py` to ensure tables exist
   - Check if user was actually created during registration

3. **Test Registration First**

   - Ensure registration works before testing login
   - Use same email/password for both registration and login

4. **Common Error Fixes**

   - **500 Internal Server Error**: Check Flask console for stack trace
   - **401 Unauthorized**: Password mismatch or user doesn't exist
   - **400 Bad Request**: Missing email or password in request body

5. **Debug Steps**

   ```bash
   # Check if your Flask app is running
   curl http://localhost:5000/health

   # Test with curl instead of Bruno
   curl -X POST http://localhost:5000/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"user@example.com","password":"test1234"}'
   ```

### GOTCHAS:

- Ensure there are no trailing slashes in any of the routes - especially the base `/trip` route
- Make sure all required packages are installed
- Check that JWT token validation is configured correctly
- Verify database tables are created properly using the SQLite viewer
- **NEW**: If login works but shows errors, check Flask console output for actual error details

## Next Steps

Consider these enhancements for your API:

- Add more comprehensive input validation
- Create custom error handlers for HTTP exceptions
- Setup logging configuration
- Add validation error handlers for form data
- Configure database migrations

## Conclusion

You now have a fully functional API with authentication, database models, and protected routes. This can serve as the backend for your Planventure application!
You now have a fully functional API with authentication, database models, and protected routes. This can serve as the backend for your Planventure application!
