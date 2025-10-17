from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'student' or 'teacher'
    school = db.Column(db.String(120))
    points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    progress = db.relationship('UserProgress', backref='user', lazy=True)
    challenges = db.relationship('UserChallenge', backref='user', lazy=True)
    badges = db.relationship('UserBadge', backref='user', lazy=True)

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    category = db.Column(db.String(50))  # climate, waste, biodiversity, etc.
    difficulty = db.Column(db.String(20))  # beginner, intermediate, advanced
    points_reward = db.Column(db.Integer, default=10)

    # Relationships
    quizzes = db.relationship('Quiz', backref='lesson', lazy=True)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    options = db.Column(db.Text)  # JSON string of options
    correct_answer = db.Column(db.Integer, nullable=False)  # index of correct option
    explanation = db.Column(db.Text)

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    points_reward = db.Column(db.Integer, default=50)
    duration_days = db.Column(db.Integer, default=7)
    is_active = db.Column(db.Boolean, default=True)

class UserProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    score = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime)

class UserChallenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
    status = db.Column(db.String(20), default='in_progress')  # in_progress, completed, failed
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    criteria = db.Column(db.String(100))  # points_threshold, challenges_completed, etc.

class UserBadge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['user_type'] = user.user_type
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        school = request.form.get('school', '')

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose another.', 'error')
            return render_template('register.html')

        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please use another email.', 'error')
            return render_template('register.html')

        # Create new user
        new_user = User(
            username=username,
            email=email,
            password=password,
            user_type=user_type,
            school=school
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/lessons')
def lessons():
    if 'user_id' not in session:
        flash('Please login to access lessons.', 'warning')
        return redirect(url_for('login'))

    lessons = Lesson.query.all()
    user_progress = {}
    if 'user_id' in session:
        progress = UserProgress.query.filter_by(user_id=session['user_id']).all()
        user_progress = {p.lesson_id: p.completed for p in progress}

    return render_template('lessons.html', lessons=lessons, user_progress=user_progress)

@app.route('/lesson/<int:lesson_id>')
def lesson_detail(lesson_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    lesson = Lesson.query.get_or_404(lesson_id)
    return render_template('lesson_detail.html', lesson=lesson)

@app.route('/quiz/<int:lesson_id>')
def quiz(lesson_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    lesson = Lesson.query.get_or_404(lesson_id)
    quizzes = Quiz.query.filter_by(lesson_id=lesson_id).all()

    # Convert options from JSON string to list
    for quiz in quizzes:
        quiz.options = json.loads(quiz.options)

    return render_template('quiz.html', lesson=lesson, quizzes=quizzes)

@app.route('/submit_quiz/<int:lesson_id>', methods=['POST'])
def submit_quiz(lesson_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login'})

    user_id = session['user_id']
    data = request.json
    answers = data.get('answers', {})

    # Calculate score
    score = 0
    total = len(answers)

    for quiz_id, answer in answers.items():
        quiz = Quiz.query.get(int(quiz_id))
        if quiz and int(answer) == quiz.correct_answer:
            score += 1

    # Update user progress
    progress = UserProgress.query.filter_by(user_id=user_id, lesson_id=lesson_id).first()
    if not progress:
        progress = UserProgress(user_id=user_id, lesson_id=lesson_id)
        db.session.add(progress)

    progress.completed = True
    progress.score = score
    progress.completed_at = datetime.utcnow()

    # Award points
    user = User.query.get(user_id)
    lesson = Lesson.query.get(lesson_id)
    user.points += lesson.points_reward

    db.session.commit()

    return jsonify({
        'success': True,
        'score': score,
        'total': total,
        'points_earned': lesson.points_reward
    })

@app.route('/challenges')
def challenges():
    if 'user_id' not in session:
        flash('Please login to access challenges.', 'warning')
        return redirect(url_for('login'))

    challenges = Challenge.query.filter_by(is_active=True).all()
    user_challenges = {}
    if 'user_id' in session:
        user_challenges_data = UserChallenge.query.filter_by(user_id=session['user_id']).all()
        user_challenges = {uc.challenge_id: uc.status for uc in user_challenges_data}

    return render_template('challenges.html', challenges=challenges, user_challenges=user_challenges)

@app.route('/join_challenge/<int:challenge_id>')
def join_challenge(challenge_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login'})

    user_id = session['user_id']

    # Check if already joined
    existing = UserChallenge.query.filter_by(user_id=user_id, challenge_id=challenge_id).first()
    if existing:
        return jsonify({'success': False, 'message': 'Already joined this challenge'})

    # Join challenge
    user_challenge = UserChallenge(user_id=user_id, challenge_id=challenge_id)
    db.session.add(user_challenge)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Challenge joined successfully!'})

@app.route('/complete_challenge/<int:challenge_id>', methods=['POST'])
def complete_challenge(challenge_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Please login'})

    user_id = session['user_id']

    # Update challenge status
    user_challenge = UserChallenge.query.filter_by(user_id=user_id, challenge_id=challenge_id).first()
    if not user_challenge:
        return jsonify({'success': False, 'message': 'Challenge not found'})

    user_challenge.status = 'completed'
    user_challenge.completed_at = datetime.utcnow()

    # Award points
    challenge = Challenge.query.get(challenge_id)
    user = User.query.get(user_id)
    user.points += challenge.points_reward

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Challenge completed!',
        'points_earned': challenge.points_reward
    })

@app.route('/leaderboard')
def leaderboard():
    # Get top users by points
    top_users = User.query.filter_by(user_type='student').order_by(User.points.desc()).limit(20).all()

    # Get school rankings
    school_rankings = db.session.query(
        User.school,
        db.func.sum(User.points).label('total_points')
    ).filter(User.user_type == 'student', User.school != '').group_by(User.school).order_by(db.desc('total_points')).all()

    return render_template('leaderboard.html', top_users=top_users, school_rankings=school_rankings)

@app.route('/rewards')
def rewards():
    if 'user_id' not in session:
        flash('Please login to view rewards.', 'warning')
        return redirect(url_for('login'))

    user_id = session['user_id']
    badges = Badge.query.all()
    user_badges = UserBadge.query.filter_by(user_id=user_id).all()
    user_badge_ids = [ub.badge_id for ub in user_badges]

    user = User.query.get(user_id)

    return render_template('rewards.html', badges=badges, user_badge_ids=user_badge_ids, user=user)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login to access dashboard.', 'warning')
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)

    if user.user_type == 'teacher':
        # Teacher dashboard
        students = User.query.filter_by(user_type='student', school=user.school).all()

        # Get student progress data
        student_data = []
        for student in students:
            completed_lessons = UserProgress.query.filter_by(user_id=student.id, completed=True).count()
            completed_challenges = UserChallenge.query.filter_by(user_id=student.id, status='completed').count()
            student_data.append({
                'student': student,
                'completed_lessons': completed_lessons,
                'completed_challenges': completed_challenges,
                'points': student.points
            })

        return render_template('dashboard.html', user=user, student_data=student_data, is_teacher=True)
    else:
        # Student dashboard
        completed_lessons = UserProgress.query.filter_by(user_id=user_id, completed=True).count()
        total_lessons = Lesson.query.count()
        completed_challenges = UserChallenge.query.filter_by(user_id=user_id, status='completed').count()
        total_challenges = Challenge.query.filter_by(is_active=True).count()

        # Recent activity
        recent_lessons = UserProgress.query.filter_by(user_id=user_id, completed=True).order_by(UserProgress.completed_at.desc()).limit(5).all()
        recent_challenges = UserChallenge.query.filter_by(user_id=user_id).order_by(UserChallenge.started_at.desc()).limit(5).all()

        return render_template('dashboard.html',
                             user=user,
                             completed_lessons=completed_lessons,
                             total_lessons=total_lessons,
                             completed_challenges=completed_challenges,
                             total_challenges=total_challenges,
                             recent_lessons=recent_lessons,
                             recent_challenges=recent_challenges,
                             is_teacher=False)

# API endpoints
@app.route('/api/user_progress')
def api_user_progress():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    user_id = session['user_id']
    progress = UserProgress.query.filter_by(user_id=user_id).all()

    data = {
        'completed_lessons': len([p for p in progress if p.completed]),
        'total_lessons': Lesson.query.count(),
        'average_score': sum([p.score for p in progress if p.completed]) / len([p for p in progress if p.completed]) if [p for p in progress if p.completed] else 0
    }

    return jsonify(data)

# Initialize database
def init_db():
    with app.app_context():
        db.create_all()

        # Import and run sample data initialization
        try:
            from database.init_db import init_sample_data
            init_sample_data()
        except ImportError:
            print("Warning: Could not import sample data initialization. Database created without sample data.")

# Initialize database on startup
init_db()

if __name__ == '__main__':
    app.run(debug=True)
