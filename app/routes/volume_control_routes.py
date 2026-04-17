from app import app
from flask import request, redirect, render_template, jsonify
from app.services.volume_control_services import process_hand_image

@app.route('/volume_control_json', methods = ["GET", "POST"])
def volume_control_json():
    image_data = request.get_json()["image"]
    processed_image = process_hand_image(image_data)

    return jsonify({
        "image": processed_image
    })