from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
app.secret_key = "change-this-secret-key-before-production"
DB_PATH = Path(__file__).parent / "orders.db"

PRODUCTS = [
    {
        "id": "noxen-core-black",
        "name": "Noxen Core Black Hoodie",
        "price": 1499,
        "tag": "Best Seller",
        "image": "hoodie-black.svg",
        "color": "Black",
        "description": "Premium heavy fleece hoodie for daily streetwear.",
        "quality": "320 GSM cotton fleece, soft brushed inner layer, ribbed cuffs, kangaroo pocket, durable stitching.",
    },
    {
        "id": "noxen-ice-white",
        "name": "Noxen Ice White Hoodie",
        "price": 1599,
        "tag": "Clean Look",
        "image": "hoodie-white.svg",
        "color": "White",
        "description": "Minimal white hoodie with a clean premium look.",
        "quality": "Soft cotton blend, anti-shrink finish, double-stitched seams, breathable winter comfort.",
    },
    {
        "id": "noxen-storm-grey",
        "name": "Noxen Storm Grey Hoodie",
        "price": 1399,
        "tag": "Everyday Pick",
        "image": "hoodie-grey.svg",
        "color": "Grey",
        "description": "Comfortable grey hoodie for gym, travel, and daily wear.",
        "quality": "Mid-heavy fleece, relaxed fit, smooth outer surface, warm inner lining, strong drawstrings.",
    },
    {
        "id": "noxen-fire-red",
        "name": "Noxen Fire Red Hoodie",
        "price": 1699,
        "tag": "Bold Color",
        "image": "hoodie-red.svg",
        "color": "Red",
        "description": "Eye-catching red hoodie built for a bold streetwear style.",
        "quality": "Color-lock fabric, premium fleece, reinforced pocket, soft hood lining, long-lasting finish.",
    },
    {
        "id": "noxen-royal-blue",
        "name": "Noxen Royal Blue Hoodie",
        "price": 1699,
        "tag": "Limited Drop",
        "image": "hoodie-blue.svg",
        "color": "Blue",
        "description": "Royal blue hoodie with strong streetwear energy.",
        "quality": "Premium cotton blend, warm fleece feel, oversized comfort, durable zipper-free pullover design.",
    },
]


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                pincode TEXT NOT NULL,
                product_id TEXT,
                product_name TEXT,
                size TEXT,
                quantity INTEGER,
                price INTEGER,
                payment_method TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        # Add missing columns when upgrading an old local DB.
        existing_cols = [row[1] for row in conn.execute("PRAGMA table_info(orders)").fetchall()]
        for col, col_type in [("price", "INTEGER"), ("payment_method", "TEXT")]:
            if col not in existing_cols:
                conn.execute(f"ALTER TABLE orders ADD COLUMN {col} {col_type}")
        conn.commit()


def get_product(product_id):
    return next((product for product in PRODUCTS if product["id"] == product_id), None)


def get_cart():
    return session.get("cart", [])


def save_cart(cart):
    session["cart"] = cart
    session.modified = True


@app.route("/")
def home():
    return render_template("index.html", products=PRODUCTS[:3], cart_count=len(get_cart()))


@app.route("/products")
def products():
    return render_template("products.html", products=PRODUCTS, cart_count=len(get_cart()))


@app.route("/add-to-cart/<product_id>", methods=["POST"])
def add_to_cart(product_id):
    product = get_product(product_id)
    if not product:
        return redirect(url_for("products"))

    cart = get_cart()
    item = next((i for i in cart if i["product_id"] == product_id), None)
    if item:
        item["quantity"] += 1
    else:
        cart.append({
            "product_id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "image": product["image"],
            "size": "M",
            "quantity": 1,
        })
    save_cart(cart)
    return redirect(url_for("cart"))


@app.route("/cart", methods=["GET", "POST"])
def cart():
    cart_items = get_cart()
    if request.method == "POST":
        updated = []
        for item in cart_items:
            product_id = item["product_id"]
            qty = int(request.form.get(f"quantity_{product_id}", item["quantity"]))
            if qty <= 0:
                continue
            item["quantity"] = qty
            item["size"] = request.form.get(f"size_{product_id}", item.get("size", "M"))
            updated.append(item)
        save_cart(updated)
        return redirect(url_for("checkout"))

    total = sum(item["price"] * item["quantity"] for item in cart_items)
    return render_template("cart.html", cart=cart_items, total=total, cart_count=len(cart_items))


@app.route("/remove-from-cart/<product_id>")
def remove_from_cart(product_id):
    cart = [item for item in get_cart() if item["product_id"] != product_id]
    save_cart(cart)
    return redirect(url_for("cart"))


@app.route("/checkout")
def checkout():
    cart_items = get_cart()
    if not cart_items:
        return redirect(url_for("products"))
    total = sum(item["price"] * item["quantity"] for item in cart_items)
    return render_template("checkout.html", cart=cart_items, total=total, cart_count=len(cart_items))


@app.route("/submit-order", methods=["POST"])
def submit_order():
    cart_items = get_cart()
    if not cart_items:
        return redirect(url_for("products"))

    customer = {
        "full_name": request.form.get("full_name", "").strip(),
        "phone": request.form.get("phone", "").strip(),
        "email": request.form.get("email", "").strip(),
        "address": request.form.get("address", "").strip(),
        "city": request.form.get("city", "").strip(),
        "pincode": request.form.get("pincode", "").strip(),
        "payment_method": request.form.get("payment_method", "Cash on Delivery"),
        "created_at": datetime.utcnow().isoformat(timespec="seconds"),
    }

    required_fields = ["full_name", "phone", "email", "address", "city", "pincode"]
    if not all(customer[field] for field in required_fields):
        return redirect(url_for("checkout"))

    with sqlite3.connect(DB_PATH) as conn:
        for item in cart_items:
            conn.execute(
                """
                INSERT INTO orders (
                    full_name, phone, email, address, city, pincode,
                    product_id, product_name, size, quantity, price,
                    payment_method, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    customer["full_name"], customer["phone"], customer["email"],
                    customer["address"], customer["city"], customer["pincode"],
                    item["product_id"], item["name"], item["size"], item["quantity"],
                    item["price"], customer["payment_method"], customer["created_at"]
                )
            )
        conn.commit()

    order = {**customer, "items": cart_items, "total": sum(i["price"] * i["quantity"] for i in cart_items)}
    save_cart([])
    return render_template("success.html", order=order, cart_count=0)


@app.route("/login")
def login():
    # Old URL kept working; now login/details happen in checkout after cart.
    return redirect(url_for("checkout") if get_cart() else url_for("products"))


@app.route("/admin/orders")
def admin_orders():
    init_db()
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    return render_template("admin.html", orders=rows, cart_count=len(get_cart()))


init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
