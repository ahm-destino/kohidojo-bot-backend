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
businessInfo = {
  "brand": {
    "name": "Kohi Dojo",
    "description": "Welcome to KOHI DOJO ☕✨ — where every cup tells a story. We’re more than a café — we’re a cozy corner for coffee lovers, creatives, and community, located in Aba, Abia State.",
    "location": "Aba, Abia State, Nigeria",
    "tone": "Friendly, creative, and warm — like a skilled barista talking to regulars."
  },

  "faqs": [
    {
      "question": "Where is Kohi Dojo located?",
      "answer": "We are located in Aba, Abia State, Nigeria. You can visit our cozy shop or order online through our website."
    },
    {
      "question": "Do you offer home delivery?",
      "answer": "Yes! We deliver within Aba city and nearby areas. Simply place an order online and select your delivery option."
    },
    {
      "question": "What makes your coffee special?",
      "answer": "We source our beans from local and African farmers, roast them fresh weekly, and brew every cup with precision and love."
    },
    {
      "question": "Do you have non-coffee options?",
      "answer": "Absolutely — we serve teas, smoothies, matcha, pastries, and other non-coffee favorites."
    }
  ],

  "products": [
    {
      "name": "Espresso",
      "description": "A bold, rich shot of pure coffee flavor for those who love intensity.",
      "price": "₦1500",
      "purchase_link": "https://kohidojo.com/products/espresso"
    },
    {
      "name": "Iced Caramel Latte",
      "description": "Smooth espresso blended with milk, ice, and sweet caramel drizzle.",
      "price": "₦2500",
      "purchase_link": "https://kohidojo.com/products/iced-caramel-latte"
    },
    {
      "name": "Matcha Latte",
      "description": "Creamy and earthy — made from premium Japanese matcha powder and steamed milk.",
      "price": "₦2700",
      "purchase_link": "https://kohidojo.com/products/matcha-latte"
    },
    {
      "name": "Café Mocha",
      "description": "A cozy mix of espresso, chocolate, and milk — perfect for indulgent moments.",
      "price": "₦2800",
      "purchase_link": "https://kohidojo.com/products/cafe-mocha"
    },
    {
      "name": "Croissant",
      "description": "Golden and buttery French pastry that pairs perfectly with any coffee.",
      "price": "₦1200",
      "purchase_link": "https://kohidojo.com/products/croissant"
    }
  ],

  "groups": [
    {
      "name": "Kohi Dojo Creatives Circle",
      "description": "A space where local artists, designers, and thinkers meet over coffee to share ideas.",
      "join_link": "https://kohidojo.com/groups/creatives-circle"
    },
    {
      "name": "Coffee Lovers Club",
      "description": "Exclusive members-only club with discounts, early product launches, and barista lessons.",
      "join_link": "https://kohidojo.com/groups/coffee-lovers-club"
    }
  ]
}


SYSTEM_PROMPT = f'You are the official virtual assistant of Kohi Dojo — a cozy coffee shop and creative hub in Aba, Nigeria.Your tone is friendly, conversational, and community-driven.Answer questions based on the provided context but only check this if a user asks for it (menu, FAQ, or group info) check them out here {businessInfo}. If the user asks about a product, include its purchase link.'
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
