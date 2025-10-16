# Skin Disease Classification Backend

Flask backend API for skin disease detection using TensorFlow/Keras.

## 🚀 Deploying to Vercel

### Step-by-Step Deployment Guide

#### 1. **Install Vercel CLI** (if not already installed)
```bash
npm install -g vercel
```

#### 2. **Login to Vercel**
```bash
vercel login
```

#### 3. **Navigate to the backend directory**
```bash
cd /home/ramji/desktop/sha/backend
```

#### 4. **Deploy to Vercel**
```bash
vercel
```
- Follow the prompts:
  - "Set up and deploy?" → **Yes**
  - "Which scope?" → Select your account
  - "Link to existing project?" → **No** (first time)
  - "What's your project's name?" → **backend** or your preferred name
  - "In which directory is your code located?" → **./**

#### 5. **Set Environment Variables** (if using Telegram bot)
```bash
vercel env add TELEGRAM_BOT_TOKEN
vercel env add TELEGRAM_CHAT_ID
```
Or add them through the Vercel dashboard.

#### 6. **Deploy to Production**
```bash
vercel --prod
```

---

## 📋 What does `vercel.json` do?

The `vercel.json` file configures how Vercel deploys your application:

```json
{
  "version": 2,                          // Vercel configuration version
  "builds": [
    {
      "src": "app.py",                   // Entry point file
      "use": "@vercel/python"            // Use Python runtime
    }
  ],
  "routes": [
    {
      "src": "/(.*)",                    // Match all routes
      "dest": "app.py"                   // Route to app.py
    }
  ],
  "env": {
    "TELEGRAM_BOT_TOKEN": "@telegram_bot_token",  // Environment variables
    "TELEGRAM_CHAT_ID": "@telegram_chat_id"
  }
}
```

**Key Components:**
- **builds**: Tells Vercel how to build your app (using Python runtime)
- **routes**: Defines URL routing (all requests go to app.py)
- **env**: References to environment variables (secrets stored in Vercel)

---

## ⚠️ Important Vercel Limitations

**TensorFlow/ML Models on Vercel:**
- **Function Size Limit**: 50MB (Serverless functions)
- **Memory Limit**: 1024MB (Pro: 3GB)
- **Execution Timeout**: 10s (Hobby), 60s (Pro)

Your `skin_disease_model.h5` file is **~180MB**, which **exceeds Vercel's limits**.

### 🔧 Recommended Solutions:

#### Option 1: Use Render.com instead (Recommended)
You already have `render.yaml` - Render supports larger models better.

#### Option 2: Use Vercel with External Model Storage
- Store model on cloud storage (AWS S3, Google Cloud Storage)
- Load model on-demand (slower, but works within limits)

#### Option 3: Deploy to Heroku/Railway/Fly.io
These platforms have better support for ML applications.

---

## 🏃 Local Development

### 1. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application
```bash
python app.py
```

The server will start on `http://localhost:5000`

---

## 📝 API Endpoints

- **POST /predict**: Upload image for skin disease classification
- **POST /send-telegram**: Send diagnosis report to Telegram

---

## 🔒 Environment Variables

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token
- `TELEGRAM_CHAT_ID`: Telegram chat ID for notifications
- `PORT`: Server port (default: 5000)

---

## 📦 Dependencies

See `requirements.txt` for full list. Key dependencies:
- Flask
- TensorFlow
- Pillow
- NumPy
- Flask-CORS
# n
