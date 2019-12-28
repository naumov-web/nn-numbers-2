__author__ = 'Naumov-Web'
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from models import Image as ImageModel
from PIL import Image
import numpy as np
from keras.models import load_model
import pickle
import base64
import os

# Constants
BASE_SIZE = 80
MAX_SIZE = 100

app = Flask(__name__)

model_path = os.path.dirname(os.path.realpath(__file__)) + '/../network/clever_model.bin'
labels_path = os.path.dirname(os.path.realpath(__file__)) + '/../network/labels.bin'
model = None
lb = None
if os.path.exists(model_path):
  model = load_model(model_path)
  lb = pickle.loads(open(labels_path, "rb").read())


@app.route("/", methods=["POST", "GET", 'OPTIONS'])
def index_page():
  return render_template('index.html')

@app.route("/learning", methods=["POST", "GET", 'OPTIONS'])
def learning_page():
  return render_template('learning.html')

@app.route("/parse", methods=["POST", "GET", 'OPTIONS'])
def parse_page():
  return render_template('parse.html')

@app.route("/check-image", methods=["POST"])
def check_image():
  if request.method == 'POST':
    if model == None:
      return jsonify({'success': 0})

    image_b64 = request.values['imageBase64']
    image_encoded = image_b64.split(',')[1]
    image_bin = base64.decodebytes(image_encoded.encode('utf-8'))

    image_model = ImageModel()
    temp_path = image_model.save_temp(image_bin)

    return jsonify({'success': 1})

@app.route("/save-image", methods=["POST"])
def save_image():
  if request.method == 'POST':
    image_b64 = request.values['imageBase64']
    right_number = request.values['right']
    image_encoded = image_b64.split(',')[1]
    image_bin = base64.decodebytes(image_encoded.encode('utf-8'))
    image_model = ImageModel()
    image_model.save(right_number, image_bin)

    return jsonify({'success': 1})

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=False)