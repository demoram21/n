# 🚀 Skin Disease Detection API - Deployment Guide

## 📁 Required Files for Deployment

### ✅ Essential Files:
- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `render.yaml` - Render.com configuration
- `skin_disease_model.h5` - ML model (25MB)
- `.gitattributes` - Git LFS configuration for model
- `.env` - Local environment variables (not deployed)
- `.env.example` - Template for environment variables
- `.gitignore` - Files to ignore in git
- `README.md` - Project documentation

### ❌ Removed Files:
- `venv/` - Virtual environment (not needed in deployment)
- `vercel.json` - Removed (Vercel has ML model limitations)
- `SETUP.md` - Merged into this README

---

## 🏆 Recommended: Deploy to Render.com

### Why Render?
- ✅ Perfect for ML applications with large models
- ✅ Free tier available
- ✅ Automatic HTTPS
- ✅ Easy environment variable management
- ✅ Built-in CI/CD from GitHub

### 📋 Render Deployment Steps:

#### 1. **Prepare Repository**
```bash
# Add all files and push to GitHub
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

#### 2. **Deploy on Render**
1. Go to [render.com](https://render.com) and sign up/login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Render will automatically detect your `render.yaml` configuration

#### 3. **Set Environment Variables**
In Render dashboard → Environment:
- `TELEGRAM_BOT_TOKEN` = `8327110814:AAEUYJqkifkImQSHnhKPv1cTB7Zh1O5Xshk`
- `TELEGRAM_CHAT_ID` = `6791150444`

#### 4. **Deploy**
- Render automatically builds and deploys
- Your API will be live at: `https://your-app-name.onrender.com`

---

## 🔄 Alternative Deployment Options

### **Option 2: Railway.app**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

### **Option 3: Heroku**
Create `Procfile`:
```
web: gunicorn app:app
```

Deploy:
```bash
heroku create your-app-name
heroku config:set TELEGRAM_BOT_TOKEN=8327110814:AAEUYJqkifkImQSHnhKPv1cTB7Zh1O5Xshk
heroku config:set TELEGRAM_CHAT_ID=6791150444
git push heroku main
```

### **Option 4: Google Cloud Run**
```dockerfile
# Create Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080"]
```

---

## 🔧 Configuration Details

### `render.yaml` Configuration:
```yaml
services:
  - type: web
    name: skin-disease-api
    env: python
    region: oregon
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:$PORT
    envVars:
      - key: TELEGRAM_BOT_TOKEN
        sync: false
      - key: TELEGRAM_CHAT_ID  
        sync: false
```

### Key Dependencies:
```txt
Flask==3.1.2
tensorflow==2.20.0
gunicorn==23.0.0
pillow==11.3.0
flask-cors==6.0.1
python-dotenv==1.0.0
```

---

## 🧪 Test Your Deployed API

### Health Check:
```bash
curl https://your-app-name.onrender.com/
```

### Test Prediction:
```bash
curl -X POST https://your-app-name.onrender.com/predict \
  -F "image=@test_image.jpg"
```

### Test Telegram Integration:
```bash
curl -X POST https://your-app-name.onrender.com/share-telegram \
  -H "Content-Type: application/json" \
  -d '{
    "disease": "Acne and Rosacea Photos",
    "confidence": 0.95,
    "treatment": "Test treatment"
  }'
```

---

## 📊 Deployment Comparison

| Platform | ML Models | Free Tier | Ease | Best For |
|----------|-----------|-----------|------|----------|
| **Render** | ✅ Excellent | ✅ 750hrs/month | ⭐⭐⭐⭐⭐ | **ML Apps** |
| Railway | ✅ Good | ✅ $5 credit | ⭐⭐⭐⭐ | Full-stack |
| Heroku | ⚠️ Limited | ❌ Paid only | ⭐⭐⭐ | Traditional apps |
| Vercel | ❌ Poor | ✅ Generous | ⭐⭐⭐⭐⭐ | Frontend/small APIs |

---

## 🎯 Quick Start (Render)

1. **Push to GitHub**: `git push origin main`
2. **Go to Render.com** and connect repository
3. **Add environment variables** in dashboard
4. **Deploy** - Render handles the rest!
5. **Test** your live API endpoints

Your skin disease detection API will be live in minutes! 🎉

---

## 🔒 Security Notes

- ✅ Environment variables stored securely on Render
- ✅ `.env` file not committed to git
- ✅ HTTPS automatically enabled
- ✅ CORS configured for your frontend