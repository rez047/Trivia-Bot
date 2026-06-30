**Trivia Bot with Online Question Fetching + Database + User Accounts + Scores**.

Stack:

* **Python**
* **Flask** (web app)
* **SQLite + SQLAlchemy** (database)
* **Requests API** (online random questions)
* **HTML/CSS**
* **Flask-Login** (sessions)

Project features:
✅ Register users
✅ Login/logout
✅ Store user profile
✅ Fetch random trivia questions online
✅ Show multiple choice answers
✅ Check answers
✅ Store scores
✅ User history
✅ Database models

---

TRIVIA BOT WEB APPLICATION

## STEP 1 - Project Setup and Flask Foundation

## 1. Create project folder

```
TriviaBot/
│
├── app.py
├── models.py
├── database.db
│
├── templates/
│   ├── base.html
│   ├── history.html
│   ├── register.html
│   ├── login.html
│   ├── quiz.html
│   └── result.html
│
└── static/
    └── style.css
```

---

## 2. Install requirements

Create:

`requirements.txt`

```txt
Flask
Flask-SQLAlchemy
Flask-Login
requests
werkzeug
```

Install:

```bash
pip install -r requirements.txt
```

---

# Understanding the Tools

## Flask

Used to create web pages and handle requests.

Example:

```python
@app.route("/")
def home():
    return "Hello"
```

When a user visits:

```
localhost:5000
```

Flask runs that function.

---

## SQLAlchemy

Allows Python to communicate with databases.

Instead of:

```sql
SELECT * FROM users
```

we use:

```python
User.query.all()
```

---

# Part 2 — Create Database

## models.py

```python
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class User(UserMixin, db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(50),
        unique=True
    )

    email = db.Column(
        db.String(100),
        unique=True
    )

    password = db.Column(
        db.String(200)
    )

    score = db.Column(
        db.Integer,
        default=0
    )



class QuizHistory(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer
    )

    question = db.Column(
        db.String(300)
    )

    correct = db.Column(
        db.String(200)
    )

    answer = db.Column(
        db.String(200)
    )

```

---

## Explanation

User table:

| field    | purpose            |
| -------- | ------------------ |
| id       | unique user number |
| username | login name         |
| email    | account email      |
| password | encrypted password |
| score    | total points       |

QuizHistory stores every attempt.

---

# STEP 2 — User Authentication

## app.py

```python
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

```

# Register Page

```python
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
```

---

# Login

```python
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
```

---

# STEP 3 — Online Trivia API

We use:

```
https://opentdb.com
```

It gives free questions.

Example response:

```json
{
"question":
"What is Python?",

"correct_answer":
"Programming Language"
}
```

---

## Fetch Questions

```python
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
```

---

# Quiz Route

```python
@app.route("/quiz")
@login_required
def quiz():


    question=get_question()


    return render_template(
    "quiz.html",
    question=question
    )
```

---

# Checking Answers

```python

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
## Create database


with app.app_context():

    db.create_all()


if __name__ == "__main__":

    app.run(
        debug=True
    )


  
```

---

# STEP 4 — Frontend

## quiz.html

<!DOCTYPE html>

<html>

<head>

<title>Trivia Bot</title>


<style>

*{
    box-sizing:border-box;
    font-family:Segoe UI, Arial;
}


body{

    min-height:100vh;
    margin:0;

    background:
    radial-gradient(circle at top,#263238,#050505);

    color:white;

    display:flex;
    justify-content:center;
    align-items:center;

}



.quiz-box{

    width:700px;

    background:#111827;

    padding:40px;

    border-radius:20px;

    box-shadow:
    0 0 30px #00ffcc55;

}



h1{

    text-align:center;

    color:#00ffc8;

}



.score{

    text-align:center;

    font-size:22px;

    margin-bottom:25px;

}



.question{

    background:#1f2937;

    padding:25px;

    border-radius:15px;

    font-size:22px;

    margin-bottom:25px;

}



.answer-btn{


    width:100%;

    padding:15px;

    margin:10px 0;

    border:none;

    border-radius:12px;

    background:#374151;

    color:white;

    font-size:18px;

    cursor:pointer;

    transition:0.3s;

}



.answer-btn:hover{

    background:#00ffc8;

    color:black;

    transform:scale(1.03);

}



.correct{

    background:#16a34a !important;

}



.wrong{

    background:#dc2626 !important;

}



.next{


margin-top:20px;

display:block;

text-align:center;

background:#00ffc8;

color:black;

padding:14px;

border-radius:10px;

text-decoration:none;


}



</style>


</head>



<body>


<div class="quiz-box">



<h1>
🤖 Trivia Bot
</h1>



<div class="score">

Score:
{{current_user.score}}

</div>



<div class="question">

{{question.question | safe}}

</div>




<form method="POST" action="/answer">



<input type="hidden"
name="question"
value="{{question.question}}">



<input type="hidden"
name="correct"
value="{{question.correct_answer}}">





{% for a in question.incorrect_answers %}


<button

class="answer-btn"

name="answer"

value="{{a}}">


{{a | safe}}


</button>


{% endfor %}






<button

class="answer-btn"

name="answer"

value="{{question.correct_answer}}">


{{question.correct_answer | safe}}


</button>





</form>


</div>


</body>


</html>
```




## result.html

<!DOCTYPE html>

<html>

<head>

<title>Result</title>


<style>

body{

background:#050505;

color:white;

font-family:Segoe UI;

display:flex;

justify-content:center;

padding:40px;

}



.card{

width:650px;

background:#111827;

padding:40px;

border-radius:20px;

box-shadow:0 0 30px #00ffc855;

}



.answer{

padding:15px;

margin:10px;

border-radius:12px;

}



.correct{

background:#16a34a;

}



.wrong{

background:#dc2626;

}



.normal{

background:#374151;

}



a{

display:block;

background:#00ffc8;

color:black;

padding:15px;

text-align:center;

border-radius:12px;

text-decoration:none;

margin-top:20px;

}



</style>

</head>


<body>


<div class="card">


<h1>

{% if is_correct %}

🎉 Correct!

{% else %}

❌ Wrong

{% endif %}


</h1>



<h2>

{{question | safe}}

</h2>




<div class="answer correct">

Correct answer:

{{correct | safe}}

</div>




{% if chosen != correct %}


<div class="answer wrong">


Your answer:

{{chosen | safe}}


</div>


{% endif %}




<a href="/quiz">

Next Question

</a>



<a href="/history">

View Previous Results

</a>


</div>


</body>

</html>


# register.html

<!DOCTYPE html>

<html>

<head>
<title>Register</title>
</head>


<body>

<h1>Create Account</h1>


<form method="POST">


<input 
name="username"
placeholder="Username"
required>


<br><br>


<input 
name="email"
placeholder="Email"
required>


<br><br>


<input 
type="password"
name="password"
placeholder="Password"
required>


<br><br>


<button>
Register
</button>


</form>


<a href="/login">
Already have account?
</a>


</body>

</html>


# login.html

<!DOCTYPE html>

<html>

<head>

<title>
Login
</title>

</head>


<body>


<h1>
Login
</h1>



<form method="POST">


<input
name="email"
placeholder="Email"
required>


<br><br>


<input
type="password"
name="password"
placeholder="Password"
required>


<br><br>


<button>
Login
</button>


</form>



<a href="/register">
Create account
</a>



</body>

</html>



## history.html
<!DOCTYPE html>

<html>

<head>

<title>
Quiz History
</title>


<style>

*{
    box-sizing:border-box;
    font-family:Segoe UI, Arial;
}


body{

    margin:0;

    min-height:100vh;

    background:
    radial-gradient(circle at top,#1e293b,#020617);

    color:white;

    padding:40px;

}



.container{

    max-width:900px;

    margin:auto;

}



h1{

    text-align:center;

    color:#00ffc8;

}



.history-card{


    background:#111827;

    margin:20px 0;

    padding:25px;

    border-radius:18px;

    box-shadow:
    0 0 20px #000;


}



.question{

    font-size:20px;

    margin-bottom:20px;

}



.correct{

    background:#16a34a;

    padding:12px;

    border-radius:10px;

    margin:10px 0;

}



.wrong{

    background:#dc2626;

    padding:12px;

    border-radius:10px;

    margin:10px 0;

}



.back{


display:block;

text-align:center;

background:#00ffc8;

color:black;

padding:15px;

border-radius:12px;

text-decoration:none;

margin-top:30px;


}



.empty{

text-align:center;

color:#aaa;

}


</style>


</head>



<body>


<div class="container">


<h1>
📚 Previous Answers
</h1>




{% if records %}



{% for r in records %}



<div class="history-card">


<div class="question">

{{r.question | safe}}

</div>



<div class="correct">


Correct Answer:

{{r.correct | safe}}


</div>




{% if r.answer == r.correct %}



<div class="correct">

Your Answer:

{{r.answer | safe}}

✔ Correct

</div>



{% else %}



<div class="wrong">


Your Answer:

{{r.answer | safe}}

✘ Wrong


</div>



{% endif %}



</div>



{% endfor %}



{% else %}


<div class="empty">

No quiz attempts yet.

</div>


{% endif %}




<a class="back" href="/quiz">

Back To Quiz

</a>



</div>


</body>

</html>



---

# style.css  

```css
body{

font-family:Arial;

text-align:center;

background:#222;

color:white;

}


button{

padding:15px;

margin:10px;

cursor:pointer;

}
```

---

# Running

Terminal:

```bash
python app.py
```

Open:

```
localhost:5000
```

---

# What I Learn

## Python

* classes
* functions
* imports
* APIs
* JSON

## Database

* tables
* relationships
* CRUD

## Web

* routes
* templates
* forms

## Security

* password hashing
* sessions


