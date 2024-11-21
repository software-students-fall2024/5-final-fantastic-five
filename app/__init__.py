from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI") 
client = MongoClient(mongo_uri)
db = client["wishlist_db"]

@app.route("/")
def home():
    return "Connected to MongoDB Atlas!"

if __name__ == "__main__":
    app.run(debug=True)
