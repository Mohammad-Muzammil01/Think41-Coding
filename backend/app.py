from flask import Flask, jsonify, request
from flask_cors import CORS

import pandas as pd
import sqlite3
import os
from dotenv import load_dotenv
import requests


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = Flask(__name__)
CORS(app)

DB_NAME = 'data.db'

# Load CSV files
orders_df = pd.read_csv("data/orders.csv")
products_df = pd.read_csv("data/products.csv")

def query_groq_llm(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "system", "content": "You're a helpful assistant for an e-commerce platform."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

# ---------- Conversation Schema Logic ----------

def get_or_create_user(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    if user:
        user_id = user[0]
    else:
        cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
        user_id = cursor.lastrowid
        conn.commit()
    conn.close()
    return user_id

def create_session(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessions (user_id) VALUES (?)", (user_id,))
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_id

@app.route("/start_session", methods=["POST"])
def start_session():
    data = request.get_json()
    username = data.get("username")
    if not username:
        return jsonify({"error": "Username is required"}), 400

    user_id = get_or_create_user(username)
    session_id = create_session(user_id)
    return jsonify({"session_id": session_id})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    session_id = data.get("session_id")
    user_input = data.get("message")

    if not session_id or not user_input:
        return jsonify({"error": "Session ID and message required"}), 400

    # 🔥 Generate response using Groq LLM
    prompt = f"""User said: '{user_input}'. 
You are a helpful assistant for an e-commerce platform. 
If you don't have enough information, ask clarifying questions. 
Otherwise, give a helpful response using your knowledge or the e-commerce data."""
    
    bot_response = query_groq_llm(prompt)

    # Save the conversation to the DB
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO conversations (session_id, user_input, bot_response)
        VALUES (?, ?, ?)
    ''', (session_id, user_input, bot_response))
    conn.commit()
    conn.close()

    return jsonify({"response": bot_response})

@app.route("/conversations/<int:session_id>", methods=["GET"])
def get_conversations(session_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_input, bot_response, timestamp FROM conversations WHERE session_id = ? ORDER BY timestamp ASC", (session_id,))
    rows = cursor.fetchall()
    conn.close()
    return jsonify([
        {"user": row[0], "bot": row[1], "timestamp": row[2]} for row in rows
    ])

# ---------- CSV-based E-commerce Endpoints ----------

@app.route('/')
def home():
    return "E-commerce Chatbot API is running"

@app.route('/api/top-products')
def top_products():
    top = orders_df.groupby('product_id')['quantity'].sum().sort_values(ascending=False).head(5)
    top = top.reset_index()
    merged = pd.merge(top, products_df, on='product_id')[['product_name', 'quantity']]
    return jsonify(merged.to_dict(orient='records'))

@app.route('/api/order-status/<order_id>')
def order_status(order_id):
    row = orders_df[orders_df['order_id'] == int(order_id)]
    if row.empty:
        return jsonify({'error': 'Order ID not found'}), 404
    return jsonify({
        'order_id': order_id,
        'status': row.iloc[0]['status'],
        'order_date': row.iloc[0]['order_date']
    })

@app.route('/api/stock/<product_name>')
def product_stock(product_name):
    row = products_df[products_df['product_name'].str.lower() == product_name.lower()]
    if row.empty:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify({
        'product_name': row.iloc[0]['product_name'],
        'stock': int(row.iloc[0]['stock'])
    })

if __name__ == '__main__':
    app.run(debug=True)
