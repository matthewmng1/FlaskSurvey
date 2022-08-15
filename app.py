from flask import Flask, request, render_template, redirect, flash, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES_KEY = "responses" #answers to survey should go here



@app.route('/')
def home():
    return render_template('home.html') # homepage



@app.route('/survey')
def survey():
    return render_template('survey.html', survey=survey) #goes to Satisfaction Survey



@app.route('/start', methods=['POST'])
def start():
    session[RESPONSES_KEY] = []
    return redirect('/questions/0')



@app.route("/answer", methods=["POST"])
def handle_question():

    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.question)):
        return redirect("/complete")

    else:
        return redirect(f"/questions/{len(responses)}")



@app.route('/questions/<int:qid>')
def show_question(qid):
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.question)):
        return redirect("/complete")

    if (len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)