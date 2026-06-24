# Noxen Hoodie App

A clean Flask starter application for selling hoodies online.

## Pages

- `/` - Home page
- `/products` - Products page
- `/login` - Customer delivery/order details page
- `/submit-order` - Saves order to SQLite database

## Run locally

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
# OR on Windows:
# venv\Scripts\activate

pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Orders

Orders are stored in:

```text
orders.db
```

## Next improvements

- Add real product images in `static/images`
- Add admin page to view orders
- Add Razorpay/Stripe payment gateway
- Add WhatsApp or email notification for new order
- Deploy on EC2 / Render / Railway / Kubernetes
