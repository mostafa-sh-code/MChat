from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'secret123'

DATA_FILE = "data.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {"users": {}, "posts": []}

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def home():
    posts = data.get("posts", [])
    return render_template('home.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in data["users"]:
            if data["users"][username] == password:
                session['username'] = username
                return redirect(url_for('post_page'))
            else:
                return "❌ رمز عبور اشتباه است!"
        else:
            data["users"][username] = password
            save_data()
            session['username'] = username
            return redirect(url_for('post_page'))

    return render_template('login.html')

@app.route('/post', methods=['GET', 'POST'])
def post_page():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        data["posts"].append({
            "username": session['username'],
            "title": title,
            "content": content
        })
        save_data()
        return redirect(url_for('home'))

    return render_template('post_form.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
