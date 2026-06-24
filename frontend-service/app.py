from flask import Flask, render_template, request, redirect, session
import requests

app = Flask(__name__)
app.secret_key = "noxen-secret-key"

PRODUCT_SERVICE_URL = "http://product-service:5001"
ORDER_SERVICE_URL = "http://order-service:5002"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/products")
def products():
    response = requests.get(f"{PRODUCT_SERVICE_URL}/products")
    products = response.json()
    return render_template("products.html", products=products)


@app.route("/add-to-cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    cart = session.get("cart", [])

    item = {
        "product_id": product_id,
        "size": request.form.get("size", "M"),
        "quantity": int(request.form.get("quantity", 1))
    }

    cart.append(item)
    session["cart"] = cart

    return redirect("/cart")


@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    return render_template("cart.html", cart=cart_items)


@app.route("/checkout")
def checkout():
    return render_template("checkout.html")


@app.route("/order", methods=["POST"])
def order():
    order_data = {
        "customer_name": request.form.get("customer_name"),
        "phone": request.form.get("phone"),
        "email": request.form.get("email"),
        "product_id": int(request.form.get("product_id", 1)),
        "size": request.form.get("size", "M"),
        "quantity": int(request.form.get("quantity", 1)),
        "address": request.form.get("address", "")
    }

    requests.post(f"{ORDER_SERVICE_URL}/orders", json=order_data)
    return redirect("/success")


@app.route("/success")
def success():
    return render_template("success.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)