
from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'secreta-cheie'

DATABASE = 'database.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            price REAL,
            image TEXT
        )""")
        conn.commit()

if not os.path.exists(DATABASE): init_db()
    
@app.route('/')
def index():
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM products LIMIT 4")
        products = c.fetchall()
    return render_template('index.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        with sqlite3.connect(DATABASE) as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
            result = c.fetchone()
        if result:
            session['user'] = user
            return redirect(url_for('index'))
        return "Login esuat."
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        return "Mesaj trimis cu succes!"
    return render_template('contact.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + query + '%',))
        results = c.fetchall()
    return render_template('search.html', products=results, query=query)

@app.route('/product/<int:product_id>')
def product(product_id):
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM products WHERE id=?", (product_id,))
        product = c.fetchone()
    return render_template('product.html', product=product)


if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
