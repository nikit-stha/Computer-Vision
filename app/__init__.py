import os

from flask import Flask, redirect, render_template, jsonify

from app.extensions import app, db

from app.models.qr_model import QR
from app.models.user_model import User

from app.routes import hand_recognition_routes
from app.routes import qr_code_routes
from app.routes import main_routes
from app.routes import face_detection_routes