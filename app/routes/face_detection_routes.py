from app import app
from flask import request, jsonify
from app.services.face_recognition_service import process_face

@app.route("/detect_face", methods=["POST"])
def detect_face():
    image_data = request.get_json()["image"]
    result = process_face(image_data)
    return jsonify(result)