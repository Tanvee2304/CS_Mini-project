from flask import Flask, request, render_template # type: ignore
import mysql.connector # type: ignore

app = Flask(__name__)

# Configure Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root", # Change this if using another user
    password="root",   # Add password if set
    database="demo_site"
)
cursor = db.cursor()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor(dictionary=True)
        
        # Print the query to check input
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print("Executing Query:", query)  # 👉 Check the console

        cursor.execute(query)
        user = cursor.fetchone()

        if user:
            return "Login Successful!"
        else:
            return "Invalid Credentials!"

    return render_template("login.html")

@app.route('/search', methods=['GET', 'POST'])
def search():
    product_details = None

    if request.method == 'POST':
        search_query = request.form['query']

        # Fetch matching product details
        query = f"SELECT * FROM products WHERE name LIKE '%{search_query}%'"
        cursor.execute(query)
        product_details = cursor.fetchall()  # Fetch all matching products

    return render_template("search.html", product_details=product_details)



if __name__ == '__main__':
    app.run(debug=True)
