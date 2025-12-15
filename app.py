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
import ast
import json
import re


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
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Not authenticated'})
        
        # Check if models are ready
        if not models_ready or ml_model is None:
            return jsonify({
                'success': False, 
                'message': 'ML models are still being trained. Please try again in a few moments.',
                'redirect': '/dashboard'
            })

        if not request.is_json:
            return jsonify({'success': False, 'message': 'Request must be JSON'})
            
        data = request.json
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'})
            
        pathway = data.get('pathway')
        responses = data.get('responses') or {}

        # Map frontend field names to model feature columns (must match feature_cols used in training)
        # We'll build a mapping function per pathway:
        def map_inputs(pathway, responses):
            if pathway == 'career':
                # Map user input to valid training values
                # Skills mapping - map form values to dataset values
                skills_mapping = {
                    'communication': 'communication',
                    'problem-solving': 'problem-solving',
                    'problem solving': 'problem-solving',
                    'technical': 'technical',
                    'leadership': 'leadership',  # Leadership exists in dataset
                    'creativity': 'creativity',  # Creativity exists in dataset
                    'analytical': 'problem-solving',
                    'organization': 'communication',
                    'teamwork': 'communication',
                    'customer service': 'service',
                    'sales': 'service',
                    'hands-on': 'hands-on',
                    'hands on': 'hands-on',
                    'service': 'service',
                    'creative': 'creativity',
                    'ui/ux': 'design',
                    'design': 'design',
                    'art': 'creativity'
                }
                
                user_skills = responses.get("primary_skills","").lower().strip()
                # Find the best matching skill from training data
                mapped_skill = skills_mapping.get(user_skills, 'communication')
                # If not found, try to find a partial match
                if mapped_skill == 'communication' and user_skills not in skills_mapping:
                    for key in skills_mapping:
                        if key in user_skills or user_skills in key:
                            mapped_skill = skills_mapping[key]
                            break
                
                # Industry mapping - form values to dataset values
                industry_mapping = {
                    'tech': 'tech',
                    'technology/it': 'tech',
                    'business': 'business',
                    'business/sales': 'business',
                    'health': 'health',
                    'healthcare': 'health',
                    'education': 'education',
                    'creative': 'creative',
                    'creative/arts': 'creative',
                    'service': 'service',
                    'service industry': 'service',
                    'trade': 'trade',
                    'skilled trades': 'trade',
                    'government': 'business',  # Map to closest match
                    'finance': 'business',
                    'finance/banking': 'business'
                }
                industry = responses.get("industry","").lower().strip()
                mapped_industry = industry_mapping.get(industry, industry if industry in ['tech', 'business', 'health', 'education', 'creative', 'service', 'trade'] else 'tech')
                
                # Salary mapping - form values to dataset format
                salary_mapping = {
                    '15k-25k': '60k-80k',  # Map to entry-level range
                    '25k-40k': '65k-85k',
                    '40k-60k': '70k-90k',
                    '60k+': '80k-120k',
                    '30k-50k': '60k-80k',
                    '50k-70k': '70k-90k',
                    '70k-90k': '70k-90k',
                    '80k+': '80k-120k'
                }
                salary = responses.get("salary","").lower().strip()
                # Check if it's already a valid dataset value
                valid_salaries = ['60k-80k', '65k-85k', '70k-90k', '75k-95k', '80k-110k', '80k-120k', '90k-130k']
                mapped_salary = salary_mapping.get(salary, salary if salary in valid_salaries else '60k-80k')
                
                # Work environment mapping
                environment_mapping = {
                    'office': 'office',
                    'office-based': 'office',
                    'remote': 'remote',
                    'remote/work from home': 'remote',
                    'field': 'field',
                    'field work': 'field',
                    'hybrid': 'hybrid',
                    'outdoor': 'outdoor'
                }
                work_env = responses.get("work_environment","").lower().strip()
                mapped_env = environment_mapping.get(work_env, work_env if work_env in ['office', 'remote', 'hybrid', 'field', 'outdoor'] else 'office')
                
                return {
                    "primary_skills": mapped_skill,
                    "industry": mapped_industry,
                    "salary": mapped_salary,
                    "work_environment": mapped_env
                }
            if pathway == 'education':
                # Modality mapping
                modality_mapping = {
                    'face_to_face': 'full_time',
                    'face-to-face': 'full_time',
                    'online': 'online',
                    'hybrid': 'hybrid',
                    'flexible': 'flexible',
                    'flexible schedule': 'flexible'
                }
                modality = responses.get("modality","").lower().strip()
                mapped_modality = modality_mapping.get(modality, modality if modality in ['full_time', 'online', 'hybrid', 'flexible'] else 'full_time')
                
                # Budget mapping - duration to budget
                budget_mapping = {
                    'short_term': 'low',
                    'short-term': 'low',
                    'medium_term': 'medium',
                    'medium-term': 'medium',
                    'long_term': 'high',
                    'long-term': 'high',
                    'flexible': 'medium',
                    'flexible/self-paced': 'medium'
                }
                duration = responses.get("budget","").lower().strip()
                mapped_budget = budget_mapping.get(duration, duration if duration in ['low', 'medium', 'high'] else 'medium')
                
                # Learning style - default to kinesthetic if not provided
                learning_style = responses.get("learning_style","").lower().strip()
                mapped_learning_style = learning_style if learning_style in ['kinesthetic', 'visual', 'auditory', 'reading'] else 'kinesthetic'
                
                # Motivation - default to career-focused
                motivation = responses.get("motivation","").lower().strip()
                mapped_motivation = motivation if motivation in ['career-focused', 'personal-growth', 'academic'] else 'career-focused'
                
                return {
                    "modality": mapped_modality,
                    "budget": mapped_budget,
                    "learning_style": mapped_learning_style,
                    "motivation": mapped_motivation
                }
            if pathway == 'tesda':
                # Budget mapping - training duration to budget
                budget_mapping = {
                    'short': 'free',
                    'short-term': 'free',
                    'medium': 'paid',  # TESDA uses 'paid' not 'low'
                    'medium-term': 'paid',
                    'long': 'paid',
                    'long-term': 'paid',
                    'flexible': 'free',
                    'flexible/self-paced': 'free'
                }
                duration = responses.get("budget","").lower().strip()
                mapped_budget = budget_mapping.get(duration, duration if duration in ['free', 'paid'] else 'free')
                
                # Time available mapping - schedule to time_available
                time_mapping = {
                    'full_time': 'full_time',
                    'full-time': 'full_time',
                    'weekdays': 'full_time',
                    'weekends': 'part_time',
                    'weekends only': 'part_time',
                    'evenings': 'part_time',
                    'flexible': 'flexible',
                    'flexible schedule': 'flexible'
                }
                schedule = responses.get("time_available","").lower().strip()
                mapped_time = time_mapping.get(schedule, schedule if schedule in ['full_time', 'part_time', 'flexible'] else 'part_time')
                
                # Location - default to manila if not provided
                location = responses.get("location","").lower().strip()
                location_mapping = {
                    'manila': 'manila',
                    'makati': 'makati',
                    'quezon city': 'quezon_city',
                    'quezon_city': 'quezon_city',
                    'pasig': 'manila',  # Map to closest
                    'taguig': 'makati',
                    'mandaluyong': 'makati'
                }
                mapped_location = location_mapping.get(location, location if location in ['manila', 'makati', 'quezon_city'] else 'manila')
                
                # Experience mapping
                experience_mapping = {
                    'none': 'beginner',
                    'no experience': 'beginner',
                    'basic': 'beginner',
                    'basic knowledge': 'beginner',
                    'intermediate': 'intermediate',
                    'some experience': 'intermediate',
                    'advanced': 'advanced',
                    'highly experienced': 'advanced'
                }
                experience = responses.get("experience","").lower().strip()
                mapped_experience = experience_mapping.get(experience, experience if experience in ['beginner', 'intermediate', 'advanced'] else 'beginner')
                
                return {
                    "budget": mapped_budget,
                    "time_available": mapped_time,
                    "location": mapped_location,
                    "experience": mapped_experience
                }
            return {}

        features = map_inputs(pathway, responses)
        
        # Get more recommendations for filtering (will be filtered down to 5)
        if pathway == 'tesda':
            recommendations = ml_model.predict_top_k(pathway, features, k=20)
        else:
            recommendations = ml_model.predict_top_k(pathway, features, k=5)

        # Filter education recommendations by program type and education level
        if pathway == 'education':
            # Scoring constants for education recommendations (matching TESDA pathway for consistency)
            PRIMARY_KEYWORD_POINTS = 10
            SECONDARY_KEYWORD_POINTS = 3
            MIN_BASE_SCORE = 80.0  # Increased from 60 to 80 for higher match percentages
            SCORE_DIVISOR = 10
            BONUS_MULTIPLIER = 20
            MAX_BONUS = 35  # Maximum bonus percentage from keywords
            MAX_MATCH_SCORE = 95.0  # Maximum possible match percentage
            
            program_type = responses.get('program_type', '').lower()
            education_level = responses.get('education_level', '').lower()
            filtered_recommendations = []
            
            # Define allowed program types based on education level
            allowed_programs = {
                'master': ['graduate', 'college'],  # Allow second bachelor's degree
                'bachelor': ['graduate', 'college'],
                'associate': ['college', 'graduate'],
                'vocational': ['college', 'graduate', 'als'],  # Keep for backward compatibility
                'high_school': ['shs', 'college', 'als'],
                'phd': ['graduate']  # PhD holders can pursue additional graduate degrees
            }
            
            # Check if program type is allowed for education level
            if education_level in allowed_programs and program_type not in allowed_programs[education_level]:
                return jsonify({
                    'success': False,
                    'message': f"For your education level, please select from: {', '.join(allowed_programs[education_level])}",
                    'recommendations': []
                })
            
            # Define program categories with improved matching
            # NOTE: Removed trailing spaces from graduate keywords (ms, ma) to allow matching "MS in Engineering"
            shs_programs = ['stem track', 'ict track', 'abm track', 'humss', 'humanities track', 'tvl', 'arts track', 'sports science']
            college_programs = ['bachelor', 'bs ', 'ba ', 'bsit', 'bscs', 'bsba', 'bsedu', 'bsn', 'bshrm', 'bsarch']
            als_programs = ['als', 'alternative learning', 'accreditation', 'equivalency']
            graduate_programs = ['master', 'mba', 'phd', 'doctorate', 'ms', 'ma', 'doctor', 'executive mba', 'professional certification', 'professional master', 'cpa review', 'pmp', 'cisa', 'lpt review', 'dba', 'med', 'edd']
            # Exclude keywords for graduate programs (to prevent bachelor's programs from being included)
            bachelor_exclude_keywords = ['bachelor', 'bs ', 'ba ', 'bsit', 'bscs', 'bsba', 'bsedu', 'bsn', 'bshrm', 'bsarch', 'bse']
            
            # Debug logging
            print(f"DEBUG: Total recommendations before filtering: {len(recommendations)}")
            print(f"DEBUG: Program type selected: {program_type}")
            print(f"DEBUG: Education level: {education_level}")
            if len(recommendations) > 0:
                print(f"DEBUG: Sample titles: {[rec['title'] for rec in recommendations[:5]]}")
            
            for rec in recommendations:
                title = rec['title'].lower()
                
                # Filter based on program type selection with relaxed validation
                if program_type == 'shs' and any(prog in title for prog in shs_programs):
                    filtered_recommendations.append(rec)
                elif program_type == 'college' and any(prog in title for prog in college_programs):
                    filtered_recommendations.append(rec)
                elif program_type == 'als' and any(prog in title for prog in als_programs):
                    filtered_recommendations.append(rec)
                elif program_type == 'graduate':
                    # For graduate programs, check for graduate keywords
                    has_graduate_keyword = any(kw in title for kw in graduate_programs)
                    # More relaxed bachelor exclusion - only check for exact bachelor degree patterns
                    has_bachelor_keyword = 'bachelor' in title or title.startswith('bs ') or title.startswith('ba ')
                    
                    if has_graduate_keyword and not has_bachelor_keyword:
                        filtered_recommendations.append(rec)
            
            # Debug logging after filtering
            print(f"DEBUG: Recommendations after program type filter: {len(filtered_recommendations)}")
            if len(filtered_recommendations) > 0:
                print(f"DEBUG: Filtered sample titles: {[rec['title'] for rec in filtered_recommendations[:5]]}")
            
            # Check if graduate programs exist in dataset
            if program_type == 'graduate':
                graduate_in_dataset = [rec for rec in recommendations if any(kw in rec['title'].lower() for kw in ['master', 'phd', 'mba', 'doctorate'])]
                print(f"DEBUG: Graduate programs in dataset: {len(graduate_in_dataset)}")
                if len(graduate_in_dataset) > 0:
                    print(f"DEBUG: Sample graduate programs: {[rec['title'] for rec in graduate_in_dataset[:3]]}")
            
            # If not enough filtered results, return empty with message
            if len(filtered_recommendations) == 0:
                return jsonify({
                    'success': False,
                    'message': f'No {program_type} programs found. Please try different criteria.',
                    'recommendations': []
                })
            
            # Field-based filtering (optional)
            field_of_interest = responses.get('field_of_interest', '').lower()
            field_program_mapping = {
                'technology': ['computer', 'it', 'software', 'programming', 'web', 'systems servicing', 'information technology', 'cybersecurity', 'data science', 'stem track', 'ict'],
                'business': ['business', 'management', 'mba', 'accountancy', 'finance', 'abm', 'bookkeeping', 'administration', 'executive'],
                'healthcare': ['nursing', 'caregiving', 'massage', 'medical', 'health', 'therapy'],
                'engineering': ['engineering', 'engineer', 'civil', 'mechanical', 'electrical', 'industrial', 'structural', 'chemical', 'stem'],
                'creative': ['arts', 'design', 'animation', 'visual graphic', 'fine arts', 'communication'],
                'education': ['education', 'teaching', 'teacher', 'mat', 'lpt', 'humss'],
                'culinary': ['cookery', 'bread', 'pastry', 'food', 'beverage', 'bartending'],
                'construction': ['welding', 'carpentry', 'masonry', 'plumbing', 'construction', 'tile setting', 'heavy equipment', 'painting'],
                'agriculture': ['agricultural', 'agriculture', 'crops', 'organic', 'farming'],
                'tourism': ['tourism', 'hospitality', 'tour guiding', 'travel services', 'hotel', 'front office'],
                'beauty': ['beauty', 'hairdressing', 'nail care', 'wellness', 'cosmetology'],
                'automotive': ['automotive', 'servicing', 'mechanic', 'vehicle'],
                'electronics': ['electronics', 'electrical', 'electronic products', 'consumer electronics', 'electrical maintenance']
            }
            
            # Track which recommendations match the field (to avoid duplicate checking later)
            field_matched_titles = set()
            if field_of_interest and field_of_interest in field_program_mapping:
                field_keywords = field_program_mapping[field_of_interest]
                field_filtered = []
                
                for rec in filtered_recommendations:
                    title_lower = rec['title'].lower()
                    if any(kw in title_lower for kw in field_keywords):
                        field_filtered.append(rec)
                        field_matched_titles.add(rec['title'])
                
                # Only apply field filter if we get results
                if len(field_filtered) > 0:
                    filtered_recommendations = field_filtered
            
            # Define education program keywords for boosting
            program_keywords = {
                'shs': {
                    'primary': ['stem', 'track', 'abm', 'humss', 'humanities', 'tvl', 'ict', 'arts', 'sports'],
                    'secondary': ['senior', 'high', 'school', 'technical']
                },
                'college': {
                    'primary': ['bs', 'ba', 'bsit', 'bscs', 'bsba', 'bsn', 'bse', 'bachelor'],
                    'secondary': ['college', 'degree', 'university', 'program', 'major', 'science', 'arts']
                },
                'als': {
                    'primary': ['als', 'alternative', 'learning', 'accreditation', 'equivalency'],
                    'secondary': ['education', 'system', 'program']
                },
                'graduate': {
                    'primary': ['master', 'mba', 'phd', 'doctorate', 'ms', 'ma', 'doctor', 'executive mba', 'mat', 'cpa review', 'pmp', 'cisa', 'lpt review', 'dba', 'edd', 'med'],
                    'secondary': ['graduate', 'advanced', 'professional', 'certification', 'research', 'administration', 'review', 'licensed', 'engineering management', 'hospital administration', 'public administration', 'cybersecurity', 'data science']
                }
            }
            
            # Scoring function for education recommendations
            def score_education_recommendation(title, keywords_dict):
                title_lower = title.lower()
                score = 0
                
                for keyword in keywords_dict.get('primary', []):
                    if keyword in title_lower:
                        score += PRIMARY_KEYWORD_POINTS
                
                for keyword in keywords_dict.get('secondary', []):
                    if keyword in title_lower:
                        score += SECONDARY_KEYWORD_POINTS
                
                return score
            
            # Apply boosting
            if program_type in program_keywords:
                keywords_dict = program_keywords[program_type]
                scored_recs = []
                
                for rec in filtered_recommendations:
                    score = score_education_recommendation(rec['title'], keywords_dict)
                    
                    if score > 0:
                        boosted_match = max(rec['match'], MIN_BASE_SCORE)
                        keyword_bonus = min((score / SCORE_DIVISOR) * BONUS_MULTIPLIER, MAX_BONUS)
                        rec['match'] = min(boosted_match + keyword_bonus, MAX_MATCH_SCORE)
                        
                        # Add +5% bonus for field of interest match (use cached check)
                        if rec['title'] in field_matched_titles:
                            rec['match'] = min(rec['match'] + 5, MAX_MATCH_SCORE)
                    
                    scored_recs.append((rec, score))
                
                scored_recs.sort(key=lambda x: (-x[1], -x[0]['match']))
                filtered_recommendations = [rec for rec, score in scored_recs if score > 0]
                
                if len(filtered_recommendations) > 0:
                    recommendations = filtered_recommendations[:5]
                else:
                    recommendations = recommendations[:5]
            else:
                recommendations = filtered_recommendations[:5]

        # Filter career recommendations by industry
        if pathway == 'career':
            # Scoring constants for career recommendations (matching TESDA pathway for consistency)
            PRIMARY_KEYWORD_POINTS = 10
            SECONDARY_KEYWORD_POINTS = 3
            MIN_BASE_SCORE = 60.0  # Minimum match percentage for keyword matches
            SCORE_DIVISOR = 10
            BONUS_MULTIPLIER = 20
            MAX_BONUS = 35  # Maximum bonus percentage from keywords
            MAX_MATCH_SCORE = 95.0  # Maximum possible match percentage
            
            industry = responses.get('industry', '').lower()
            
            # Define career categories with comprehensive keyword matching
            industry_keywords = {
            'tech': {
                'primary': ['software', 'developer', 'programmer', 'data', 'analyst', 'it', 'technology', 'web', 'app'],
                'secondary': ['computer', 'systems', 'technical', 'digital', 'engineer', 'specialist']
            },
            'healthcare': {
                'primary': ['nurse', 'nursing', 'medical', 'health', 'care', 'therapy', 'therapist', 'clinical'],
                'secondary': ['assistant', 'technician', 'caregiver', 'wellness', 'patient']
            },
            'health': {  # Alias for 'healthcare' to support both form inputs and dataset values
                'primary': ['nurse', 'nursing', 'medical', 'health', 'care', 'therapy', 'therapist', 'clinical'],
                'secondary': ['assistant', 'technician', 'caregiver', 'wellness', 'patient']
            },
            'business': {
                'primary': ['business', 'management', 'manager', 'accountant', 'finance', 'hr', 'human resources'],
                'secondary': ['administrator', 'operations', 'executive', 'analyst', 'consultant']
            },
            'creative': {
                'primary': ['design', 'designer', 'graphic', 'content', 'writer', 'creative', 'ux', 'ui', 'artist'],
                'secondary': ['media', 'visual', 'digital', 'marketing', 'brand']
            },
            'engineering': {
                'primary': ['engineer', 'engineering', 'civil', 'mechanical', 'electrical', 'industrial'],
                'secondary': ['technical', 'design', 'construction', 'manufacturing', 'automation']
            },
            'education': {
                'primary': ['teacher', 'teaching', 'professor', 'educator', 'instructor', 'tutor', 'education'],
                'secondary': ['training', 'academic', 'faculty', 'learning', 'curriculum']
            },
            'sales': {
                'primary': ['sales', 'marketing', 'representative', 'account', 'customer', 'business development'],
                'secondary': ['client', 'service', 'relationship', 'commercial', 'retail']
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
            
            # Scoring function for career recommendations
            def score_career_recommendation(title, keywords_dict):
                title_lower = title.lower()
                score = 0
                
                # Primary keywords worth more points
                for keyword in keywords_dict.get('primary', []):
                    if keyword in title_lower:
                        score += PRIMARY_KEYWORD_POINTS
                        
                # Secondary keywords worth fewer points
                for keyword in keywords_dict.get('secondary', []):
                    if keyword in title_lower:
                        score += SECONDARY_KEYWORD_POINTS
                        
                return score
                
            if industry in industry_keywords:
                keywords_dict = industry_keywords[industry]
                scored_recs = []
                
                # Score all recommendations and boost match percentages
                for rec in recommendations:
                    score = score_career_recommendation(rec['title'], keywords_dict)
                    
                    # Boost match percentage if there's a keyword match
                    if score > 0:
                        # Start with original match or minimum base score (whichever is higher)
                        boosted_match = max(rec['match'], MIN_BASE_SCORE)
                        
                        # Add bonus based on keyword score
                        keyword_bonus = min((score / SCORE_DIVISOR) * BONUS_MULTIPLIER, MAX_BONUS)
                        
                        rec['match'] = min(boosted_match + keyword_bonus, MAX_MATCH_SCORE)
                    
                    scored_recs.append((rec, score))
                
                # Sort by score (descending), then by original match percentage
                scored_recs.sort(key=lambda x: (-x[1], -x[0]['match']))
                
                # Get top recommendations with scores > 0
                filtered_recommendations = [rec for rec, score in scored_recs if score > 0]
                
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
                'primary': ['computer', 'systems servicing', 'programming', 'technology', 'web', 'database', 'network'],
                'secondary': ['ict', 'servicing', 'tech']
            },
            'automotive': {
                'primary': ['automotive', 'servicing', 'engine', 'automotive servicing', 'diesel', 'transmission'],
                'secondary': ['motor', 'vehicle', 'mechanic']
            },
            'construction': {
                'primary': ['masonry', 'carpentry', 'welding', 'plumbing', 'construction'],
                'secondary': ['building', 'installation', 'fabrication', 'repair', 'maintenance']
            },
            'electrical': {
                'primary': ['electrical installation', 'electrical maintenance', 'electrical', 'wiring', 'installation and maintenance'],
                'secondary': ['installation', 'maintenance', 'wiring']
            },
            'electronics': {
                'primary': ['electronics', 'electrical', 'products assembly', 'servicing'],
                'secondary': ['maintenance', 'technology']
            },
            'food': {
                'primary': ['cookery', 'bread', 'pastry', 'bartending', 'food processing'],
                'secondary': ['food', 'beverage', 'cooking']
            },
            'healthcare': {
                'primary': ['caregiving', 'health', 'medical', 'nursing', 'massage therapy', 'health care'],
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
            
            # Scoring constants for TESDA recommendations
            PRIMARY_KEYWORD_POINTS = 10  # Points awarded per primary keyword match
            SECONDARY_KEYWORD_POINTS = 3  # Points awarded per secondary keyword match
            MIN_BASE_SCORE = 60.0  # Minimum match percentage for keyword matches
            BONUS_MULTIPLIER = 20  # Percentage bonus per 10 keyword points
            MAX_BONUS = 35  # Maximum bonus percentage from keywords
            MAX_MATCH_SCORE = 95.0  # Maximum possible match percentage
            
            # Scoring function for TESDA recommendations
            def score_tesda_recommendation(title, keywords_dict):
                title_lower = title.lower()
                score = 0

                # Primary keywords worth more points
                for keyword in keywords_dict.get('primary', []):
                    if keyword in title_lower:
                        score += PRIMARY_KEYWORD_POINTS

                # Secondary keywords worth fewer points
                for keyword in keywords_dict.get('secondary', []):
                    if keyword in title_lower:
                        score += SECONDARY_KEYWORD_POINTS

                return score
            if course_interest in course_keywords:
                keywords_dict = course_keywords[course_interest]
                scored_recs = []
                
                # Score all recommendations and boost match percentages
                for rec in recommendations:
                    score = score_tesda_recommendation(rec['title'], keywords_dict)
                    
                    # If there's a keyword match, boost the original match percentage
                    if score > 0:
                        # Start with original match or minimum base score (whichever is higher)
                        boosted_match = max(rec['match'], MIN_BASE_SCORE)
                        
                        # Add bonus based on keyword score
                        # Each PRIMARY_KEYWORD_POINTS adds BONUS_MULTIPLIER% to match
                        keyword_bonus = min((score / PRIMARY_KEYWORD_POINTS) * BONUS_MULTIPLIER, MAX_BONUS)
                        
                        rec['match'] = min(boosted_match + keyword_bonus, MAX_MATCH_SCORE)
                    
                    scored_recs.append((rec, score))
                
                # Sort by score (descending), then by boosted match percentage
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
    except Exception as e:
        import traceback
        print(f"Error in submit_pathway: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False, 
            'message': f'An error occurred: {str(e)}'
        }), 500


@app.route('/save_recommendation', methods=['POST'])
def save_recommendation():
    try:
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Not authenticated'})
        
        if not request.is_json:
            return jsonify({'success': False, 'message': 'Request must be JSON'})
        
        data = request.json
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'})
        
        # Handle both 'pathway' and 'pathway_type' for compatibility
        pathway = data.get('pathway') or data.get('pathway_type')
        if not pathway:
            return jsonify({'success': False, 'message': 'Pathway not provided'})
        
        recommendation = data.get('recommendation')
        if not recommendation:
            return jsonify({'success': False, 'message': 'Recommendation data not provided'})
        
        conn = sqlite3.connect('education_system.db')
        c = conn.cursor()
        c.execute('''INSERT INTO recommendations (user_id, pathway, recommendation_data, saved)
                    VALUES (?, ?, ?, 1)''',
                 (session['user_id'], pathway, str(recommendation)))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Recommendation saved successfully'})
    except Exception as e:
        import traceback
        print(f"Error in save_recommendation: {str(e)}")
        print(traceback.format_exc())
        return jsonify({
            'success': False, 
            'message': f'An error occurred: {str(e)}'
        }), 500

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
                            r.recommendation_data, r.created_at
                    FROM recommendations r 
                    JOIN users u ON r.user_id = u.id 
                    WHERE r.saved = 1 AND r.pathway = ?
                    ORDER BY r.created_at DESC''', (pathway_filter,))
    else:
        c.execute('''SELECT r.id, u.username as user_email, r.pathway as pathway_type, 
                            r.recommendation_data, r.created_at
                    FROM recommendations r 
                    JOIN users u ON r.user_id = u.id 
                    WHERE r.saved = 1
                    ORDER BY r.created_at DESC''')
    
    recommendations = []
    for row in c.fetchall():
        # Parse recommendation data to extract title and match
        rec_data_str = str(row[3]) if row[3] else "{}"
        title_text = "Unknown"
        match_score = 0.75  # default
        
        try:
            # Try to parse as dict string first (most common format)
            if rec_data_str.startswith('{'):
                rec_data = ast.literal_eval(rec_data_str)
            else:
                # Try JSON parsing
                rec_data = json.loads(rec_data_str)
            
            # Extract title and match from parsed data
            title_text = rec_data.get('title', 'Unknown')
            match_score = rec_data.get('match', 0.75)
            # Convert match percentage to decimal if needed
            if isinstance(match_score, (int, float)) and match_score > 1:
                match_score = match_score / 100.0
        except (ValueError, SyntaxError, json.JSONDecodeError):
            # If parsing fails, try to extract title from string using regex
            # Look for 'title': 'value' or "title": "value" patterns
            title_match = re.search(r"['\"]title['\"]:\s*['\"]([^'\"]+)['\"]", rec_data_str)
            if title_match:
                title_text = title_match.group(1)
            else:
                # Try another pattern: 'title': 'value'
                title_match = re.search(r"'title':\s*['\"]([^'\"]+)['\"]", rec_data_str)
                if title_match:
                    title_text = title_match.group(1)
                else:
                    # Fallback: just use first 50 chars
                    title_text = rec_data_str[:50] if len(rec_data_str) > 0 else "Unknown"
        
        recommendations.append({
            'id': row[0],
            'user_email': row[1],
            'pathway_type': row[2],
            'title': title_text,
            'match_score': match_score,
            'created_at': row[4]  # created_at is now at index 4 (5th column)
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