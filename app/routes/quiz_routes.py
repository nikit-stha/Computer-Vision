from app import app
from flask import jsonify, request, redirect, render_template, url_for
from app.services.quiz_service import process_image

from app.services.quiz_service import add_new_question

#API Endpoint

@app.route("/API/quiz", methods = ["POST"])
def api_quiz():
    image_data = request.get_json()["image"]
    processed_image = process_image(image_data)

    return jsonify({
        "image" : processed_image
    })

@app.route('/add_question', methods = ["POST", "GET"])
def add_question():
    if request.method == "POST":
        question = request.form.get("question")
        option1 = request.form.get("option1")
        option2 = request.form.get("option2")
        option3 = request.form.get("option3")
        option4 = request.form.get("option4")

        answer = request.form.get("answer")

        sucess, message = add_new_question(
            question,
            option1,
            option2,
            option3,
            option4,
            answer
        )

        if sucess:
            return redirect(url_for("quiz"))
        
        return render_template(
            "add_new_question.html",
            question = question,
            option1= option1,
            option2= option2,
            option3= option3,
            option4= option4,
            answer = answer
        )
    
    question = request.args.get("question")
    option1 = request.args.get("option1")
    option2 = request.args.get("option2")
    option3 = request.args.get("option3")
    option4 = request.args.get("option4")
    answer = request.args.get("answer")

    return render_template(
        "add_new_question.html",
            question = question,
            option1= option1,
            option2= option2,
            option3= option3,
            option4= option4,
            answer = answer
        )