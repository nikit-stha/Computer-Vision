from app import app
from flask import request, redirect, render_template, jsonify
from app.services.qr_code_services import process_barcode

@app.route('/API/detect_qr', methods = ["POST"])
def detect_qr():
    image_data = request.get_json()["image"]
    processed_image = process_barcode(image_data)

    return jsonify({
        "image": processed_image
    })