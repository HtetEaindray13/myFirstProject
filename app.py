import cv2
import dlib
import numpy as np
import base64
import flask
from flask import Flask, request, jsonify, render_template
from io import BytesIO
from PIL import Image

app = Flask(__name__)
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def decode_image(image_data):
    image_data = base64.b64decode(image_data.split(',')[1])
    image = Image.open(BytesIO(image_data))
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

def detect_faces_and_eyes(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    face_data = []

    for face in faces:
        landmarks = predictor(gray, face)
        eyes = [(landmarks.part(n).x, landmarks.part(n).y) for n in range(36, 48)]
        face_data.append({
            "face": [face.left(), face.top(), face.right(), face.bottom()],
            "eyes": eyes
        })

    return face_data

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/process', methods=['POST'])
def process_frame():
    data = request.get_json()
    image = decode_image(data['image'])
    face_data = detect_faces_and_eyes(image)
    return jsonify(face_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

