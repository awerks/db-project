from flask import Flask, render_template, request, send_from_directory, jsonify
from os import environ
import pymysql

# from sshtunnel import SSHTunnelForwarder

app = Flask(__name__, static_url_path="/static")

# testing purposes

# SSH_HOST = environ.get("SSH_HOST")
# SSH_USERNAME =  environ.get("SSH_USERNAME")
# SSH_PASSWORD = environ.get("SSH_PASSWORD")

MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = environ.get("MYSQL_USER")
MYSQL_PASSWORD = environ.get("MYSQL_PASSWORD")
MYSQL_DB = environ.get("MYSQL_DB")
LOCAL_PORT = 49868


def connect_db():
    # server = SSHTunnelForwarder(
    #     (SSH_HOST, 22),
    #     ssh_username=SSH_USERNAME,
    #     ssh_password=SSH_PASSWORD,
    #     remote_bind_address=(MYSQL_HOST, MYSQL_PORT),
    # )c
    # server.start()

    connection = pymysql.connect(
        host=MYSQL_HOST,
        port=LOCAL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
    )
    return connection  # , server


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/maintenance")
def maintenance():
    return send_from_directory("static", "maintenance.html")


@app.route("/search")
def searhh():
    return send_from_directory("static", "search.html")


@app.route("/imprint")
def imprint():
    return send_from_directory("static", "imprint.html")


@app.route("/search_fields", methods=["POST"])
def search():
    form_data = request.form.to_dict()

    search_criteria = {k: v for k, v in form_data.items() if v}

    print("Search Criteria:", search_criteria)

    results = []
    if "product_id" in search_criteria:
        results = [
            {"id": 1, "name": "Eco-friendly T-shirt", "price": 19.99},
            {"id": 2, "name": "Reusable Water Bottle", "price": 9.99},
        ]
    elif "username" in search_criteria:
        results = [
            {"id": 1, "username": "john_doe", "email": "john@example.com"},
            {"id": 2, "username": "jane_doe", "email": "jane@example.com"},
        ]

    return render_template("search_results.html", results=results)


@app.route("/login", methods=["GET"])
def admin():
    return send_from_directory("static", "login.html")


@app.route("/authenticate", methods=["POST"])
def admin_authenticate():
    form_username = request.form.get("username")
    form_password = request.form.get("password")
    connection = connect_db()
    with connection.cursor() as cursor:
        cursor.execute("SELECT username, password FROM User WHERE role = 'Admin'")
        result = cursor.fetchone()
        if result:
            admin_username, admin_password = result
            if form_username == admin_username and form_password == admin_password:
                return send_from_directory("static", "maintenance.html")
            else:
                return jsonify({"message": "Invalid username or password."}), 401
        else:
            return jsonify({"message": "No admin user found."}), 401


@app.route("/detail/<int:id>", methods=["GET"])
def detail(id):
    result = {
        "id": id,
        "name": "Eco-friendly T-shirt",
        "price": 19.99,
        "description": "A soft, organic cotton t-shirt.",
        "category": "Clothing",
        "sustainability": 85,
        "carbon_footprint": 12,
    }

    return render_template("details.html", result=result)


@app.route("/product_input")
def product_input():
    fields = [
        {"id": "name", "name": "name", "label": "Product Name", "type": "text", "required": True},
        {"id": "price", "name": "price", "label": "Price", "type": "number", "required": True},
    ]
    return render_template("input_template.html", title="Product", form_action="/submit_product", fields=fields)


@app.route("/user_input")
def user_input():
    fields = [
        {"id": "username", "name": "username", "label": "Username", "type": "text", "required": True},
        {"id": "email", "name": "email", "label": "Email", "type": "email", "required": True},
        {
            "id": "role",
            "name": "role",
            "label": "Role",
            "type": "select",
            "required": True,
            "options": [{"value": "Customer", "label": "Customer"}, {"value": "EcoReviewer", "label": "EcoReviewer"}],
        },
    ]
    return render_template("input_template.html", title="User", form_action="/submit_user", fields=fields)


@app.route("/category_input")
def category_input():
    fields = [
        {"id": "name", "name": "name", "label": "Category Name", "type": "text", "required": True},
        {"id": "description", "name": "description", "label": "Description", "type": "text", "required": True},
        {
            "id": "category_type",
            "name": "category_type",
            "label": "Category Type",
            "type": "select",
            "required": True,
            "options": [
                {"value": "Clothing", "label": "Clothing"},
                {"value": "Food", "label": "Food"},
                {"value": "Electronics", "label": "Electronics"},
            ],
        },
    ]
    return render_template("input_template.html", title="Category", form_action="/submit_category", fields=fields)


@app.route("/eco_rating_input")
def eco_rating_input():
    fields = [
        {
            "id": "total_rating",
            "name": "total_rating",
            "label": "Total Rating (1-100)",
            "type": "number",
            "required": True,
        },
        {"id": "certification", "name": "certification", "label": "Certification", "type": "text", "required": True},
        {"id": "audit_date", "name": "audit_date", "label": "Audit Date", "type": "date", "required": True},
        {
            "id": "sustainability",
            "name": "sustainability",
            "label": "Sustainability Score",
            "type": "number",
            "required": True,
        },
        {
            "id": "carbon_footprint",
            "name": "carbon_footprint",
            "label": "Carbon Footprint",
            "type": "number",
            "required": True,
        },
    ]
    return render_template("input_template.html", title="EcoRating", form_action="/submit_eco_rating", fields=fields)


@app.route("/purchase_input")
def purchase_input():
    fields = [
        {"id": "purchase_date", "name": "purchase_date", "label": "Purchase Date", "type": "date", "required": True},
        {"id": "user_id", "name": "user_id", "label": "User ID", "type": "number", "required": True},
        {"id": "product_id", "name": "product_id", "label": "Product ID", "type": "number", "required": True},
    ]
    return render_template("input_template.html", title="Purchase", form_action="/submit_purchase", fields=fields)


# Submission Handlers
@app.route("/submit_product", methods=["POST"])
def submit_product():
    name = request.form["name"]
    price = request.form["price"]

    # connection, server = connect_db()
    connection = connect_db()

    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Product (name, price) VALUES (%s, %s)", (name, price))
            connection.commit()
            print("Product submitted successfully!")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        connection.close()
        # server.stop()

    return render_template("feedback_template.html", success=True)


@app.route("/submit_user", methods=["POST"])
def submit_user():
    username = request.form["username"]
    email = request.form["email"]
    role = request.form["role"]

    # connection, server = connect_db()
    connection = connect_db()

    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO User (username, email, role) VALUES (%s, %s, %s)", (username, email, role))
            connection.commit()
            print("User submitted successfully!")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        connection.close()
        # server.stop()

    return render_template("feedback_template.html", success=True)


@app.route("/submit_category", methods=["POST"])
def submit_category():
    name = request.form["name"]
    description = request.form["description"]
    category_type = request.form["category_type"]

    # connection, server = connect_db()
    connection = connect_db()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Category (name, description, category_type) VALUES (%s, %s, %s)",
                (name, description, category_type),
            )
            connection.commit()
            print("Category submitted successfully!")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        connection.close()
        # server.stop()

    return render_template("feedback_template.html", success=True)


@app.route("/submit_eco_rating", methods=["POST"])
def submit_eco_rating():
    total_rating = request.form["total_rating"]
    certification = request.form["certification"]
    audit_date = request.form["audit_date"]
    sustainability = request.form["sustainability"]
    carbon_footprint = request.form["carbon_footprint"]

    # connection, server = connect_db()
    connection = connect_db()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO EcoRating (total_rating, certification, audit_date, sustainability, carbon_footprint) VALUES (%s, %s, %s, %s, %s)",
                (total_rating, certification, audit_date, sustainability, carbon_footprint),
            )
            connection.commit()
            print("EcoRating submitted successfully!")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        connection.close()
        # server.stop()

    return render_template("feedback_template.html", success=True)


@app.route("/submit_purchase", methods=["POST"])
def submit_purchase():
    purchase_date = request.form["purchase_date"]
    user_id = request.form["user_id"]
    product_id = request.form["product_id"]

    # connection, server = connect_db()
    connection = connect_db()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO Purchases (purchase_date, user_id, product_id) VALUES (%s, %s, %s)",
                (purchase_date, user_id, product_id),
            )
            connection.commit()
            print("Purchase submitted successfully!")
    except Exception as e:
        print(f"Error occurred: {str(e)}")
    finally:
        connection.close()
        # server.stop()

    return render_template("feedback_template.html", success=True)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8013)
