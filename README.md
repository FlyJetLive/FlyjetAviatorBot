# Flyjet Aviator Signals Bot

Aviator signals prediction bot for Telegram. Uses WebSocket data to predict crash points.

### 🚀 How to Deploy
1. Clone the repository
2. Add your `.env` file with required credentials
3. Deploy on [Render](https://render.com/) with the given Procfile

### ⚙️ Commands
- **Aviator Signal Test:**  
```bash
curl -X POST -H "Content-Type: application/json" -d "{\"signal\": \"2X Coming Soon\"}" https://<YOUR_RENDER_URL>/aviator
