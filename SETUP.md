# Environment Setup Guide

## ✅ Configuration Complete!

Your `.env` file has been created with your Telegram credentials.

### 📁 Files Created/Updated:

1. **`.env`** - Contains your Telegram bot token and chat ID (🔒 **NOT committed to git**)
2. **`.env.example`** - Template file for other developers (✅ **Safe to commit**)
3. **`requirements.txt`** - Updated with `python-dotenv` package
4. **`app.py`** - Updated to load environment variables from `.env`
5. **`.gitignore`** - Updated to exclude `.env` files

---

## 🚀 How to Run Locally

### Option 1: Using Virtual Environment (Recommended)

```bash
# Navigate to backend directory
cd /home/ramji/desktop/sha/backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Option 2: Using pipx

```bash
cd /home/ramji/desktop/sha/backend
pipx run --spec -r requirements.txt flask run
```

---

## 🌐 Deploy to Vercel

When you deploy to Vercel, you need to set the environment variables:

### Method 1: Vercel Dashboard
1. Go to your project on Vercel
2. Click **Settings** → **Environment Variables**
3. Add:
   - `TELEGRAM_BOT_TOKEN` = `8327110814:AAEUYJqkifkImQSHnhKPv1cTB7Zh1O5Xshk`
   - `TELEGRAM_CHAT_ID` = `6791150444`

### Method 2: Vercel CLI
```bash
vercel env add TELEGRAM_BOT_TOKEN
# Enter: 8327110814:AAEUYJqkifkImQSHnhKPv1cTB7Zh1O5Xshk

vercel env add TELEGRAM_CHAT_ID
# Enter: 6791150444
```

---

## ⚠️ Important Security Notes

- ✅ `.env` is in `.gitignore` - your secrets are safe
- ✅ Never commit `.env` file to GitHub
- ✅ Use `.env.example` as a template for other developers
- ✅ On Vercel, environment variables are stored securely

---

## 🧪 Test Your Setup

Once running, test the endpoints:

```bash
# Health check
curl http://localhost:5000/

# Test prediction (with an image)
curl -X POST -F "image=@test_image.jpg" http://localhost:5000/predict

# Test Telegram integration
curl -X POST http://localhost:5000/share-telegram \
  -H "Content-Type: application/json" \
  -d '{"disease": "Test", "confidence": 0.95, "treatment": "Test treatment"}'
```

---

## 📝 Environment Variables

Your `.env` file contains:
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot authentication token
- `TELEGRAM_CHAT_ID`: The chat ID where reports will be sent
- `PORT`: Server port (default: 5000)

---

## 🔄 Next Steps

1. ✅ Environment variables configured
2. 📦 Install dependencies in virtual environment
3. 🏃 Run locally to test
4. 🚀 Deploy to Vercel
5. 🔧 Add environment variables on Vercel
6. 🎉 Test your deployed API!
