from flask import Flask, render_template, request, session, redirect, flash
from app import app
from app.models.Recipe import Recipe
from app.models.User import User
from ﬂask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/', methods=['GET'])
def index():
    if 'user' in session:
        print("USER DELETED")
        session.pop('user', None)
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def process():
    if request.method == 'POST':

        if not User.validate_register(request.form):
            return redirect("/")

        pw_hash = bcrypt.generate_password_hash(request.form['password'])

        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'password': pw_hash,
            'email': request.form['email'],
            'user_location': request.form['user_location'],
            'fav_food': request.form['fav_food'],
            'position': request.form['position'],
            'genre': request.form['genre']
        }
        print(data)

        user_id = User.insert(data)
        session["user"] = {"email": data['email'],
                           "id": user_id, "first_name": data['first_name']}

        print("USER_ID => ", user_id, session)
        return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def login():
    data = {"email": request.form['email']}
    user_db = User.exists(data)

    if not user_db:
        flash("Invalid Email/Password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_db.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect("/")

    session["user"] = {"id": user_db.user_id,
                       "email": user_db.email, "first_name": user_db.first_name}
    print("USER_DB_LOGIN => ", user_db.email, user_db.user_id)
    print("SESSION =>", session)

    return redirect("/dashboard")


@app.route('/dashboard', methods=['GET'])
def results():
    if 'user' in session:
        data = {"email": session['user']['email']}
        user_db = User.exists(data)
        recipes = Recipe.get_all()
        return render_template('dashboard.html', user=user_db, recipes=recipes)
    return redirect("/")
