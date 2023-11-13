from flask import Flask, render_template, request, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

RESPONSES_KEY = "responses"
survey = satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route("/")
def home_page():
    """survey home page"""
    return render_template("homepage.html",survey=survey)
    
@app.route("/start", methods=["POST"])
def start_survey():
    """starting the survey"""
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")

@app.route("/questions/<int:questnum>")
def show_question(questnum):
    """show question and collect answer to responses[]"""
    responses = session.get(RESPONSES_KEY)
    if len(responses) != questnum:
        """question is not in order"""
        flash(f"Invalid question Id: {questnum}.")
        return redirect(f"/questions/{len(responses)}")
    if len(responses) == len(survey.questions):
        """if answer all questions"""
        return redirect("/finish")
        
    question = survey.questions[questnum]
    return render_template("question.html",quest_num=questnum, question=question)

@app.route("/answer", methods=["POST"])
def save_answer():
    """save data to responses"""
    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses
    if len(responses) == len(survey.questions):
        return redirect("/finish")
    else:
        return redirect (f"/questions/{len(responses)}")

@app.route("/finish")
def thanks_user():
    """finish survey"""
    return render_template("finish.html")