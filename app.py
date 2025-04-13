from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session handling

# Database connection setup
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="demo_site"
)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Create a new cursor for querying products
    cursor = db.cursor()

    try:
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
    finally:
        cursor.close()  # Ensure the cursor is closed after use

    return render_template('home.html', products=products)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor()

        try:
            # Check if username already exists
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            if user:
                return "Username already exists!", 409

            # Insert new user
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
            return redirect(url_for('login'))
        finally:
            cursor.close()  # Ensure the cursor is closed after use

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor(dictionary=True)  # Initialize the cursor here

        try:
            # Print the query to check input
            query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
            print("Executing Query:", query)  # 👉 Check the console

            cursor.execute(query)
            user = cursor.fetchone()

            # Ensure we read all results before proceeding
            cursor.fetchall()  # If you have more results to fetch, do this to clear the result set

            if user:
                return redirect(url_for('home'))
            else:
                return "Invalid Credentials!"

        finally:
            cursor.close()  # Close the cursor after we're done with it

    return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/search', methods=['GET'])
def search_page():
    query = request.args.get('query')
    cursor = db.cursor()

    try:
        if query:
            cursor.execute("SELECT * FROM products WHERE name LIKE %s", ('%' + query + '%',))
            products = cursor.fetchall()
        else:
            products = []
    finally:
        cursor.close()  # Ensure the cursor is closed after use

    return render_template('search.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)
