import os
import groq
from flask import Flask, request, session, jsonify
from datetime import timedelta
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

app.secret_key = '12345'
app.permanent_session_lifetime = timedelta(minutes = 5)


API_KEY = os.getenv("GROQ_API_KEY")
print(f"Loaded API Key: {API_KEY}")

client = groq.Client(api_key=API_KEY)
businessInfo = """
brand:
  name: Kohi Dojo
  description: |
    Welcome to KOHI DOJO ☕🍜🔥 — your neighborhood hub for comfort food, creativity, and community.  
    We’re more than a café — we’re a hybrid spot where coffee lovers, food explorers, and everyday hustlers find their perfect pick-me-up.  
    From handcrafted coffee and pastries to Japanese-inspired meals, shawarma, and fresh snacks, we serve flavor for every mood.
  location: Aba, Abia State, Nigeria
  tone: Friendly, creative, and warm — like a skilled customer Representative talking to vip customers.

faqs:
  - question: Where is Kohi Dojo located?
    answer: We are located in Aba, Abia State, Nigeria. You can visit our cozy shop or order online through our website.
  - question: Do you offer home delivery?
    answer: Yes! We deliver within Aba city and nearby areas. Simply place an order online and select your delivery option.
  - question: What makes your coffee special?
    answer: We source our beans from local and African farmers, roast them fresh weekly, and brew every cup with precision and love.
  - question: Do you have non-coffee options?
    answer: Absolutely — we serve teas, smoothies, matcha, pastries, and other non-coffee favorites.

products:
  - category: Coffee
    name: Blackie
    description: Freshly brewed hot black coffee — simple, strong, no milk, no stress.
    price: "₦500"
    purchase_link: https://kohidojo.com/products/blackie

  - category: Coffee
    name: Kohi Hot
    description: Smooth hot coffee with milk. Lure comfort in a cup.
    price: "₦500 / ₦1000"
    purchase_link: https://kohidojo.com/products/kohi-hot

  - category: Coffee
    name: Kohi Cold
    description: Chilled coffee served cold and refreshing. Perfect for the heat.
    price: "₦500 / ₦1000"
    purchase_link: https://kohidojo.com/products/kohi-cold

  - category: Kohi Fresh
    name: Sunny Blend
    description: Banana • Watermelon • Apple — bright, light, and morning-sweet.
    price: "₦1200"
    purchase_link: https://kohidojo.com/products/sunny-blend

  - category: Kohi Fresh
    name: Island Flow
    description: Banana • Pineapple • Apple — tropical, smooth, and sunny calm.
    price: "₦1200"
    purchase_link: https://kohidojo.com/products/island-flow

  - category: Kohi Fresh
    name: Loja’s Bowl
    description: Watermelon • Pineapple • Apple • Banana — a colorful fruit rush that feels like home.
    price: "₦1500"
    purchase_link: https://kohidojo.com/products/lojas-bowl

  - category: Shawarma
    name: Chickie
    description: Tender grilled chicken wrapped with fresh veggies and creamy sauce.
    price: "₦1000 / ₦1500 / ₦2000"
    purchase_link: https://kohidojo.com/products/chickie

  - category: Shawarma
    name: Beefie
    description: Juicy beef shawarma layered with our house spice mix and garlic cream.
    price: "₦1500 / ₦2000"
    purchase_link: https://kohidojo.com/products/beefie

  - category: Shawarma
    name: Mixie (Special)
    description: The best of both worlds — chicken + beef with double sauce love.
    price: "₦3000"
    purchase_link: https://kohidojo.com/products/mixie-special

  - category: Shawarma
    name: Mini Shawas
    description: Small, quick bite version of our classics. Same flavor, smaller wrap.
    price: "₦1000"
    purchase_link: https://kohidojo.com/products/mini-shawas


groups:
  - Kohi Dojo Creatives Circle | A space for local creatives to share ideas. | https://kohidojo.com/groups/creatives-circle
  - Coffee Lovers Club | Members-only club with discounts and barista lessons. | https://kohidojo.com/groups/coffee-lovers-club
"""



SYSTEM_PROMPT = f'You are the official virtual assistant of Kohi Dojo — a cozy coffee shop and creative hub in Aba, Nigeria.Your tone is friendly, conversational, and community-driven.You must not answer any question outside this business. Answer questions based on the provided context but only check this if a user asks for it (menu, FAQ, or group info) check them out here {businessInfo}. If the user asks about a product, include its purchase link.'
messages = { 'role' : 'system',
          'content': SYSTEM_PROMPT 
}



def processMessage():
    kohidojo_chatbot = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages= session['messages'],
    )
    session['messages'].append({'role': 'assistant',
                                'content' : kohidojo_chatbot.choices[0].message.content
                                })
    print(session['messages'])
    return jsonify(kohidojo_chatbot.choices[0].message.content)




@app.route('/get-users-prompt', methods=['POST'])
def usersPrompt():
    session.permanent = True
    userInput = request.get_json()
    userPrompt = userInput
    session['messages'] = [messages]
    session['messages'].append(
        {
        'role' : 'user',
        'content' : userPrompt
        }
    )
    return processMessage(), 200
