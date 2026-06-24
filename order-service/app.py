from flask import Flask, request, jsonify

app = Flask(__name__)

orders = []

@app.route("/")
def home():
    return jsonify({
        "service": "Noxen Order Service",
        "status": "running"
    })

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    order = {
        "id": len(orders) + 1,
        "customer_name": data.get("customer_name"),
        "phone": data.get("phone"),
        "email": data.get("email"),
        "product_id": data.get("product_id"),
        "size": data.get("size"),
        "quantity": data.get("quantity"),
        "address": data.get("address")
    }

    orders.append(order)

    return jsonify({
        "message": "Order created successfully",
        "order": order
    }), 201

@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify(orders)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)