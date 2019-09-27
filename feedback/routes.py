import os
import secrets
from PIL import Image
from flask import render_template, flash, url_for, redirect, request
from feedback import app, db, bcrypt
from feedback.forms import FeedbackForm, RegistrationForm, LoginForm, UpdateAccountForm
from feedback.models import Feedback, Registration
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST', 'GET'])
def submit():
    form = FeedbackForm()
    if form.validate_on_submit():
        f = Feedback(form.customer.data, form.dealer.data, form.rating.data, form.comments.data)
        db.session.add(f)
        db.session.commit()
        flash('Feedback successfully submitted.')
        return redirect(url_for('success'))
    return render_template('submit.html', form=form)
    
@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        hash_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Registration(fullname=form.fullname.data, email=form.email.data, password=hash_pass)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully, You can now login.')
        return redirect(url_for('login'))
    return render_template('register.html', title= 'Register', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user = Registration.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsucessful. Check email and password')

    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pic', picture_fn)

    # resize image before saving using pillow
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    # form_picture.save(picture_path)

    return picture_fn

@app.route('/dashboard' , methods=['POST', 'GET'])
@login_required
def dashboard():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.img_file = picture_file
        current_user.fullname = form.fullname.data
        current_user.email = form.email.data
        db.session.commit()
        flash('You account has been updated.')
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        form.fullname.data = current_user.fullname
        form.email.data = current_user.email
    img_file = url_for('static', filename='profile_pic/' + current_user.img_file)
    return render_template('dashboard.html', title='Dashboard', img_file=img_file, form=form)
