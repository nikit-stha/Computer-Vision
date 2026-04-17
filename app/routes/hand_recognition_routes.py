from app import app
from flask import render_template, request, redirect, jsonify
from app.services.hand_recognition_services import process_hand_image

@app.route("/detect_hand", methods=["POST"])
def detect_hand():
    image_data = request.get_json()["image"]
    processed_image = process_hand_image(image_data)

    return jsonify({
        "image": processed_image
    })