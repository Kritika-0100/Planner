from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

from models import User, Task

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/todo')
@login_required
def todo():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('todo.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
@login_required
def add_task():
    task_name = request.form.get('task_name')
    new_task = Task(user_id=current_user.id, task_name=task_name)
    db.session.add(new_task)
    db.session.commit()
    flash('Task added successfully!', 'success')
    return redirect(url_for('todo'))

@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'success')
    return redirect(url_for('todo'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        selected_theme = request.form.get('theme')
        current_user.theme = selected_theme
        db.session.commit()
        flash('Settings updated!', 'success')
        return redirect(url_for('settings'))
    return render_template('settings.html')

@app.route('/update_settings', methods=['POST'])
@login_required
def update_settings():
    theme = request.form.get('theme')
    current_user.theme = theme
    db.session.commit()
    flash('Theme updated successfully!', 'success')
    return redirect(url_for('settings'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form