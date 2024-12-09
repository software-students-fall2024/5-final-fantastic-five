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
            # Mock database and collection
            mock_db = MagicMock()
            mock_mongo_client.return_value = {"wishlist": mock_db}
            app = create_app()
            app.config.update(
                {
                    "TESTING": True,
                }
            )
            yield app, mock_db  # pylint: disable=redefined-outer-name


@pytest.fixture
def client(app_fixture):  # pylint: disable=redefined-outer-name
    """
    A test client for the app.
    """
    app, _ = app_fixture
    return app.test_client()


def test_home_page(client):  # pylint: disable=redefined-outer-name
    """Test the home page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'<a href="./login">Log in</a>' in response.data
    assert b'<a href="./signup">Sign up</a>' in response.data


def test_login(client):  # pylint: disable=redefined-outer-name
    """Test the login page"""
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Username" in response.data
    assert b"Password" in response.data


def test_login_post(client):  # pylint: disable=redefined-outer-name
    """Test the POST method for user login."""
    response = client.post("/login", data={"username": "test_user", "password": "test_pass"})
    assert response.status_code == 302  # Redirects after successful login
    assert response.headers["Location"] == "/test_user"


def test_signup(client):  # pylint: disable=redefined-outer-name
    """Test the signup page."""
    response = client.get("/signup")
    assert response.status_code == 200
    assert b"Username" in response.data
    assert b"Password" in response.data


def test_signup_post(client):  # pylint: disable=redefined-outer-name
    """Test the POST method for user signup."""
    response = client.post(
        "/signup", data={"username": "new_user", "password": "secure_pass"}
    )
    assert response.status_code == 302  # Redirects after successful signup
    assert response.headers["Location"] == "/new_user"


def test_profile(client):  # pylint: disable=redefined-outer-name
    """Test the GET method for viewing profile."""
    response = client.get("/nht251")
    assert response.status_code == 200
    assert b"nht251" in response.data


def test_add_wishlist_get(client):  # pylint: disable=redefined-outer-name
    """Test the GET method for adding a wishlist."""
    response = client.get("/nht251/add_wishlist")
    assert response.status_code == 200
    assert b"Wishlist Name" in response.data


def test_add_wishlist_post(client):  # pylint: disable=redefined-outer-name
    """Test the POST method for adding a wishlist."""
    response = client.post("/nht251/add_wishlist", data={"name": "New Wishlist"})
    assert response.status_code == 302  # Redirects after successful post
    assert response.headers["Location"] == "/nht251"


def test_wishlist_view(client, app_fixture):  # pylint: disable=redefined-outer-name
    """Test viewing a wishlist."""
    _, mock_db = app_fixture
    mock_wishlist_id = str(ObjectId())  # Generate a valid ObjectId string
    mock_db.lists.find_one.return_value = {
        "_id": ObjectId(mock_wishlist_id),
        "name": "Test Wishlist",
        "items": [],
    }
    response = client.get(f"/wishlist/{mock_wishlist_id}")
    print(response.data)
    assert response.status_code == 200
    assert b"/add_item" in response.data


def test_add_item_get(client, app_fixture):  # pylint: disable=redefined-outer-name
    """Test the GET method for adding an item."""
    _, mock_db = app_fixture
    mock_wishlist_id = str(ObjectId())  # Generate a valid ObjectId string
    mock_db.lists.find_one.return_value = {
        "_id": ObjectId(mock_wishlist_id),
        "name": "Test Wishlist",
        "items": [],
    }
    response = client.get(f"/wishlist/{mock_wishlist_id}/add_item")
    # response = client.get("/wishlist/mock_id/add_item")
    assert response.status_code == 200
    assert b"Add Item" in response.data


def test_add_item_post(client, app_fixture):  # pylint: disable=redefined-outer-name
    """Test the POST method for adding an item to a wishlist"""
    _, mock_db = app_fixture
    mock_wishlist_id = str(ObjectId())  # Generate a valid ObjectId string
    mock_db.lists.find_one.return_value = {
        "_id": ObjectId(mock_wishlist_id),
        "name": "Test Wishlist",
        "items": [],
    }
    response = client.post(
        f"/wishlist/{mock_wishlist_id}/add_item",
        data={"name": "New Item", "price": "10.00", "link": "http://example.com"},
    )
    assert response.status_code == 302  # Redirects after successful post
    assert response.headers["Location"] == f"/wishlist/{mock_wishlist_id}"
