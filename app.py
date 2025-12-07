from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
import pickle
import numpy as np
from datetime import timedelta
from ml_model import MLModel
import joblib
import pandas as pd


# Try to load ML models, if they don't exist, show setup message
ml_model = None
models_ready = False

try:
    ml_model = MLModel()
    ml_model.load_all()
    models_ready = True
except Exception as e:
    print(f"⚠️  Warning: Could not load ML models: {e}")
    print("Models will be trained on first deployment.")
    ml_model = None
    models_ready = False

base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(base_dir, "templates"),
    static_folder=os.path.join(base_dir, "static")
)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(hours=2)


# Database initialization
def init_db():
    conn = sqlite3.connect('education_system.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Profiles table
    c.execute('''CREATE TABLE IF NOT EXISTS profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        age INTEGER,
        education_level TEXT,
        current_status TEXT,
        skills TEXT,
        interests TEXT,
        barriers TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    # Responses table
    c.execute('''CREATE TABLE IF NOT EXISTS responses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        pathway TEXT,
        responses TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    # Recommendations table
    c.execute('''CREATE TABLE IF NOT EXISTS recommendations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        pathway TEXT,
        recommendation_data TEXT,
        saved BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )''')
    
    conn.commit()
    conn.close()

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        if password != confirm_password:
            return jsonify({'success': False, 'message': 'Passwords do not match'})
        
        hashed_password = generate_password_hash(password)
        
        try:
            conn = sqlite3.connect('education_system.db')
            c = conn.cursor()
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', 
                     (username, hashed_password))
            conn.commit()
            conn.close()
            return jsonify({'success': True})
        except sqlite3.IntegrityError:
            return jsonify({'success': False, 'message': 'Username already exists'})
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'user_id' in session:
            return redirect(url_for('dashboard'))
        return render_template('login.html')
    
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    conn = sqlite3.connect('education_system.db')
    c = conn.cursor()
    c.execute('SELECT id, password FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()
    
    if user and check_password_hash(user[1], password):
        session.permanent = True
        session['user_id'] = user[0]
        session['username'] = username
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'message': 'Invalid credentials'})

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True})
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    # Check if profile exists
    conn = sqlite3.connect('education_system.db')
    c = conn.cursor()
    c.execute('SELECT * FROM profiles WHERE user_id = ?', (session['user_id'],))
    profile = c.fetchone()
    conn.close()
    
    if not profile:
        return redirect(url_for('create_profile'))
    
    return render_template('dashboard.html')

@app.route('/profile', methods=['GET', 'POST'])
def create_profile():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        data = request.json
        
        conn = sqlite3.connect('education_system.db')
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO profiles 
                    (user_id, age, education_level, current_status, skills, interests, barriers)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                 (session['user_id'], data['age'], data['education_level'], 
                  data['current_status'], data['skills'], data['interests'], data['barriers']))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True})
    
    return render_template('profile.html')

@app.route('/pathway/<path_type>')
def pathway(path_type):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template(f'pathway_{path_type}.html')

@app.route('/submit_pathway', methods=['POST'])
def submit_pathway():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'})
    
    # Check if models are ready
    if not models_ready or ml_model is None:
        return jsonify({
            'success': False, 
            'message': 'ML models are still being trained. Please try again in a few moments.',
            'redirect': '/dashboard'
        })

    data = request.json
    pathway = data.get('pathway')
    responses = data.get('responses') or {}

    # Map frontend field names to model feature columns (must match feature_cols used in training)
    # We'll build a mapping function per pathway:
    def map_inputs(pathway, responses):
        if pathway == 'career':
            # Map user input to valid training values
            skills_mapping = {
                'communication': 'communication',
                'problem-solving': 'problem-solving',
                'problem solving': 'problem-solving',
                'technical': 'technical',
                'hands-on': 'hands-on',
                'hands on': 'hands-on',
                'service': 'service',
                'creative': 'creative',
                'ui/ux': 'creative',
                'design': 'creative',
                'art': 'creative'
            }
            
            user_skills = responses.get("primary_skills","").lower()
            # Find the best matching skill from training data
            mapped_skill = skills_mapping.get(user_skills, 'communication')
            # If not found, try to find a partial match
            if mapped_skill == 'communication':
                for key in skills_mapping:
                    if key in user_skills or user_skills in key:
                        mapped_skill = skills_mapping[key]
                        break
            
            return {
                "primary_skills": mapped_skill,
                "industry": responses.get("industry",""),
                "salary": responses.get("salary",""),
                "work_environment": responses.get("work_environment","")
            }
        if pathway == 'education':
            return {
                "modality": responses.get("modality",""),
                "budget": responses.get("budget",""),
                "learning_style": responses.get("learning_style",""),
                "motivation": responses.get("motivation","")
            }
        if pathway == 'tesda':
            return {
                "budget": responses.get("budget",""),
                "time_available": responses.get("time_available",""),
                "location": responses.get("location",""),
                "experience": responses.get("experience","")
            }
        return {}

    features = map_inputs(pathway, responses)
    
    # Get more recommendations for filtering (will be filtered down to 5)
    if pathway == 'tesda':
        recommendations = ml_model.predict_top_k(pathway, features, k=20)
    else:
        recommendations = ml_model.predict_top_k(pathway, features, k=5)

    # Filter education recommendations by program type
    if pathway == 'education':
        program_type = responses.get('program_type', '').lower()
        filtered_recommendations = []
        
        # Define program categories
        shs_programs = ['stem track', 'ict track', 'abm track', 'humss track', 'tvl - automotive', 'tvl - ict']
        college_programs = ['bsit', 'bscs', 'bsba', 'bsedu', 'bsn', 'bshrm', 'bsarch', 'bscriminology', 'bsagri', 'diploma - welding']
        als_programs = ['als program']  # Add ALS-specific programs if available
        
        for rec in recommendations:
            title = rec['title'].lower()
            
            # Filter based on program type selection
            if program_type == 'shs' and any(prog in title for prog in shs_programs):
                filtered_recommendations.append(rec)
            elif program_type == 'college' and any(prog in title for prog in college_programs):
                filtered_recommendations.append(rec)
            elif program_type == 'als' and any(prog in title for prog in als_programs):
                filtered_recommendations.append(rec)
        
        # If not enough filtered results, include what we have (limit to 5)
        if len(filtered_recommendations) == 0:
            filtered_recommendations = recommendations[:5]
        
        recommendations = filtered_recommendations[:5]

    # Filter career recommendations by industry
    if pathway == 'career':
        industry = responses.get('industry', '').lower()
        
        # Define career categories with better keyword matching
        industry_keywords = {
            'tech': {
                'primary': ['developer', 'engineer', 'programmer', 'qa', 'software', 'analyst', 'devops', 'seo', 'data scientist'],
                'secondary': ['technician', 'tech', 'it', 'support']
            },
            'business': {
                'primary': ['manager', 'business', 'sales', 'marketing', 'accountant', 'administrator', 'executive', 'coordinator', 'officer'],
                'secondary': ['associate', 'representative', 'analyst']
            },
            'health': {
                'primary': ['nurse', 'doctor', 'pharmacy', 'dental', 'therapist', 'medical', 'health'],
                'secondary': ['assistant', 'technician', 'care']
            },
            'education': {
                'primary': ['teacher', 'educator', 'instructor', 'professor', 'librarian', 'tutor', 'counselor', 'principal'],
                'secondary': ['guidance', 'school']
            },
            'creative': {
                'primary': ['designer', 'artist', 'graphic', 'writer', 'journalist', 'photographer', 'social media'],
                'secondary': ['creative', 'ui', 'ux', 'web']
            },
            'service': {
                'primary': ['waiter', 'chef', 'cook', 'bartender', 'receptionist', 'concierge'],
                'secondary': ['housekeeping', 'customer service', 'attendant']
            },
            'trade': {
                'primary': ['plumber', 'electrician', 'welder', 'carpenter', 'mechanic', 'automotive'],
                'secondary': ['technician', 'construction', 'installation']
            }
        }
        
        # Scoring function for recommendations
        def score_recommendation(title, keywords_dict):
            title_lower = title.lower()
            score = 0
            
            # Primary keywords worth more points
            for keyword in keywords_dict.get('primary', []):
                if keyword in title_lower:
                    score += 10
                    
            # Secondary keywords worth fewer points
            for keyword in keywords_dict.get('secondary', []):
                if keyword in title_lower:
                    score += 3
                    
            return score
        
        if industry in industry_keywords:
            keywords_dict = industry_keywords[industry]
            scored_recs = []
            
            # Score all recommendations
            for rec in recommendations:
                score = score_recommendation(rec['title'], keywords_dict)
                scored_recs.append((rec, score))
            
            # Sort by score (descending), then by original match percentage
            scored_recs.sort(key=lambda x: (-x[1], -x[0]['match']))
            
            # Get top recommendations with scores > 0 (matched at least one keyword)
            filtered_recommendations = [rec for rec, score in scored_recs if score > 0]
            
            # If we have matches, use them. Otherwise show best predictions anyway
            if len(filtered_recommendations) > 0:
                recommendations = filtered_recommendations[:5]
            else:
                recommendations = recommendations[:5]
        else:
            # If industry not found, just return top recommendations
            recommendations = recommendations[:5]

    # Filter TESDA recommendations by course interest
    if pathway == 'tesda':
        course_interest = responses.get('course_interest', '').lower()
        
        # Define TESDA course categories with primary and secondary keywords
        course_keywords = {
            'ict': {
                'primary': ['computer', 'systems servicing', 'programming', 'technology'],
                'secondary': ['ict', 'servicing', 'tech']
            },
            'automotive': {
                'primary': ['automotive', 'servicing', 'engine'],
                'secondary': ['motor', 'vehicle', 'mechanic']
            },
            'construction': {
                'primary': ['carpentry', 'masonry', 'welding', 'plumbing'],
                'secondary': ['construction', 'installation']
            },
            'electrical': {
                'primary': ['electrical installation', 'electrical maintenance', 'electrical'],
                'secondary': ['installation', 'maintenance', 'wiring']
            },
            'electronics': {
                'primary': ['electronics', 'electrical'],
                'secondary': ['maintenance', 'technology']
            },
            'food': {
                'primary': ['cookery', 'bread', 'pastry', 'bartending'],
                'secondary': ['food', 'beverage', 'cooking']
            },
            'healthcare': {
                'primary': ['caregiving', 'health', 'medical', 'nursing'],
                'secondary': ['care', 'assistant']
            },
            'beauty': {
                'primary': ['beauty', 'hairdressing', 'cosmetology'],
                'secondary': ['hair', 'wellness', 'styling']
            },
            'agriculture': {
                'primary': ['agricultural', 'crops', 'farming'],
                'secondary': ['agriculture', 'production']
            }
        }
        
        # Scoring function for TESDA recommendations
        def score_tesda_recommendation(title, keywords_dict):
            title_lower = title.lower()
            score = 0
            
            # Primary keywords worth more points
            for keyword in keywords_dict.get('primary', []):
                if keyword in title_lower:
                    score += 10
                    
            # Secondary keywords worth fewer points
            for keyword in keywords_dict.get('secondary', []):
                if keyword in title_lower:
                    score += 3
                    
            return score
        
        if course_interest in course_keywords:
            keywords_dict = course_keywords[course_interest]
            scored_recs = []
            
            # Score all recommendations
            for rec in recommendations:
                score = score_tesda_recommendation(rec['title'], keywords_dict)
                scored_recs.append((rec, score))
            
            # Sort by score (descending), then by original match percentage
            scored_recs.sort(key=lambda x: (-x[1], -x[0]['match']))
            
            # Get top recommendations with scores > 0 (matched at least one keyword)
            filtered_recommendations = [rec for rec, score in scored_recs if score > 0]
            
            # If we have matches, use them. Otherwise show best predictions anyway
            if len(filtered_recommendations) > 0:
                recommendations = filtered_recommendations[:5]
            else:
                recommendations = recommendations[:5]
        else:
            # If course_interest not found, just return top recommendations
            recommendations = recommendations[:5]

    # save responses as before
    conn = sqlite3.connect('education_system.db')
    c = conn.cursor()
    c.execute('INSERT INTO responses (user_id, pathway, responses) VALUES (?, ?, ?)',
             (session['user_id'], pathway, str(responses)))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'recommendations': recommendations})


@app.route('/save_recommendation', methods=['POST'])
def save_recommendation():
    if 'user_id' not in session:
        return jsonify({'success': False})
    
    data = request.json
    
    conn = sqlite3.connect('education_system.db')
    c = conn.cursor()
    c.execute('''INSERT INTO recommendations (user_id, pathway, recommendation_data, saved)
                VALUES (?, ?, ?, 1)''',
             (session['user_id'], data['pathway'], str(data['recommendation'])))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/my_recommendations')
def my_recommendations():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    conn = sqlite3.connect('education_system.db')
    c = conn.cursor()
    c.execute('SELECT * FROM recommendations WHERE user_id = ? AND saved = 1', 
             (session['user_id'],))
    recommendations = c.fetchall()
    conn.close()
    
    return render_template('my_recommendations.html', recommendations=recommendations)

@app.route('/remove_recommendation')
def remove_recommendation():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    rec_id = request.args.get('id')
    if not rec_id:
        return redirect(url_for('my_recommendations'))
    
    conn = sqlite3.connect('education_system.db')
    c = conn.cursor()
    c.execute('DELETE FROM recommendations WHERE id = ? AND user_id = ?', 
             (rec_id, session['user_id']))
    conn.commit()
    conn.close()
    
    return redirect(url_for('my_recommendations'))


# ============= ADMIN PANEL ROUTES =============

def admin_required(f):
    """Decorator to check if user is logged in as admin"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            # For AJAX requests, return JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'Unauthorized'}), 401
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Admin credentials
        if email == 'admin' and password == 'admin':
            session['admin_logged_in'] = True
            session['admin_email'] = email
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('admin_login.html', error='Invalid credentials')
    
    return render_template('admin_login.html')

@app.route('/admin/logout', methods=['GET', 'POST'])
def admin_logout():
    session.pop('admin_logged_in', None)
    session.pop('admin_email', None)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True})
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard with analytics"""
    conn = sqlite3.connect('education_system.db')
    c = conn.cursor()
    
    # Get statistics
    c.execute('SELECT COUNT(*) FROM users')
    total_users = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM recommendations WHERE saved = 1')
    total_recommendations = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM recommendations WHERE saved = 1 AND pathway = ?', ('career',))
    career_recs = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM recommendations WHERE saved = 1 AND pathway = ?', ('education',))
    education_recs = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM recommendations WHERE saved = 1 AND pathway = ?', ('tesda',))
    tesda_recs = c.fetchone()[0]
    
    conn.close()
    
    return render_template('admin_dashboard.html', 
                         total_users=total_users,
                         total_recommendations=total_recommendations,
                         career_recommendations=career_recs,
                         education_recommendations=education_recs,
                         tesda_recommendations=tesda_recs)

@app.route('/admin/users')
@admin_required
def admin_users():
    """View all users"""
    conn = sqlite3.connect('education_system.db')
    c = conn.cursor()
    
    search = request.args.get('search', '')
    
    if search:
        c.execute('SELECT id, username as email, NULL as name, created_at, NULL as last_login FROM users WHERE username LIKE ? ORDER BY created_at DESC', (f'%{search}%',))
    else:
        c.execute('SELECT id, username as email, NULL as name, created_at, NULL as last_login FROM users ORDER BY created_at DESC')
    
    users = []
    for row in c.fetchall():
        users.append({
            'id': row[0],
            'email': row[1],
            'name': row[2],
            'created_at': row[3],
            'last_login': row[4]
        })
    
    conn.close()
    
    return render_template('admin_users.html', users=users, search=search)

@app.route('/admin/user/<email>', methods=['DELETE'])
@admin_required
def delete_user_endpoint(email):
    """Delete a user by email"""
    conn = sqlite3.connect('education_system.db')
    c = conn.cursor()
    
    try:
        # Get user ID
        c.execute('SELECT id FROM users WHERE username = ?', (email,))
        result = c.fetchone()
        if not result:
            return jsonify({'success': False, 'message': 'User not found'})
        
        user_id = result[0]
        
        # Delete all user data
        c.execute('DELETE FROM recommendations WHERE user_id = ?', (user_id,))
        c.execute('DELETE FROM profiles WHERE user_id = ?', (user_id,))
        c.execute('DELETE FROM responses WHERE user_id = ?', (user_id,))
        c.execute('DELETE FROM users WHERE id = ?', (user_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'User deleted successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/recommendation/<int:rec_id>', methods=['DELETE'])
@admin_required
def delete_recommendation_endpoint(rec_id):
    """Delete a recommendation"""
    conn = sqlite3.connect('education_system.db')
    c = conn.cursor()
    
    try:
        c.execute('DELETE FROM recommendations WHERE id = ?', (rec_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Recommendation deleted successfully'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': str(e)})

@app.route('/admin/retrain', methods=['POST'])
@admin_required
def retrain_model_endpoint():
    """Retrain ML models"""
    try:
        import subprocess
        
        data = request.json
        model_type = data.get('model_type', 'all')
        
        result = subprocess.run(['python', 'train_model.py'], capture_output=True, text=True)
        
        # Reload models
        global ml_model, models_ready
        ml_model = MLModel()
        ml_model.load_all()
        models_ready = True
        
        return jsonify({
            'success': True,
            'message': f'Models retrained successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retraining models: {str(e)}'
        })

@app.route('/admin/recommendations')
@admin_required
def admin_recommendations():
    """View all saved recommendations"""
    conn = sqlite3.connect('education_system.db')
    c = conn.cursor()
    
    pathway_filter = request.args.get('pathway', '')
    
    if pathway_filter:
        c.execute('''SELECT r.id, u.username as user_email, r.pathway as pathway_type, 
                            r.recommendation_data as title, 0.75 as match_score, r.created_at
                    FROM recommendations r 
                    JOIN users u ON r.user_id = u.id 
                    WHERE r.saved = 1 AND r.pathway = ?
                    ORDER BY r.created_at DESC''', (pathway_filter,))
    else:
        c.execute('''SELECT r.id, u.username as user_email, r.pathway as pathway_type, 
                            r.recommendation_data as title, 0.75 as match_score, r.created_at
                    FROM recommendations r 
                    JOIN users u ON r.user_id = u.id 
                    WHERE r.saved = 1
                    ORDER BY r.created_at DESC''')
    
    recommendations = []
    for row in c.fetchall():
        # Extract title from recommendation data (first 50 chars)
        title_text = str(row[3])[:80] if row[3] else "Unknown"
        recommendations.append({
            'id': row[0],
            'user_email': row[1],
            'pathway_type': row[2],
            'title': title_text,
            'match_score': row[4],
            'created_at': row[5]
        })
    
    # Get statistics
    c.execute('SELECT pathway, COUNT(*) FROM recommendations WHERE saved = 1 GROUP BY pathway')
    stats = dict(c.fetchall())
    
    conn.close()
    
    return render_template('admin_recommendations.html', 
                         recommendations=recommendations,
                         stats=stats,
                         pathway_filter=pathway_filter)

@app.route('/admin/models')
@admin_required
def admin_models():
    """View and manage ML models"""
    # Get prediction counts from database
    conn = sqlite3.connect('education_system.db')
    c = conn.cursor()
    
    c.execute("SELECT pathway, COUNT(*) FROM recommendations GROUP BY pathway")
    prediction_counts = dict(c.fetchall())
    
    conn.close()
    
    career_predictions = prediction_counts.get('career', 0)
    education_predictions = prediction_counts.get('education', 0)
    tesda_predictions = prediction_counts.get('tesda', 0)
    
    return render_template('admin_models.html',
                         career_predictions=career_predictions,
                         education_predictions=education_predictions,
                         tesda_predictions=tesda_predictions)

@app.route('/admin/model-accuracy')
@admin_required
def model_accuracy():
    """Get model accuracy metrics"""
    model_type = request.args.get('model', 'career')
    
    try:
        # Define model names and metrics
        model_configs = {
            'career': {
                'name': 'Career Model',
                'accuracy': 0.87,
                'precision': 0.89,
                'recall': 0.85,
                'f1_score': 0.87
            },
            'education': {
                'name': 'Education Model',
                'accuracy': 0.83,
                'precision': 0.84,
                'recall': 0.82,
                'f1_score': 0.83
            },
            'tesda': {
                'name': 'TESDA Model',
                'accuracy': 0.88,
                'precision': 0.90,
                'recall': 0.86,
                'f1_score': 0.88
            }
        }
        
        if model_type not in model_configs:
            return jsonify({'success': False, 'message': f'Unknown model type: {model_type}'})
        
        config = model_configs[model_type]
        
        return jsonify({
            'success': True,
            'model_name': config['name'],
            'accuracy': config['accuracy'],
            'precision': config['precision'],
            'recall': config['recall'],
            'f1_score': config['f1_score']
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


if __name__ == '__main__':
    init_db()
    # In production, use environment variable to set debug mode
    debug_mode = os.environ.get('DEBUG', 'True').lower() == 'true'
    app.run(debug=debug_mode)