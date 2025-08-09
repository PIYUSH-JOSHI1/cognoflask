from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
import csv
import json
from datetime import datetime
import uuid
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config.get('SECRET_KEY', 'learning-disability-support-platform-2024')

# Create necessary directories
def create_directories():
    directories = [
        'data/users',
        'data/progress',
        'data/dyslexia',
        'data/dyscalculia', 
        'data/dysgraphia',
        'data/dyspraxia',
        'data/ai_models',
        'static/uploads',
        'static/user_data'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

create_directories()

# Import all modules
from modules.auth import auth_bp
from modules.dyslexia import dyslexia_bp
from modules.dyscalculia import dyscalculia_bp
from modules.dysgraphia import dysgraphia_bp
from modules.dyspraxia import dyspraxia_bp
from modules.dashboard import dashboard_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dyslexia_bp, url_prefix='/dyslexia')
app.register_blueprint(dyscalculia_bp, url_prefix='/dyscalculia')
app.register_blueprint(dysgraphia_bp, url_prefix='/dysgraphia')
app.register_blueprint(dyspraxia_bp, url_prefix='/dyspraxia')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard.main'))
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
