from flask import Flask, render_template, request, session, redirect, url_for
import random, json

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Load questions
with open("questions.json") as f:
    QUESTIONS = json.load(f)

TOTAL_Q = 30


# =========================
# HOME (START PAGE)
# =========================
@app.route("/")
def home():
    return render_template("start.html")


# =========================
# START EXAM
# =========================
@app.route("/start", methods=["POST"])
def start_exam():
    name = request.form.get("username")

    session.clear()
    session["name"] = name
    session["questions"] = random.sample(QUESTIONS, TOTAL_Q)
    session["answers"] = [-1] * TOTAL_Q   # pre-fill

    return redirect(url_for("quiz", qn=0))


# =========================
# QUIZ
# =========================
@app.route("/quiz/<int:qn>", methods=["GET", "POST"])
def quiz(qn):

    if "questions" not in session:
        return redirect(url_for("home"))

    if qn >= TOTAL_Q:
        return redirect(url_for("result"))

    if request.method == "POST":
        ans = request.form.get("answer")

        answers = session["answers"]

        if ans is not None:
            answers[qn] = int(ans)

        session["answers"] = answers
        session.modified = True

        return redirect(url_for("quiz", qn=qn + 1))

    q = session["questions"][qn]

    return render_template(
        "quiz.html",
        q=q,
        qn=qn,
        total=TOTAL_Q,
        answers=session["answers"],
        name=session.get("name", "User")
    )


# =========================
# RESULT
# =========================
@app.route("/result")
def result():

    questions = session.get("questions", [])
    answers = session.get("answers", [])

    correct = 0
    result_data = []

    for q, a in zip(questions, answers):
        is_correct = a == q["correct"]
        if is_correct:
            correct += 1

        result_data.append({
            "q": q["q"],
            "correct": q["options"][q["correct"]],
            "your": q["options"][a] if a != -1 else "Not Answered",
            "status": is_correct
        })

    score = round((correct / TOTAL_Q) * 100, 2)

    return render_template(
        "result.html",
        results=result_data,
        score=score,
        correct=correct,
        total=TOTAL_Q,
        name=session.get("name", "User")
    )


if __name__ == "__main__":
    app.run(debug=True)