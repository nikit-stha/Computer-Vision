import json
from flask import render_template, request, redirect, url_for
from app import app
from app.services.face_recognition_service import register_face_from_temp

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")
@app.route("/hand")
def camera():
    return render_template("hand.html")

@app.route('/qr')
def qr():
    return render_template('qr.html')

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

@app.route("/face")
def face_detection():
    return render_template("face_detection.html")

@app.route("/volume_control")
def volume_control():
    return render_template("volume_control.html")