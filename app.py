from flask import Flask, render_template, send_from_directory, request, url_for, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "nsfEFefa43fAFafx6"

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

@login_manager.user_loader
def load_user(user_id):
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
    return render_template("player.html", name=name)

@app.route('/tvshows')
def tvshows():
    return render_template('tvshows.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Users.query.filter_by(username=username).first()
        
        if user and user.password == password:
            login_user(user)
            flash("Logged in successfully!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for("login"))

    return render_template('login.html')

@app.route('/api/login', methods=["POST"])
def api_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = Users.query.filter_by(username=username).first()

    if user and user.password == password:
        login_user(user)
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = Users(username=username, password=password)
        
        db.session.add(user)
        db.session.commit()
        
        flash("Registered successfully! Please log in.", "success")
        return redirect(url_for("login"))

    return render_template('signup.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "success")
    return redirect(url_for("home"))

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('static/images', filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create all tables defined in the models
    app.run(debug=True)
