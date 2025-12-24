from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/bookmarks')
def bookmarks():
    return render_template('bookmarks.html')

@main_bp.route('/achievements')
def achievements():
    return render_template('achievements.html')

@main_bp.route('/schedule')
def schedule():
    return render_template('schedule.html')

@main_bp.route('/flashcards')
@main_bp.route('/flashcards')
def flashcards():
    return render_template('flashcards.html')

@main_bp.route('/pods')
@main_bp.route('/pods')
def pods():
    return render_template('pods.html')

@main_bp.route('/settings')
@main_bp.route('/settings')
def settings():
    return render_template('settings.html')

@main_bp.route('/profile')
def profile():
    return render_template('profile.html')

@main_bp.route('/preferences')
def preferences():
    return render_template('preferences.html')

@main_bp.route('/security')
def security():
    return render_template('security.html')

@main_bp.route('/inbox')
def inbox():
    return render_template('inbox.html')

@main_bp.route('/welcome')
def welcome():
    return render_template('welcome.html')

@main_bp.route('/product')
def product():
    return render_template('product.html')

@main_bp.route('/learn-more')
def learn_more():
    return render_template('learn_more.html')

@main_bp.route('/login')
def login():
    return render_template('login.html')

@main_bp.route('/register')
def register():
    return render_template('register.html')
