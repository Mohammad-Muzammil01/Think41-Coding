from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Load CSV files
orders_df = pd.read_csv("data/orders.csv")
products_df = pd.read_csv("data/products.csv")

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
