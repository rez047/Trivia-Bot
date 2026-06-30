from flask import *

from flask_sqlalchemy import SQLAlchemy

from flask_login import *

from werkzeug.security import generate_password_hash, check_password_hash

import requests



from models import db,User,QuizHistory



app = Flask(__name__)


app.config["SECRET_KEY"]="secretkey"


app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"



db.init_app(app)


login_manager=LoginManager()

login_manager.init_app(app)



@login_manager.user_loader
def load_user(id):

    return User.query.get(int(id))


@app.route("/")
def home():

    return """
    <h1>Trivia Bot</h1>

    <a href='/register'>Register</a>
    <br>
    <a href='/login'>Login</a>
    """


@app.route("/register",methods=["GET","POST"])
def register():


    if request.method=="POST":


        user=User(

        username=request.form["username"],

        email=request.form["email"],

        password=
        generate_password_hash(
        request.form["password"]
        )

        )


        db.session.add(user)

        db.session.commit()


        return redirect("/login")


    return render_template(
    "register.html"
    )

@app.route("/login",
methods=["GET","POST"])
def login():


    if request.method=="POST":


        user=User.query.filter_by(
        email=request.form["email"]
        ).first()


        if user and check_password_hash(
        user.password,
        request.form["password"]
        ):


            login_user(user)

            return redirect("/quiz")



    return render_template("login.html")


def get_question():

    url = (
        "https://opentdb.com/api.php"
        "?amount=1&type=multiple"
    )


    response = requests.get(url)


    data = response.json()


    if data["response_code"] != 0:

        return {

            "question": "No question available, try again",

            "correct_answer": "OK",

            "incorrect_answers": []

        }


    q = data["results"][0]


    return q


@app.route("/quiz")
@login_required
def quiz():


    question=get_question()


    return render_template(
    "quiz.html",
    question=question
    )



@app.route("/answer", methods=["POST"])
@login_required
def answer():


    chosen = request.form["answer"]

    correct = request.form["correct"]

    question = request.form["question"]


    is_correct = chosen == correct


    if is_correct:

        current_user.score += 10



    history = QuizHistory(

        user_id=current_user.id,

        question=question,

        correct=correct,

        answer=chosen

    )


    db.session.add(history)

    db.session.commit()



    return render_template(
        "result.html",
        question=question,
        chosen=chosen,
        correct=correct,
        is_correct=is_correct
    )


@app.route("/leaderboard")
def leaderboard():


    users=User.query.order_by(
    User.score.desc()
    ).all()


    return render_template(
    "leaderboard.html",
    users=users
    )


@app.route("/history")
@login_required
def history():

    records = QuizHistory.query.filter_by(
        user_id=current_user.id
    ).all()


    return render_template(
        "history.html",
        records=records
    )


with app.app_context():

    db.create_all()


if __name__ == "__main__":

    app.run(
        debug=True
    )


