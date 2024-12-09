"""
Extended test suite for the Flask application using MagicMock.
"""

import os
from unittest.mock import MagicMock, patch
from bson import ObjectId
import pytest
from app.app import create_app


@pytest.fixture
def app_fixture():
    """
    Create and configure a new app instance for testing with mocked db.
    """
    with patch.dict(
        os.environ,
        {
            "MONGO_URI": "mongodb://mongodb:27017/wishlist_db",
            "MONGO_DBNAME": "wishlist",
        },
    ):
        with patch("app.app.pymongo.MongoClient") as mock_mongo_client:
            # Mock database and collections
            mock_db = MagicMock()
            mock_mongo_client.return_value = {"wishlist": mock_db}
            app = create_app()
            app.config.update({"TESTING": True})
            yield app, mock_db  # pylint: disable=redefined-outer-name


@pytest.fixture
def client(app_fixture):  # pylint: disable=redefined-outer-name
    """
    A test client for the app.
    """
    app, _ = app_fixture
    return app.test_client()


def mock_user_data():
    """Return mock user data."""
    return {"username": "test_user", "password": "test_pass"}


def test_home_page(client):  # pylint: disable=redefined-outer-name
    """Test the home page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'<a href="./login">Log in</a>' in response.data
    assert b'<a href="./signup">Sign up</a>' in response.data

def test_login(client, app_fixture):  # pylint: disable=redefined-outer-name
    """Test the login page"""
    _, mock_db = app_fixture
    mock_db.users.find_one.return_value = mock_user_data()

    response = client.post(
        "/login", data={"username": "test_user", "password": "test_pass"}
    )
    assert response.status_code == 302  # Redirects after successful login
    assert response.headers["Location"] == "/test_user"

def test_login_post_failure(client, app_fixture):  # pylint: disable=redefined-outer-name
    """Test login failure with incorrect credentials."""
    _, mock_db = app_fixture
    mock_db.users.find_one.return_value = None  # Simulate no user found

    response = client.post("/login", data={"username": "fake_user", "password": "wrong_pass"})

    # Check for redirection to the login page
    assert response.status_code == 302  # Redirect after failure
    assert response.headers["Location"] == "/login"

def test_signup(client, app_fixture):  # pylint: disable=redefined-outer-name
    """Test the signup page."""
    _, mock_db = app_fixture
    mock_db.users.find_one.return_value = None  # No user with this username

    response = client.post(
        "/signup", data={"username": "new_user", "password": "secure_pass"}
    )
    assert response.status_code == 302  # Redirects after successful signup
    assert response.headers["Location"] == "/login"

def test_signup_post_existing_user(client, app_fixture):  # pylint: disable=redefined-outer-name
    """Test signup failure with an existing username."""
    _, mock_db = app_fixture
    mock_db.users.find_one.return_value = {"username": "existing_user"}  # Simulate user exists

    response = client.post(
        "/signup", data={"username": "existing_user", "password": "secure_pass"}
    )

    # Check for redirection to the signup page
    assert response.status_code == 302  # Redirect after failure
    assert response.headers["Location"] == "/signup"

def test_profile(client, app_fixture):  # pylint: disable=redefined-outer-name
    """Test the GET method for viewing profile."""
    _, mock_db = app_fixture
    mock_db.lists.find.return_value = [{"name": "Test Wishlist"}]

    response = client.get("/test_user")
    assert response.status_code == 200
    assert b"Test Wishlist" in response.data


def test_add_wishlist_get(client, app_fixture):  # pylint: disable=redefined-outer-name
    """Test the GET method for adding a wishlist."""
    _, mock_db = app_fixture
    mock_db.lists.find.return_value = [{"name": "Wishlist"}]

    # Mock login
    with client.session_transaction() as sess:
        sess["username"] = "test_user"

    response = client.get("/test_user/add_wishlist")
    assert response.status_code == 200
    assert b"Wishlist Name" in response.data


def test_add_wishlist_post(client, app_fixture):  # pylint: disable=redefined-outer-name
    """Test the POST method for adding a wishlist."""
    _, mock_db = app_fixture
    mock_db.lists.insert_one.return_value = None  # Simulate insert success

    # Mock login
    with client.session_transaction() as sess:
        sess["username"] = "test_user"

    response = client.post("/test_user/add_wishlist", data={"name": "New Wishlist"})
    assert response.status_code == 302  # Redirects after successful post
    assert response.headers["Location"] == "/test_user"


def test_wishlist_view(client, app_fixture):  # pylint: disable=redefined-outer-name
    """Test viewing a wishlist."""
    _, mock_db = app_fixture
    mock_wishlist_id = str(ObjectId())
    mock_db.lists.find_one.return_value = {
        "_id": ObjectId(mock_wishlist_id),
        "name": "Test Wishlist",
        "items": [],
    }

    response = client.get(f"/wishlist/{mock_wishlist_id}")
    assert response.status_code == 200
    assert b"Test Wishlist" in response.data


def test_add_item_post(client, app_fixture):  # pylint: disable=redefined-outer-name
    """Test the POST method for adding an item to a wishlist."""
    _, mock_db = app_fixture
    mock_wishlist_id = str(ObjectId())
    mock_db.lists.find_one.return_value = {
        "_id": ObjectId(mock_wishlist_id),
        "name": "Test Wishlist",
        "items": [],
    }

    response = client.post(
        f"/wishlist/{mock_wishlist_id}/add_item",
        data={"name": "New Item", "price": "10.00", "link": "http://example.com"},
    )
    assert response.status_code == 302
    assert response.headers["Location"] == f"/wishlist/{mock_wishlist_id}"
