from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from textblob import TextBlob

# --- Flask setup ---
app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feedback.db'   # persistent DB file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# --- Models ---
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), default="user", index=True)  # "user" or "admin"

    feedbacks = db.relationship("Feedback", backref="user", lazy=True)

class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.String(10), index=True)  # Positive, Negative, Neutral

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
@login_required
def submit():
    message = request.form["message"]
    analysis = TextBlob(message)
    sentiment = "Positive" if analysis.sentiment.polarity > 0 else "Negative" if analysis.sentiment.polarity < 0 else "Neutral"

    fb = Feedback(user_id=current_user.id, message=message, sentiment=sentiment)
    db.session.add(fb)
    db.session.commit()
    flash("Feedback submitted successfully!")
    return redirect(url_for("index"))

@app.route("/view")
@login_required
def view():
    if current_user.role != "admin":
        return "Access denied"

    feedback = Feedback.query.all()
    pos = sum(1 for fb in feedback if fb.sentiment == "Positive")
    neg = sum(1 for fb in feedback if fb.sentiment == "Negative")
    neu = sum(1 for fb in feedback if fb.sentiment == "Neutral")
    sentiment_counts = [pos, neg, neu]

    return render_template("view.html", feedback=feedback, sentiment_counts=sentiment_counts)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and user.password == request.form["password"]:
            login_user(user)
            return redirect(url_for("index"))
        flash("Invalid credentials")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        new_user = User(username=request.form["username"], password=request.form["password"])
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please login.")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# --- Startup ---
if __name__ == "__main__":
    with app.app_context():
        db.create_all()   # ✅ tables created once at startup
    app.run(debug=True)
