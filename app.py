from flask import Flask, render_template, request, jsonify
import mysql.connector
import qrcode
from PIL import Image

app = Flask(__name__)

# MySQL Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "12345",
    "database": "stylehub"
}

# Home route to render the landing page
@app.route("/")
def index():
    return render_template("index.html")

# Route to render the category page
@app.route("/categories.html")
def categories():
    search_query = request.args.get("search", default=None, type=str)
    return render_template("categories.html", search_query=search_query)

# Route to render the cart page
@app.route("/cart.html")
def cart():
    return render_template("cart.html")

@app.route("/blog.html")
def blog():
    return render_template("blog.html")

@app.route("/contact.html")
def contact():
    return render_template("contact.html")

# Payment Route
@app.route("/payment")
def payment():
    total_amount = request.args.get("amount", default=0, type=float)
    final_amount = total_amount * 85  # Multiply by 85
    upi_id = "singlasanyam94-1@oksbi"

    # Generate UPI payment link
    upi_link = f"upi://pay?pa={upi_id}&pn=StyleHub&am={final_amount:.2f}&cu=INR"

    # Generate QR code for the final amount
    qr = qrcode.make(upi_link)
    qr.save("static/qr_code.png")

    return render_template("payment.html", total_amount=final_amount)

@app.route("/thankyou.html")
def thankyou():
    return render_template("thankyou.html")

@app.route("/success.html")
def success():
    return render_template("success.html")

# Fetch all categories for dropdown
@app.route("/categories")
def get_categories():
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
        return jsonify(categories)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Fetch products based on category ID or search query
@app.route("/products")
def get_products():
    connection = None
    cursor = None
    category_id = request.args.get("category_id", type=int)
    search_query = request.args.get("search", type=str)

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        if search_query:
            query = "SELECT * FROM products WHERE name LIKE %s"
            cursor.execute(query, (f"%{search_query}%",))
        elif category_id:
            query = "SELECT * FROM products WHERE category_id = %s"
            cursor.execute(query, (category_id,))
        else:
            query = "SELECT * FROM products"
            cursor.execute(query)

        products = cursor.fetchall()
        return jsonify(products)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Fetch most popular products
@app.route("/most-popular")
def get_most_popular():
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM most_popular")
        popular_products = cursor.fetchall()
        return jsonify(popular_products)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Fetch product details by ID
@app.route("/product/<int:product_id>")
def get_product_by_id(product_id):
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM products WHERE id = %s"
        cursor.execute(query, (product_id,))
        product = cursor.fetchone()

        if product:
            return jsonify(product)
        else:
            return jsonify({"error": "Product not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    app.run(debug=True)
