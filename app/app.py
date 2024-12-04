from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/wishlist')
def show_wishlist():
    return render_template('wishlist.html')

@app.route('/add-item', methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        # placeholder output until db schema established
        print(request.form["link"])
        print(request.form["name"])
    return render_template('add-item.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # placeholder output until db schema established
        print(request.form["username"])
        print(request.form["password"])
    return render_template('login.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # placeholder output until db schema established
        print(request.form["username"])
        print(request.form["password"])
    return render_template('signup.html')

if __name__ == "__main__":
    app.run(debug=True, port=3000)
    # app.run(debug=True, port=3000)
