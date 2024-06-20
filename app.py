from flask import Flask, render_template, url_for, flash, redirect, request, jsonify
from models import db, bcrypt, login_manager, User, Post
from flask_login import login_user, current_user, logout_user, login_required
from config import Config
import random
import time

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()

# Sample paragraphs
paragraphs = [
    "The quick brown fox jumps over the lazy dog.",
    "A journey of a thousand miles begins with a single step.",
    "To be or not to be, that is the question.",
    "All that glitters is not gold.",
    "A picture is worth a thousand words."
]
# Time allocation for each paragraph (in seconds)
time_allocations = {
    "short": 10,   # 1/2 minutes
    "medium": 20   # 1/2 and more minutes
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    else:
        flash('User already exists')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    paragraph = random.choice(paragraphs)
    return render_template('dashboard.html', paragraph=paragraph)

@app.route('/generate_paragraph', methods=['GET'])
def generate_paragraph():
    # Select a random paragraph and determine its length
    paragraph = random.choice(paragraphs)
    if len(paragraph.split()) > 15:  # Adjust the threshold for short vs medium paragraphs as needed
        paragraph_type = "medium"
    else:
        paragraph_type = "short"
    
    # Return paragraph and time allocation
    return jsonify({'paragraph': paragraph, 'time': time_allocations[paragraph_type]})

@app.route('/result', methods=['POST'])
def result():
    user_text = request.form['user_text']
    original_text = request.form['original_text']
    start_time = float(request.form['start_time'])
    end_time = time.time()
    
    # Calculate the time taken
    time_taken = end_time - start_time
    
    # Calculate words per minute
    words_count = len(user_text.split())
    if time_taken > 0:
        wps = words_count / time_taken
    else:
        wps = 0  # Handle division by zero edge case
    
    
    # Calculate accuracy
    correct_chars = sum(1 for a, b in zip(user_text, original_text) if a == b)
    accuracy = correct_chars / len(original_text) * 100
    
    result = {
        'time_taken': time_taken,
        'wps': wps,
        'accuracy': accuracy
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)