from flask import Flask, jsonify

app = Flask(__name__)

products = [
    {
        "id": 1,
        "name": "Noxen Black Hoodie",
        "price": 999,
        "description": "Premium black hoodie with Never Settle attitude.",
        "sizes": ["S", "M", "L", "XL"],
        "stock": 25,
        "image": "hoodie-black.svg"
    },
    {
        "id": 2,
        "name": "Noxen Grey Hoodie",
        "price": 1099,
        "description": "Soft grey hoodie for daily comfort and streetwear style.",
        "sizes": ["M", "L", "XL"],
        "stock": 18,
        "image": "hoodie-grey.svg"
    },
    {
        "id": 3,
        "name": "Noxen Blue Hoodie",
        "price": 1199,
        "description": "Blue hoodie with clean streetwear design.",
        "sizes": ["S", "M", "L", "XL"],
        "stock": 20,
        "image": "hoodie-blue.svg"
    },
    {
        "id": 4,
        "name": "Noxen Red Hoodie",
        "price": 1199,
        "description": "Bold red hoodie for confident everyday style.",
        "sizes": ["S", "M", "L", "XL"],
        "stock": 16,
        "image": "hoodie-red.svg"
    },
    {
        "id": 5,
        "name": "Noxen White Hoodie",
        "price": 1299,
        "description": "Clean white hoodie with premium comfort.",
        "sizes": ["M", "L", "XL"],
        "stock": 14,
        "image": "hoodie-white.svg"
    }
]


@app.route("/")
def home():
    return jsonify({
        "service": "Noxen Product Service",
        "status": "running"
    })


@app.route("/products")
def get_products():
    return jsonify(products)


@app.route("/products/<int:product_id>")
def get_product(product_id):
    for product in products:
        if product["id"] == product_id:
            return jsonify(product)

    return jsonify({
        "error": "Product not found"
    }), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)