from flask import Flask, render_template, request

app = Flask(__name__)

hoodies = [
    {
        "id": 1,
        "name": "Black Phantom Hoodie",
        "price": "₹1,999",
        "sizes": ["S", "M", "L", "XL"],
        "material": "Premium cotton fleece",
        "description": "Minimal black oversized hoodie for everyday streetwear.",
        "image": "hoodie1.png"
    },
    {
        "id": 2,
        "name": "Urban Ash Hoodie",
        "price": "₹1,799",
        "sizes": ["S", "M", "L", "XL"],
        "material": "Soft brushed cotton",
        "description": "Grey clean hoodie made for comfort and daily wear.",
        "image": "hoodie2.png"
    },
    {
        "id": 3,
        "name": "Midnight Oversized Hoodie",
        "price": "₹2,199",
        "sizes": ["M", "L", "XL", "XXL"],
        "material": "Heavyweight cotton blend",
        "description": "Bold oversized hoodie with premium winter comfort.",
        "image": "hoodie3.png"
    },
    {
        "id": 4,
        "name": "Storm Rider Hoodie",
        "price": "₹2,499",
        "sizes": ["M", "L", "XL"],
        "material": "Thick winter fleece",
        "description": "Dark hoodie built for cold weather and strong style.",
        "image": "hoodie4.png"
    },
    {
        "id": 5,
        "name": "Noxen Core Hoodie",
        "price": "₹1,599",
        "sizes": ["S", "M", "L"],
        "material": "Cotton polyester blend",
        "description": "Simple NOXEN logo hoodie for a clean premium look.",
        "image": "hoodie5.png"
    }
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/catalog")
def catalog():
    return render_template("catalog.html", hoodies=hoodies)

@app.route("/product/<int:product_id>")
def product(product_id):
    selected = next((h for h in hoodies if h["id"] == product_id), None)

    if selected is None:
        return "Product not found", 404

    return render_template("product.html", hoodie=selected)

@app.route("/place-order", methods=["POST"])
def place_order():
    order = {
        "product_name": request.form.get("product_name"),
        "price": request.form.get("price"),
        "size": request.form.get("size"),
        "customer_name": request.form.get("customer_name"),
        "email": request.form.get("email"),
        "phone": request.form.get("phone"),
        "address": request.form.get("address"),
        "payment": request.form.get("payment")
    }

    return render_template("order_success.html", order=order)

if __name__ == "__main__":
    app.run(debug=True)