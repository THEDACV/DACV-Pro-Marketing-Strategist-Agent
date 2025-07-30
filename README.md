# 🚀 DACV Pro: Advanced Marketing Strategist

AI-powered marketing strategy generator leveraging real-time data, OpenAI, Stripe, and dynamic market insights to deliver tailored campaigns for your business.

---

## 🌟 Features

- 🎯 **AI-Generated Marketing Strategies**  
  Generate high-impact marketing plans based on product description, audience, and budget.

- 📈 **Real-Time Market & SEO Insights**  
  Get current social trends, SEO metrics, and sentiment analysis.

- 💳 **Subscription & Payment Integration**  
  Stripe-powered pricing tiers with user session tracking and plan-based access.

- 📊 **User History & Strategy Archive**  
  Keep track of previously generated strategies.

- 🔐 **Rate Limiting & Usage Tracking**  
  Protect backend and enforce usage limits for free users.

---

## 📦 Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, Vanilla JS, Stripe.js
- **APIs:** OpenAI, Market Data API (mock), Sentiment API (mock)
- **Payment:** Stripe Subscriptions
- **Security:** Flask-Limiter, Webhooks

---

## 🚀 Getting Started

### 1. 🔧 Clone the Repository

```bash
git clone https://github.com/yourusername/advanced-marketing-strategist.git
cd advanced-marketing-strategist

2. 📦 Install Dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. 🔐 Set Environment Configuration
Edit app.config.update() section in advanced_marketing_strategist.py with your actual credentials:

python
Copy
Edit

OPENAI_API_KEY='your-openai-api-key'
STRIPE_PUBLIC_KEY='your-stripe-public-key'
STRIPE_SECRET_KEY='your-stripe-secret-key'
MARKET_DATA_API_KEY='your-market-data-api-key'
SENTIMENT_API_KEY='your-sentiment-api-key'
STRIPE_WEBHOOK_SECRET='your-stripe-webhook-secret'

📄 License
MIT License © 2025 [Chaithanya Vishwamitra D A]
