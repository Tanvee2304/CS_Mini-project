from flask import Flask, request, render_template
import mysql.connector

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
        # 🚨 SQL Injection Vulnerable Query
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()

        if user:
            return "Login Successful!"
        else:
            return "Invalid Credentials!"

    return render_template("login.html")

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = None
    if request.method == 'POST':
        search_query = request.form['query']
        
        # ❌ Intentionally Vulnerable SQL Query (for SQL Injection testing)
        query = f"SELECT * FROM products WHERE name LIKE '%{search_query}%'"
        cursor.execute(query)
        results = cursor.fetchall()

    return render_template('search.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
