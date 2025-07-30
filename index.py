# advanced_marketing_strategist.py
from flask import Flask, request, jsonify, render_template_string
import openai
import os
from datetime import datetime
import stripe
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import requests
import json
import hashlib

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change for production

# Configuration
app.config.update(
    OPENAI_API_KEY='your-openai-api-key-here',
    STRIPE_PUBLIC_KEY='your-stripe-public-key',
    STRIPE_SECRET_KEY='your-stripe-secret-key',
    MARKET_DATA_API_KEY='your-market-data-api-key',
    SENTIMENT_API_KEY='your-sentiment-api-key',
    MAX_FREE_USES=1,
    STRIPE_WEBHOOK_SECRET='your-stripe-webhook-secret'  # For production
)

# Initialize services
openai.api_key = app.config['OPENAI_API_KEY']
stripe.api_key = app.config['STRIPE_SECRET_KEY']
limiter = Limiter(app=app, key_func=get_remote_address)

# Real-time data cache
real_time_cache = {}
CACHE_EXPIRY = 3600  # 1 hour

class RealTimeData:
    @staticmethod
    def get_social_media_trends():
        """Get real-time social media trends"""
        cache_key = hashlib.md5('social_trends'.encode()).hexdigest()
        if cache_key in real_time_cache:
            return real_time_cache[cache_key]
        
        try:
            # Mock API - replace with actual API
            response = requests.get(
                'https://api.example.com/social/trends',
                headers={'Authorization': f'Bearer {app.config["MARKET_DATA_API_KEY"]}'}
            )
            data = response.json()
            real_time_cache[cache_key] = data
            return data
        except:
            return {
                "trending_platforms": ["TikTok", "Instagram Reels", "LinkedIn"],
                "popular_content_types": ["Short Videos", "Live Streams", "Interactive Polls"],
                "engagement_tips": ["Use trending audio", "Post during peak hours", "Engage with comments"]
            }

    @staticmethod
    def get_seo_data(keyword):
        """Get real-time SEO data"""
        cache_key = hashlib.md5(f'seo_{keyword}'.encode()).hexdigest()
        if cache_key in real_time_cache:
            return real_time_cache[cache_key]
        
        try:
            # Mock API - replace with actual API
            response = requests.get(
                f'https://api.example.com/seo/{keyword}',
                headers={'Authorization': f'Bearer {app.config["MARKET_DATA_API_KEY"]}'}
            )
            data = response.json()
            real_time_cache[cache_key] = data
            return data
        except:
            return {
                "keyword_difficulty": "Medium",
                "search_volume": 5000,
                "cpc": 1.25,
                "related_keywords": [f"{keyword} tips", f"best {keyword}", f"{keyword} guide"]
            }

    @staticmethod
    def get_market_sentiment(product):
        """Get market sentiment"""
        cache_key = hashlib.md5(f'sentiment_{product}'.encode()).hexdigest()
        if cache_key in real_time_cache:
            return real_time_cache[cache_key]
        
        try:
            # Mock API - replace with actual API
            response = requests.post(
                'https://api.example.com/sentiment',
                headers={'Authorization': f'Bearer {app.config["SENTIMENT_API_KEY"]}'},
                json={'text': product}
            )
            data = response.json()
            real_time_cache[cache_key] = data
            return data
        except:
            return {
                "sentiment": "neutral",
                "confidence": 0.75,
                "keywords": ["innovative", "competitive", "emerging"]
            }

class UserManager:
    def __init__(self):
        self.user_data = {}  # In production, use a database
        
    def check_user(self, user_id):
        if user_id not in self.user_data:
            self.user_data[user_id] = {
                'uses': 0,
                'paid': False,
                'customer_id': None,
                'subscription_id': None
            }
        return self.user_data[user_id]
    
    def increment_use(self, user_id):
        user = self.check_user(user_id)
        user['uses'] += 1
        return user['uses']
    
    def set_paid(self, user_id, customer_id, subscription_id):
        user = self.check_user(user_id)
        user['paid'] = True
        user['customer_id'] = customer_id
        user['subscription_id'] = subscription_id
        return True

user_manager = UserManager()

class AdvancedMarketingStrategist:
    def __init__(self):
        self.history = []
    
    def generate_strategy(self, product, audience, budget, user_id):
        user = user_manager.check_user(user_id)
        if user['uses'] >= app.config['MAX_FREE_USES'] and not user['paid']:
            return {"error": "Payment required", "payment_required": True}
        
        social_trends = RealTimeData.get_social_media_trends()
        sentiment = RealTimeData.get_market_sentiment(product)
        seo_data = RealTimeData.get_seo_data(product.split()[0])
        
        ai_strategy = self._generate_ai_strategy(product, audience, budget, social_trends, sentiment)
        
        strategy = {
            "social_media": self._enhance_social_strategy(ai_strategy.get('social_media', {}), social_trends),
            "seo": self._enhance_seo_strategy(ai_strategy.get('seo', {}), seo_data),
            "content": self._enhance_content_strategy(ai_strategy.get('content', {}), sentiment),
            "paid_advertising": self._generate_paid_ad_strategy(budget, sentiment),
            "budget_allocation": self._allocate_budget(budget),
            "real_time_insights": {
                "market_sentiment": sentiment,
                "trending_content": social_trends.get('popular_content_types', []),
                "competitor_analysis": self._get_competitor_analysis(product)
            },
            "timestamp": datetime.now().isoformat()
        }
        
        self.history.append({
            "user_id": user_id,
            "timestamp": strategy["timestamp"],
            "product": product,
            "audience": audience,
            "budget": budget,
            "strategy": strategy
        })
        
        user_manager.increment_use(user_id)
        return strategy
    
    # ... [keep all the other methods unchanged] ...

strategist = AdvancedMarketingStrategist()

# HTML Template with Payment UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DACV Pro Marketing Strategist</title>
    <script src="https://js.stripe.com/v3/"></script>
    <style>
        /* [keep all the CSS unchanged] */
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>Pro Marketing Strategist</h1>
            <p class="subtitle">AI-powered marketing strategies with real-time data</p>
        </div>
    </header>
    
    <div class="container">
        <div class="card">
            <div class="tabs">
                <div class="tab active" onclick="openTab('strategy')">Strategy Generator</div>
                <div class="tab" onclick="openTab('history')">My Strategies</div>
                <div class="tab" onclick="openTab('pricing')">Pricing</div>
            </div>
            
            <div id="strategy" class="tab-content active">
                <form id="strategyForm">
                    <div class="form-group">
                        <label for="product">Product/Service Description</label>
                        <textarea id="product" name="product" required placeholder="Describe your product or service in detail..."></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="audience">Target Audience</label>
                        <input type="text" id="audience" name="audience" required placeholder="e.g., Young professionals aged 25-35, tech-savvy">
                    </div>
                    
                    <div class="form-group">
                        <label for="budget">Monthly Marketing Budget ($)</label>
                        <input type="number" id="budget" name="budget" required placeholder="e.g., 5000">
                    </div>
                    
                    <button type="submit" class="btn btn-block" id="generateBtn">
                        <span id="btnText">Generate Marketing Strategy</span>
                    </button>
                </form>
                
                <div id="paymentAlert" class="alert alert-warning hidden">
                    <p>You've used your free strategy. Upgrade to generate more strategies.</p>
                    <button class="btn btn-outline" onclick="openTab('pricing')">View Pricing Plans</button>
                </div>
                
                <div id="result" class="strategy-result hidden">
                    <h2>Your Custom Marketing Strategy</h2>
                    <div id="strategyContent"></div>
                </div>
            </div>
            
            <div id="history" class="tab-content">
                <h2>Your Previous Strategies</h2>
                <div id="historyContent">
                    <p>Loading your strategy history...</p>
                </div>
            </div>
            
            <div id="pricing" class="tab-content">
                <h2>Choose Your Plan</h2>
                <p>Upgrade to generate unlimited marketing strategies with advanced features.</p>
                
                <div class="pricing-plans">
                    <div class="plan">
                        <div class="plan-header">
                            <h3 class="plan-title">Starter</h3>
                            <div class="plan-price">$29<span>/month</span></div>
                            <p>For small businesses and startups</p>
                        </div>
                        <ul class="plan-features">
                            <li>10 strategy generations per month</li>
                            <li>Basic market insights</li>
                            <li>Email support</li>
                        </ul>
                        <button class="btn btn-block" onclick="showPaymentForm('price_1')">Choose Plan</button>
                    </div>
                    
                    <div class="plan">
                        <div class="plan-header">
                            <h3 class="plan-title">Professional</h3>
                            <div class="plan-price">$99<span>/month</span></div>
                            <p>For growing businesses</p>
                        </div>
                        <ul class="plan-features">
                            <li>Unlimited strategy generations</li>
                            <li>Advanced market insights</li>
                            <li>Real-time competitor analysis</li>
                            <li>Priority support</li>
                        </ul>
                        <button class="btn btn-block" onclick="showPaymentForm('price_2')">Choose Plan</button>
                    </div>
                    
                    <div class="plan">
                        <div class="plan-header">
                            <h3 class="plan-title">Enterprise</h3>
                            <div class="plan-price">$299<span>/month</span></div>
                            <p>For agencies and large teams</p>
                        </div>
                        <ul class="plan-features">
                            <li>Unlimited strategy generations</li>
                            <li>All Professional features</li>
                            <li>Team collaboration tools</li>
                            <li>Dedicated account manager</li>
                            <li>API access</li>
                        </ul>
                        <button class="btn btn-block" onclick="showPaymentForm('price_3')">Choose Plan</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div id="paymentModal" class="payment-modal">
        <div class="modal-content">
            <span class="close-modal" onclick="hidePaymentForm()">&times;</span>
            <h2>Complete Your Subscription</h2>
            <p>Enter your payment details to get started</p>
            
            <form id="payment-form">
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" required placeholder="your@email.com">
                </div>
                
                <div class="form-group">
                    <label for="card-element">Credit or Debit Card</label>
                    <div id="card-element">
                        <!-- Stripe Elements will be inserted here -->
                    </div>
                    <div id="card-errors" role="alert"></div>
                </div>
                
                <input type="hidden" id="priceId">
                <button type="submit" class="btn btn-block" id="submitBtn">
                    <span id="submitBtnText">Subscribe Now</span>
                </button>
            </form>
        </div>
    </div>
    
    <script>
        // Initialize Stripe
        const stripe = Stripe('{{ STRIPE_PUBLIC_KEY }}');
        const elements = stripe.elements();
        const cardElement = elements.create('card');
        cardElement.mount('#card-element');
        
        // User session
        let userId = localStorage.getItem('marketingStrategistUserId');
        if (!userId) {
            userId = 'user_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('marketingStrategistUserId', userId);
        }
        
        // Tab navigation
        function openTab(tabName) {
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
            
            document.getElementById(tabName).classList.add('active');
            document.querySelector(`.tab[onclick="openTab('${tabName}')"]`).classList.add('active');
            
            if (tabName === 'history') loadUserHistory();
        }
        
        // Form submission
        document.getElementById('strategyForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const btn = document.getElementById('generateBtn');
            const btnText = document.getElementById('btnText');
            
            btn.disabled = true;
            btnText.innerHTML = '<div class="loading"></div> Generating Strategy...';
            
            fetch('/generate-strategy', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    product: document.getElementById('product').value,
                    audience: document.getElementById('audience').value,
                    budget: parseFloat(document.getElementById('budget').value),
                    user_id: userId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error === "Payment required") {
                    document.getElementById('paymentAlert').classList.remove('hidden');
                    document.getElementById('result').classList.add('hidden');
                } else {
                    document.getElementById('paymentAlert').classList.add('hidden');
                    displayStrategy(data);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error generating strategy. Please try again.');
            })
            .finally(() => {
                btn.disabled = false;
                btnText.textContent = 'Generate Marketing Strategy';
            });
        });
        
        // Display strategy results
        function displayStrategy(strategy) {
            const resultDiv = document.getElementById('result');
            const contentDiv = document.getElementById('strategyContent');
            contentDiv.innerHTML = '';
            
            // [Keep all the displayStrategy code unchanged]
            
            resultDiv.classList.remove('hidden');
            openTab('strategy');
        }
        
        // Payment form handling
        function showPaymentForm(priceId) {
            document.getElementById('priceId').value = priceId;
            document.getElementById('paymentModal').classList.add('active');
            document.getElementById('card-errors').textContent = '';
        }
        
        function hidePaymentForm() {
            document.getElementById('paymentModal').classList.remove('active');
        }
        
        // Handle payment form submission
        const paymentForm = document.getElementById('payment-form');
        paymentForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const submitBtn = document.getElementById('submitBtn');
            const submitBtnText = document.getElementById('submitBtnText');
            const email = document.getElementById('email').value;
            
            if (!email) {
                document.getElementById('card-errors').textContent = 'Please enter your email';
                return;
            }
            
            submitBtn.disabled = true;
            submitBtnText.innerHTML = '<div class="loading"></div> Processing...';
            
            try {
                // Create payment method
                const { paymentMethod, error: pmError } = await stripe.createPaymentMethod({
                    type: 'card',
                    card: cardElement,
                    billing_details: { email: email }
                });
                
                if (pmError) throw pmError;
                
                // Create subscription
                const response = await fetch('/create-subscription', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        payment_method_id: paymentMethod.id,
                        price_id: document.getElementById('priceId').value,
                        user_id: userId,
                        email: email
                    })
                });
                
                const data = await response.json();
                
                if (!response.ok) {
                    throw new Error(data.error || 'Subscription creation failed');
                }
                
                // Confirm the payment
                const { paymentIntent, error: confirmError } = await stripe.confirmCardPayment(
                    data.client_secret, {
                        payment_method: paymentMethod.id
                    }
                );
                
                if (confirmError) throw confirmError;
                
                if (paymentIntent.status === 'succeeded') {
                    hidePaymentForm();
                    
                    // Show success message
                    const alertDiv = document.createElement('div');
                    alertDiv.className = 'alert alert-info';
                    alertDiv.innerHTML = `
                        <p>Payment successful! You can now generate unlimited strategies.</p>
                        <p>Subscription ID: ${data.subscription_id}</p>
                    `;
                    document.getElementById('strategy').prepend(alertDiv);
                    
                    document.getElementById('paymentAlert').classList.add('hidden');
                    
                    // Refresh user status
                    fetch('/check-user-usage?user_id=' + userId)
                        .then(response => response.json())
                        .then(data => {
                            if (data.paid) {
                                document.getElementById('paymentAlert').classList.add('hidden');
                            }
                        });
                } else {
                    throw new Error('Payment processing failed');
                }
            } catch (error) {
                console.error('Payment error:', error);
                document.getElementById('card-errors').textContent = error.message || 'Payment failed. Please try again.';
            } finally {
                submitBtn.disabled = false;
                submitBtnText.textContent = 'Subscribe Now';
            }
        });
        
        // Load history on page load
        document.addEventListener('DOMContentLoaded', function() {
            if (window.location.hash === '#history') openTab('history');
            if (window.location.hash === '#pricing') openTab('pricing');
            
            // Check user usage
            fetch('/check-user-usage?user_id=' + userId)
                .then(response => response.json())
                .then(data => {
                    if (data.uses_left <= 0 && !data.paid) {
                        document.getElementById('paymentAlert').classList.remove('hidden');
                    }
                });
        });
    </script>
</body>
</html>
"""

# Flask Routes
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, STRIPE_PUBLIC_KEY=app.config['STRIPE_PUBLIC_KEY'])

@app.route('/generate-strategy', methods=['POST'])
@limiter.limit("5 per minute")
def generate_strategy():
    data = request.json
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({"error": "User ID required"}), 400
    
    strategy = strategist.generate_strategy(
        data['product'],
        data['audience'],
        data['budget'],
        user_id
    )
    
    return jsonify(strategy)

@app.route('/get-user-history')
def get_user_history():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID required"}), 400
    
    history = strategist.get_user_history(user_id)
    return jsonify(history)

@app.route('/check-user-usage')
def check_user_usage():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "User ID required"}), 400
    
    user = user_manager.check_user(user_id)
    return jsonify({
        "uses_left": max(0, app.config['MAX_FREE_USES'] - user['uses']),
        "paid": user['paid']
    })

@app.route('/create-subscription', methods=['POST'])
def create_subscription():
    data = request.json
    user_id = data.get('user_id')
    
    try:
        # Create customer in Stripe
        customer = stripe.Customer.create(
            email=data['email'],
            payment_method=data['payment_method_id'],
            invoice_settings={
                'default_payment_method': data['payment_method_id']
            }
        )
        
        # Create subscription
        subscription = stripe.Subscription.create(
            customer=customer.id,
            items=[{'price': data['price_id']}],
            expand=['latest_invoice.payment_intent'],
            payment_behavior='default_incomplete',
            payment_settings={
                'save_default_payment_method': 'on_subscription'
            }
        )
        
        # Confirm the payment intent
        payment_intent = stripe.PaymentIntent.confirm(
            subscription.latest_invoice.payment_intent.id,
            payment_method=data['payment_method_id']
        )
        
        if payment_intent.status == 'succeeded':
            # Mark user as paid
            user_manager.set_paid(user_id, customer.id, subscription.id)
            return jsonify({
                "success": True,
                "subscription_id": subscription.id,
                "client_secret": payment_intent.client_secret
            })
        else:
            return jsonify({
                "error": "Payment failed",
                "message": payment_intent.last_payment_error or "Payment could not be processed"
            }), 400
            
    except stripe.error.CardError as e:
        return jsonify({
            "error": "Card error",
            "message": e.user_message
        }), 400
    except stripe.error.StripeError as e:
        return jsonify({
            "error": "Stripe error",
            "message": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "error": "Server error",
            "message": str(e)
        }), 500

# Webhook for Stripe events (for production)
@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    event = None
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, app.config['STRIPE_WEBHOOK_SECRET']
        )
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except stripe.error.SignatureVerificationError as e:
        return jsonify({'error': str(e)}), 400
    
    # Handle subscription events
    if event['type'] == 'invoice.payment_succeeded':
        # Handle successful recurring payment
        pass
    elif event['type'] == 'customer.subscription.deleted':
        # Handle subscription cancellation
        pass
    
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')