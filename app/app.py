"""
Flask API for managing wishlists.
Handles routes for wishlist creation, retrieval, and updates.
"""

from functools import wraps
import os
import uuid
import pymongo
from bson import ObjectId
from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for, session, flash

load_dotenv()


def create_app():
    """Initializes and configures the Flask app."""
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB limit
    app.secret_key = os.getenv("SECRET_KEY")
    app.config["SESSION_TYPE"] = "filesystem"

    mongo_uri = os.getenv("MONGO_URI")
    mongo_dbname = "wishlist"

    if not mongo_uri:
        raise ValueError("MONGO_URI is not set in the environment variables.")
    if not mongo_dbname:
        raise ValueError("MONGO_DBNAME is not set in the environment variables.")

    connection = pymongo.MongoClient(mongo_uri, tls=True)
    db = connection[mongo_dbname]

    # indexing
    db.users.create_index("username", unique=True)
    db.lists.create_index("public_id")

    register_routes(app, db)

    return app


def register_routes(app, db):
    """Register routes"""

    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "username" not in session:
                flash("Access denied. Please log in.", "error")
                return redirect(url_for("login"))
            return f(*args, **kwargs)

        return decorated_function

    @app.route("/")
    def home():
        """
        Home route that renders the homepage.
        """
        return render_template("home.html")

    @app.route("/<username>")
    def profile(username):
        """
        Profile page for a user displaying their wishlists.

        Args:
            username (str): Username of the profile owner.

        Returns:
            Rendered HTML template for the profile page.
        """
        user_wishlists = list(db.lists.find({"username": username}))
        return render_template(
            "profile.html", username=username, wishlists=user_wishlists
        )

    @app.route("/<username>/add_wishlist", methods=["GET", "POST"])
    @login_required
    def add_wishlist(username):
        """
        Route to add a new wishlist for a user.

        Args:
            username (str): Username of the profile owner.

        Returns:
            Redirects to the profile page after adding a wishlist or renders the add wishlist page.
        """
        if session["username"] != username:
            flash("Access denied. You cannot modify another user's wishlist.", "error")
            return redirect(url_for("home"))

        if request.method == "POST":
            new_wishlist = {
                "username": username,
                "items": [],
                "name": request.form["name"],
                "public_id": str(uuid.uuid4()),  # Generate a unique public ID
            }
            db.lists.insert_one(new_wishlist)
            return redirect(url_for("profile", username=username))

        user_wishlists = list(db.lists.find({"username": username}))
        return render_template(
            "add-wishlist.html", username=username, wishlists=user_wishlists
        )

    @app.route("/wishlist/<wishlist_id>")
    def wishlist_view(wishlist_id):
        """
        Route to display a specific wishlist with its items.

        Args:
            wishlist_id (str): ID of the wishlist.

        Returns:
            Rendered HTML template for the wishlist page.
        """
        user_wishlist = db.lists.find_one({"_id": ObjectId(wishlist_id)})
        items = list(db.items.find({"wishlist": ObjectId(wishlist_id)}))
        return render_template("wishlist.html", wishlist=user_wishlist, items=items)

    @app.route("/wishlist/<wishlist_id>/add_item", methods=["GET", "POST"])
    def add_item(wishlist_id):
        """
        Route to add an item to a specific wishlist.

        Args:
            wishlist_id (str): ID of the wishlist.

        Returns:
            Redirects to the wishlist page after adding an item or renders the add item page.
        """
        if request.method == "POST":
            wishlist_items = db.lists.find_one({"_id": ObjectId(wishlist_id)})["items"]
            new_item = {
                "wishlist": ObjectId(wishlist_id),
                "link": request.form["link"],
                "name": request.form["name"],
                "price": request.form["price"],
            }
            wishlist_items.append(new_item)
            db.lists.update_one(
                {"_id": ObjectId(wishlist_id)}, {"$set": {"items": wishlist_items}}
            )
            db.items.insert_one(new_item)
            return redirect(url_for("wishlist_view", wishlist_id=wishlist_id))
        return render_template("add-item.html", id=wishlist_id)

    @app.route("/login", methods=["GET", "POST"])
    def login():
        """
        Route for user login.

        Returns:
            Redirects to the profile page after successful login or renders the login page.
        """
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            # Find user in the database
            user = db.users.find_one({"username": username})
            if not user or user["password"] != password:
                flash("Invalid username or password.", "error")
                return redirect(url_for("login"))

            # Login success: store user in session
            session["username"] = username
            return redirect(url_for("profile", username=username))

        return render_template("login.html")

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        """
        Route for user signup.

        Returns:
            Redirects to the profile page after successful signup or renders the signup page.
        """
        if request.method == "POST":
            username = request.form["username"].strip()
            password = request.form["password"].strip()

            # Validation
            if len(username) < 3 or len(password) < 6:
                flash(
                    "Username must be at least 3 characters and password at least 6 characters.",
                    "error",
                )
                return redirect(url_for("signup"))

            # Check if username already exists
            if db.users.find_one({"username": username}):
                flash(
                    "Username already exists. Please choose a different one.", "error"
                )
                return redirect(url_for("signup"))

            # Store user details in plain-text
            new_user = {
                "username": username,
                "password": password,
            }
            db.users.insert_one(new_user)
            flash("Signup successful! Please log in.", "success")
            return redirect(url_for("login"))
        return render_template("signup.html")

    @app.route("/logout")
    def logout():
        """
        Route for user logout.
        """
        session.pop("username", None)
        flash("You have been logged out.", "info")
        return redirect(url_for("home"))

    @app.route("/view/<public_id>")
    def public_view(public_id):
        """
        Public view to show a shared wishlist.
        """
        wishlist = db.lists.find_one({"public_id": public_id})
        if not wishlist:
            return "Wishlist not found", 404
        items = db.items.find({"wishlist": wishlist["_id"]})
        return render_template("public_wishlist.html", wishlist=wishlist, items=items)

    @app.route("/view/mark_purchased/<item_id>", methods=["POST"])
    def mark_as_purchased(item_id):
        db.items.update_one({"_id": ObjectId(item_id)}, {"$set": {"purchased": True}})
        return "Item marked as purchased", 200


APP = create_app()
if __name__ == "__main__":
    # APP.run(host="0.0.0.0", port=3000)
    APP.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", "3000")))
