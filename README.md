# Final Project: Wish List Tracker App

![Flask API CI/CD Badge](https://github.com/software-students-fall2024/5-final-fantastic-five/actions/workflows/flask-api.yml)
![MongoDB CI/CD Badge](https://github.com/software-students-fall2024/5-final-fantastic-five/actions/workflows/mongodb.yml)

## Table of Contents
- [Project Description](#project-description)
- [Subsystems Overview](#subsystems-overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Testing](#testing)
- [Contributors](#contributors)
- [Links](#links)
- [Future Work](#future-work)

---

## Project Description
The Wish List Tracker App is a web-based platform designed to help users organize, share, and manage their wishlists for any occasion. Users can create multiple wishlists, add items with detailed information (e.g., name, price, purchase link), and share these lists with friends and family. The app aims to simplify gift-giving while avoiding duplicate gifts through a "claim" feature. 

**Target Audience:** 
- Individuals organizing wishlists for personal use.
- Families and friends looking to streamline gift exchanges.

**Key Features:**
- Wishlist creation and management.
- Sharing wishlists via unique links.
- Item claiming to prevent duplicate purchases.
- (Future) Item recommendations based on wishlist contents.


---

## Subsystems Overview

### Subsystem 1: Flask API
- **Description:** The Flask API serves as the backend of the application, providing endpoints for user authentication, wishlist management, and item claiming. It integrates with the MongoDB database to store and retrieve data.
- **Technology Stack:** Python, Flask, MongoDB
- **Container:** [Link to Docker Hub image] (To be added)

### Subsystem 2: MongoDB Database
- **Description:** The MongoDB database stores all application data, including user profiles, wishlists, and items. It ensures data persistence and allows for efficient querying.
- **Technology Stack:** MongoDB
- **Container:** [Link to Docker Hub image] (To be added)


---

## Getting Started

### Prerequisites
- Python 3.9+ for local dev 
- Docker and Docker Compose installed on your system.
- MongoDB (running locally or in Docker)

### Setup Instructions
1. Clone the repository:
    ```bash
    git clone https://github.com/software-students-fall2024/5-final-fantastic-five.git
    ```
2. Navigate to the project directory:
    ```bash
    cd 5-final-fantastic-five
    ```
3. Set up environment variables:
    create a .env file in the root of the project with following values:
    ```bash
    MONGO_URI=mongodb://mongodb:27017/wishlist_db
    SECRET_KEY=your_secret_key
    ```

4. Build and run containers: 
Use Docker Compose to set up the application:
    ```bash
    docker-compose up --build
    ```

5. Verify services:
    Flask API: open http://localhost:3000 in browser
    MongoDB: Connect using a MongoDB client (like compass) or the Mongo shell.

Here’s how you can add a **"Local Development Setup"** section to your `README`:

---

### Local Development Setup (Optional)

If you'd like to work on the Flask API outside the containerized environment, follow these steps to set up the project locally:

--- 

#### Prerequisites
- Python 3.9+
- MongoDB installed locally or running in a Docker container.

---
#### Steps to Set Up

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/software-students-fall2024/5-final-fantastic-five.git
   cd 5-final-fantastic-five
   ```

2. **Set Up a Virtual Environment:**
   Create and activate a Python virtual environment to manage dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   Install the required Python libraries listed in `requirements.txt`:
   ```bash
   pip install -r app/requirements.txt
   ```

4. **Set Up Environment Variables:**
   Create a `.env` file in the root of the project with the following content:
   ```bash
   MONGO_URI=mongodb://localhost:27017/wishlist_db
   SECRET_KEY=your_secret_key
   ```

5. **Run MongoDB Locally (Optional):**
   If MongoDB is not already running locally, start it using Docker:
   ```bash
   docker run -d -p 27017:27017 --name mongodb mongo
   ```

6. **Start the Flask API Locally:**
   Navigate to the Flask application directory and start the server:
   ```bash
   cd app
   flask run --host=0.0.0.0 --port=3000
   ```

   The API will be accessible at `http://localhost:3000`.

---

#### Notes:
- When working locally, ensure the `MONGO_URI` in your `.env` file points to the correct MongoDB instance (local or Dockerized).
- Always activate the virtual environment (`source venv/bin/activate`) before running the application locally.
- To deactivate the virtual environment, run `deactivate`.

---

## Usage
Once the application is set up, update the following steps:
1. Access the Flask API endpoints for managing wishlists and items (e.g., `http://localhost:3000/wishlists`). 
2. Use the /wishlists endpoint to create and retrieve wishlists via POST requests
3. Share wishlists by using the generated unique links.

---

## Environment Variables
The application requires the following environment variables:
- `MONGO_URI`: Connection string for MongoDB (e.g., mongodb://mongodb:27017/wishlist_db for local Dockerized MongoDB, or an Atlas URI for production).
- `SECRET_KEY`: Secret key for Flask sessions.

---

## Testing
Each subsystem includes unit tests to ensure functionality.

<!-- temp, not actual commands, just for example -->
### Running Tests
1. **Flask API**
    ```bash
    cd app
    pytest --cov=.
    ```
2. **Database**
    Run ```bash
    docker exec -it mongodb mongo
    ``` and verify the seeded collections.

---

## Contributors
- [Alexandra Mastrangelo](https://github.com/alexandramastrangelo)
- [Natalie Trump](https://github.com/nht251)

---

## Links
- [Container Images](#)
    - [Flask API Image](https://hub.docker.com/r/arm9129/flask-api)
  - [MongoDB Image](https://hub.docker.com/r/arm9129/db)
  - [Database Seeder Image](https://hub.docker.com/r/arm9129/db-seeder)
- [Digital Ocean Deployment](wishlist-app-lrc7l.ondigitalocean.app)


---

## Future Work
- **Item Recommendations:** Suggest items based on wishlist content.
- **Collaborative Wishlists:** Allow multiple users to contribute to a single wishlist.
- **Price Tracking:** Notify users of price changes for wishlist items.