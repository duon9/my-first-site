from flask import Flask, render_template, send_from_directory, request , url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user 

app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "nsfEFefa43fAFafx6"


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
 
 
db.init_app(app)
 
with app.app_context():
    db.create_all()

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/movies')
def movies():
    return render_template('movies.html')

@app.route('/movies/<name>')
def player(name):
    return render_template("player.html", name = name)

@app.route('/tvshows')
def tvshows():
    return render_template('tvshows.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(
            username = request.form.get("username")
        ).first()

        if user.password == request.form.get("password"):
            login_user(user)
            return redirect(url_for("home"))

    return render_template('login.html')

@app.route('/signup', methods = ["GET", "POST"])
def signup():
    if (request.method == "POST"):
        user = Users(username = request.form.get("username"),
                     password = request.form.get("password"))
        
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template('signup.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/images', filename)

if __name__ == '__main__':
    app.run(debug=True)