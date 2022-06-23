#!/usr/bin/env python3
from flask import flash, redirect, render_template, request, session, url_for
from flask_cors import CORS
from flask_login import current_user, login_required, login_user, logout_user
from posts.database.engine import User, Post
from werkzeug.security import check_password_hash
from posts import app
from posts.database import storage
from posts.forms import LoginForm, RegisterForm, PostForm

from posts import helper_methods
app.url_map.strict_slashes = False

cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.route('/', methods=['GET', 'POST'])
def index():
    uin = helper_methods.logged_in(current_user)
    # form = PostForm()
    # record = storage.all()
    return render_template("home.html", uin=uin)

@app.route('/create_post', methods=['POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        obj = Post(post=form.post.data, ingridients=form.ingridients.data, recipe=form.recipe.data)
        storage.save(obj)
        if current_user.is_authenticated:
            setattr(obj, 'user_id', current_user.id)
            storage.save(obj)
            flash('Successfully posted!', 'success')
            return redirect(url_for('dashboard'))
        else:
            session['cookie'] = obj.id
            flash("Please login first!")
            return redirect(url_for("login"))
    return redirect(url_for("dashboard"))


@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """Return user homepage with their posts listed"""
    uin = helper_methods.logged_in(current_user)
    try:
        if session['cookie']:
            post_id = session['cookie']
            post_obj = storage.get_post_by_id(post_id)
            setattr(post_obj, 'user_id', current_user.id)
            storage.save(post_obj)
            session['cookie'] = None
    except KeyError:
        pass
    user = storage.get_user_by_id(current_user.id)
    u_post = list()
    for rec in user.post:
        u_post.append(rec)

    return render_template('user_dashboard.html', uin=uin, user=user, u_post=u_post)

@app.route("/dashboard", methods=['POST', 'DELETE'])
def update():
    req = request.form
    if request.method == 'POST':
        updated_line = req.get('updated_post').split('</span>')[1]
        updated_post = updated_line.split(',id=')[0]
        post_id = updated_line.split(',id=')[1]
        for rec in storage.all().values():
            if str(rec.id) == post_id:
                setattr(rec, 'title', updated_post)
                storage.save(rec)
    else:
        post_to_delete = req.get('post_to_delete')
        for rec in storage.all().values():
            if str(rec.id) == post_to_delete:
                storage.delete(rec)
    return("just updated/deleted")
    
@app.route('/register', methods=['POST', 'GET'])
def register():
    uin = helper_methods.logged_in(current_user)
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        storage.save(user)
        flash('A warm welcome!', 'success')
        login_user(user)
        return redirect(url_for('dashboard'))
    return render_template('register.html', uin=uin, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    uin = helper_methods.logged_in(current_user)
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = storage.get_user_by_email(form.email.data)
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password!', 'danger')
    return render_template('login.html', uin=uin, form=form)

@app.route('/logout', methods=['GET'])
def logout():
    """return landing page in response to logout"""
    logout_user()
    flash("See you later!", "success")
    return redirect(url_for('index'))

# @app.errorhandler(404)
# def not_found(error):
#     """return custom 404 page
#        return render_template("custom_404.html")
#      """
#     return ({error: "Page Not Found"}, 404)



# @app.after_request
# def handle_cors(response):
#     """cors"""
#     # allow access from other domains
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers',
#                          'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods',
#                          'GET,PUT,POST,DELETE,OPTIONS')
#     return response
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)