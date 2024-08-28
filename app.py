import secrets

from flask import Flask, redirect, render_template, request, session, url_for

from models import Question, Quiz, db

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def index():
    return redirect("home")


@app.route("/home")
def home():
    quizzes = Quiz.query.all()
    return render_template("home.html", quiz_ids=[quiz.id for quiz in quizzes])


@app.route("/quiz/<int:quiz_id>")
def quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template("quiz.html", quiz=quiz)


@app.route("/submit")
def submit():
    quiz_id = request.args.get("quiz_id")
    quiz = Quiz.query.get_or_404(quiz_id)
    answers = request.args.to_dict()
    answers.pop("quiz_id", None)
    # in case some questions haven't been answered.
    res = len(quiz.questions) - len(answers)
    for k, a in answers.items():
        if quiz.questions[int(k)].correct_answer != int(a):
            res += 1
    res = 1 - res / len(quiz.questions)
    res = int(res * 100)  # from a fraction to a percentage.
    if "best" in session:
        session["best"] = max(session["best"], res)
    else:
        session["best"] = res
    return redirect(url_for("score", score=res))


@app.route("/score")
def score():
    score = request.args.get("score")
    if score is None:
        redirect("home")
    return render_template("score.html", score=score)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port="4040")
