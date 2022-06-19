 import os
from datetime import datetime

import flask
import numpy as np
import pandas as pd
from flask import render_template, request, session
from werkzeug.utils import secure_filename

from src import app
from src.objective import ObjectiveTest
from src.subjective import SubjectiveTest
from src.utils import backup, relative_ranking

# Placeholders
global_answers = list()


@app.route('/')
@app.route('/home')
def home():
    ''' Renders the home page '''
    directory = os.path.join(str(os.getcwd()), "database")
    session["database_path"] = os.path.join(str(os.getcwd()), "database", "userlog.csv")
    if "userlog.csv" not in os.listdir(directory):
        df = pd.DataFrame(columns=["DATE", "USERNAME", "SUBJECT", "SUBJECT_ID", "TEST_TYPE", "TEST_ID", "SCORE", "RESULT"])
        df.to_csv(session["database_path"], index=False)
    else:
        print("Database in place!")
    session["date"] = datetime.now()
    return render_template(
        "index.html",
        date=session["date"].day,
        month=session["date"].month,
        year=session["date"].year
    )


@app.route("/form", methods=['GET', 'POST'])
def form():
    ''' Prompt user to start the test '''
    if request.form["username"] == "":
        session["username"] = "Username"
    else:
        session["username"] = request.form["username"]
    return render_template(
        "form.html",
        username=session["username"]
    )


@app.route("/generate_test", methods=["GET", "POST"])
def generate_test():
    session["subject_id"] = request.form["subject_id"]
    if session["subject_id"] == "0":
        session["subject_name"] = "SOFTWARE ENGINEERING"
        session["filepath"] = os.path.join(str(os.getcwd()), "corpus", "software-testing.txt")
    elif session["subject_id"] == "1":
        session["subject_name"] = "DBMS"
        session["filepath"] = os.path.join(str(os.getcwd()), "corpus", "dbms.txt")
    elif session["subject_id"] == "2":
        session["subject_name"] = "Machine Learning"
        session["filepath"] = os.path.join(str(os.getcwd()), "corpus", "ml.txt")
    elif session["subject_id"] == "99":
        file = request.files["file"]
        session["filepath"] = secure_filename(file.filename)
        file.save(secure_filename(file.filename))
        session["subject_name"] = "CUSTOM"
    else:
        print("Done!")
    session["test_id"] = request.form["test_id"]

    if session["test_id"] == "0":
        # Generate objective test
        objective_generator = ObjectiveTest(session["filepath"])
        question_list, answer_list = objective_generator.generate_test()
        for ans in answer_list:
            global_answers.append(ans)

        return render_template(
            "objective_test.html",
            username=session["username"],
            testname=session["subject_name"],
            question1=question_list[0],
            question2=question_list[1],
            question3=question_list[2]
        )
    elif session["test_id"] == "1":
        # Generate subjective test
        subjective_generator = SubjectiveTest(session["filepath"])
        question_list, answer_list = subjective_generator.generate_test(num_questions=2)
        for ans in answer_list:
            global_answers.append(ans)

        return render_template(
            "subjective_test.html",
            username=session["username"],
            testname=session["subject_name"],
            question1=question_list[0],
            question2=question_list[1]
        )
    else:
        print("Done!")
        return None


@ app.route("/output", methods=["GET", "POST"])
def output():
    default_ans = list()
    user_ans = list()
    if session["test_id"] == "0":
        # Access objective answers
        user_ans.append(str(request.form["answer1"]).strip().upper())
        user_ans.append(str(request.form["answer2"]).strip().upper())
        user_ans.append(str(request.form["answer3"]).strip().upper())
    elif session["test_id"] == "1":
        # Access subjective answers
        user_ans.append(str(request.form["answer1"]).strip().upper())
        user_ans.append(str(request.form["answer2"]).strip().upper())
    else:
        print("Done!")

    # Process answers
    for x in global_answers:
        default_ans.append(str(x).strip().upper())

    # Evaluate the user repsonse
    total_score = 0
    status = None
    if session["test_id"] == "0":
        # Evaluate objective answer
        for i, _ in enumerate(user_ans):
            if user_ans[i] == default_ans[i]:
                total_score += 100
        total_score /= 3
        total_score = round(total_score, 3)
        if total_score >= 33.33:
            status = "Pass"
        else:
            status = "Fail"
    elif session["test_id"] == "1":
        # evaluate subjective answer
        for i, _ in enumerate(default_ans):
            # Subjective test
            subjective_generator = SubjectiveTest(session["filepath"])
            total_score += subjective_generator.evaluate_subjective_answer(default_ans[i], user_ans[i])
        total_score /= 2
        total_score = round(total_score, 3)
        if total_score > 50.0:
            status = "Pass"
        else:
            status = "Fail"
    # Backup data
    session["score"] = np.round(total_score, decimals=2)
    session["result"] = status
    try:
        status = backup(session)
    except Exception as e:
        print("Exception raised at `views.__output`:", e)
    # Compute relative ranking of the student
    max_score, min_score, mean_score = relative_ranking(session)
    # Clear instance
    global_answers.clear()

    # Render output
    return render_template(
        "output.html",
        show_score=session["score"],
        username=session["username"],
        subjectname=session["subject_name"],
        status=session["result"],
        max_score=max_score,
        min_score=min_score,
        mean_score=mean_score
    )
