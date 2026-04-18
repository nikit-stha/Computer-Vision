from app import app
from flask import request, jsonify, render_template, url_for, redirect
from app.services.face_recognition_service import process_face

from app.services.face_recognition_service import register_face_from_temp

@app.route("/detect_face", methods=["POST"])
def detect_face():
    image_data = request.get_json()["image"]
    result = process_face(image_data)
    return jsonify(result)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        temp_face_filename = request.form.get("temp_face_filename")
        face_location = request.form.get("face_location")

        success, message = register_face_from_temp(
            username,
            temp_face_filename,
            face_location
        )

        if success:
            return redirect(url_for("face_detection"))

        return render_template(
            "register.html",
            face=temp_face_filename,
            face_location=face_location
        )

    face = request.args.get("face")
    face_location = request.args.get("location")

    return render_template(
        "register.html",
        face=face,
        face_location=face_location
    )