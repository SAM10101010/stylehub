from flask import Flask, render_template, request, jsonify
import mysql.connector

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
    return render_template("categories.html")

# Route to render the cart page
@app.route("/cart")
def cart():
    return render_template("cart.html")


# Fetch all categories for dropdown (optional)
@app.route("/categories")
def get_categories():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categories")
        categories = cursor.fetchall()
        return jsonify(categories)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cursor.close()
        connection.close()

# Fetch most popular products
@app.route("/most-popular")
def get_most_popular():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM most_popular")
        popular_products = cursor.fetchall()
        return jsonify(popular_products)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cursor.close()
        connection.close()

# Fetch products by category ID
@app.route("/products")
def get_products():
    category_id = request.args.get("category_id", type=int)
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        if category_id:
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
        cursor.close()
        connection.close()

# Fetch product details by ID (for cart display)
@app.route("/product/<int:product_id>")
def get_product_by_id(product_id):
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
        cursor.close()
        connection.close()

if __name__ == "__main__":
    app.run(debug=True)
