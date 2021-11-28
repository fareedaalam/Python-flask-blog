# from os import abort
import math
import os
from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
from Models.Models import db, Contacts, Posts
import json
from flask_mail import Mail, Message

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# read config file
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)

# file upload config
root_dir = os.path.dirname(app.instance_path) + params['file_upload_path']
app.config['UPLOAD_FOLDER'] = os.path.join(root_dir)
# user when session required
app.secret_key = "super_secret_key"
# set smtp mail
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT='465',
    MAIL_USE_SSL=True,
    MAIL_USERNAME=params['gmail-user'],
    MAIL_PASSWORD=params['gmail-pwd']
)
mail = Mail(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()


# @app.errorhandler(Exception)
# def handle_exception(e):
#     # pass through HTTP errors
#     if isinstance(e, HTTPException):
#         return e
#
#     # now you're handling non-HTTP exceptions only
#     return render_template("500_generic.html", e=e), 500

@app.route('/')
def home_page():
    posts = Posts.query.filter_by().all()
    last = math.ceil(len(posts) / int(params['no_of_posts']))
    page = request.args.get('page')
    # if not str(page).isnumeric():
    if page is None:
        page = 1

    page = int(page)
    posts = posts[(page - 1) * int(params['no_of_posts']): (page - 1) * int(params['no_of_posts']) + int(
        params['no_of_posts'])]
    # pagination logic
    if page == 1:
        prev = "#"
        next = "/?page=" + str(page + 1)
    elif page == last:
        prev = "/?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/?page=" + str(page - 1)
        next = "/?page=" + str(page + 1)

    return render_template('index.html', params=params, posts=posts, next=next, prev=prev)


@app.route('/delete/<string:sn>', methods=['GET', 'POST'])
def delete(sn):
    if 'user' in session and session['user'] == params['admin_user']:
        _post = Posts.query.filter_by(sn=sn).first()
        img_path = params['file_upload_path'] + _post.img_url
        print(img_path)
        if os.path.exists(img_path):
            os.remove(img_path)
        db.session.delete(_post)
        db.session.commit()
        return redirect('/dashboard')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print('testing url', request.url)
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            _post = Posts()
            _post.img_url = filename
            _post.title = ''
            _post.muted_text = ''
            _post.slug = ''
            _post.content = ''
            return render_template('edit.html', params=params, post=_post)

    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/dashboard ')


@app.route('/edit/<string:sn>', methods=['GET', 'POST'])
def edit(sn):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                print('file not exists')

            file = request.files['file']
            # If the user does not select a file
            if file.filename == '':
                flash('No selected file')

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                _title = request.form.get('title')
                _muted_text = request.form.get('muted_text')
                _slug = request.form.get('slug')
                _img_url = file.filename  # request.form.get('img_url')
                _content = request.form.get('content')
                _by = session['user']

                if sn == '0':
                    _post = Posts(title=_title, muted_text=_muted_text, slug=_slug, img_url=_img_url, content=_content,
                                  created_by=_by)
                    db.session.add(_post)
                    db.session.commit()
                else:
                    post = Posts.query.filter_by(sn=sn).first()
                    post.title = _title
                    post.muted_text = _muted_text
                    post.slug = _slug
                    post.img_url = _img_url
                    post.content = _content
                    post.created_by = _by
                    db.session.commit()
                    return redirect('/dashboard')

        if request.method == 'GET':
            edit_rec = Posts.query.filter_by(sn=sn).first()
            if edit_rec:
                return render_template('edit.html', params=params, sn=sn, post=edit_rec)
            else:
                edit_rec = Posts
                edit_rec.title = ''
                edit_rec.muted_text = ''
                edit_rec.content = ''
                edit_rec.img_url = ''
                edit_rec.slug=''
                return render_template('edit.html', params=params, sn=sn, post=edit_rec)

    return render_template('edit.html', params=params, post=Posts)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user' in session and session['user'] == params['admin_user']:
        login_user = session['user']
        post = Posts.query.all()
        return render_template('dashboard.html', params=params, post_data=post, login_user=login_user)
        # return render_template('dashboard.html', params=params, post_data=post)

    if request.method == 'POST':
        user = request.form.get('uname')
        pwd = request.form.get('pwd')
        if user == params['admin_user'] and pwd == params['admin_pwd']:
            # set the session variable
            session['user'] = user
            post = Posts.query.all()
            return render_template('dashboard.html', params=params, post_data=post)

    return render_template('login.html', params=params)


@app.route('/about')
def about():
    return render_template('about.html', params=params)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'GET':
        return render_template('contact.html', params=params)

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        contact_no = request.form['contact_no']
        message = request.form['message']
        contacts_data = Contacts(name=name, email=email, contact_no=contact_no, message=message)
        db.session.add(contacts_data)
        db.session.commit()
        msg = Message('New message from ' + email,
                      recipients=[params['gmail-user']],
                      sender=email,
                      body=message + "\n" + contact_no
                      )
        mail.send(msg)
        flash('Query Has been Acknowledged Successfully', 'success')

        return render_template('contact.html', params=params)


@app.route("/post/<string:post_slug>", methods=['GET'])
def post_route(post_slug):
    post = Posts.query.filter_by(slug=post_slug).first()
    if post:
        return render_template('post.html', params=params, post=post)
    else:
        post = Posts
        post.title = ''
        post.muted_text = ''
        post.content = ''
        post.img_url = ''
        post.slug = ''
        return render_template('post.html', params=params, post=post)



# this is another test CRUD process
# @app.route('/data/create', methods=['GET', 'POST'])
# def create():
#     if request.method == 'GET':
#         return render_template('create.html')
#
#     if request.method == 'POST':
#         employee_id = request.form['employee_id']
#         name = request.form['name']
#         age = request.form['age']
#         position = request.form['position']
#         employee = EmployeeModel(employee_id=employee_id, name=name, age=age, position=position)
#         db.session.add(employee)
#         db.session.commit()
#
#     return redirect('/data')
#
#
# @app.route('/data')
# def RetrieveList():
#     employees = EmployeeModel.query.all()
#     return render_template('datalist.html', employees=employees)
#
#
# @app.route('/data/<int:id>')
# def RetrieveEmployee(id):
#     employee = EmployeeModel.query.filter_by(employee_id=id).first()
#     if employee:
#         return render_template('data.html', employee=employee)
#     return f"Employee with id ={id} Doenst exist"
#
#
# @app.route('/data/<int:id>/update', methods=['GET', 'POST'])
# def update(id):
#     employee = EmployeeModel.query.filter_by(employee_id=id).first()
#     if request.method == 'POST':
#         if employee:
#             db.session.delete(employee)
#             db.session.commit()
#             name = request.form['name']
#             age = request.form['age']
#             position = request.form['position']
#             employee = EmployeeModel(employee_id=id, name=name, age=age, position=position)
#             db.session.add(employee)
#             db.session.commit()
#             return redirect(f'/data/{id}')
#         return f"Employee with id = {id} Does nit exist"
#
#     return render_template('update.html', employee=employee)
#
#
# @app.route('/data/<int:id>/delete', methods=['GET', 'POST'])
# def delete(id):
#     employee = EmployeeModel.query.filter_by(employee_id=id).first()
#     if request.method == 'POST':
#         if employee:
#             db.session.delete(employee)
#             db.session.commit()

#             return redirect('/data')
#         abort(404)
#
#     return render_template('delete.html')


app.run(host='localhost', port=5000, debug=True)
