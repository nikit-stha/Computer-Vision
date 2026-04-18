import json
from flask import render_template, request, redirect, url_for
from app import app




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

@app.route("/face")
def face_detection():
    return render_template("face_detection.html")

@app.route("/volume_control")
def volume_control():
    return render_template("volume_control.html")

@app.route('/quiz')
def quiz():
    return render_template("quiz.html")



