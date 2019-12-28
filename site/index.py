__author__ = 'Naumov-Web'
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from models import Image
import base64
import os

app = Flask(__name__)

@app.route("/", methods=["POST", "GET", 'OPTIONS'])
def index_page():
  return render_template('index.html')

@app.route("/learning", methods=["POST", "GET", 'OPTIONS'])
def learning_page():
  return render_template('learning.html')

@app.route("/save-image", methods=["POST"])
def save_image():
  if request.method == 'POST':
    image_b64 = request.values['imageBase64']
    right_number = request.values['right']
    image_encoded = image_b64.split(',')[1]
    image_bin = base64.decodebytes(image_encoded.encode('utf-8'))
    image_model = Image()
    image_model.save(right_number, image_bin)

    return jsonify({'success': 1})

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=False)