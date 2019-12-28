import os
from PIL import Image
import numpy as np
from keras.models import load_model
import pickle
import argparse

# Constants
BASE_SIZE = 80
MAX_SIZE = 100

def transform_image(image):
    image_bin = image.resize((MAX_SIZE, MAX_SIZE))

    # 2. Выделяем значащую часть
    bbox = Image.eval(image_bin, lambda px: 255 - px).getbbox()
    if bbox == None:
        return None
    # Оригинальные длины сторон
    widthlen = bbox[2] - bbox[0]
    heightlen = bbox[3] - bbox[1]

    # Новые длины сторон
    if heightlen > widthlen:
        widthlen = int(BASE_SIZE * widthlen / heightlen)
        heightlen = BASE_SIZE
    else:
        heightlen = int(BASE_SIZE * widthlen / heightlen)
        widthlen = BASE_SIZE

    # 3. Преобразуем значащую часть в картинку 30 * 30
    # Стартовая точка рисования
    hstart = int((MAX_SIZE - heightlen) / 2)
    wstart = int((MAX_SIZE - widthlen) / 2)
    # Отмасштабированная картинка
    image_temp = image_bin.crop(bbox).resize((widthlen, heightlen), Image.NEAREST)

    # 4. Размещаем значащую часть в центре картинки 40 * 40
    # Перенос на белый фон с центрированием
    new_img = Image.new('L', (MAX_SIZE, MAX_SIZE), 255)
    new_img.paste(image_temp, (wstart, hstart))

    return new_img

def process_image(file_path):
    # 1. Считываем файл
    image_bin = Image.open(file_path)
    new_img = transform_image(image_bin)

    imgdata = list(new_img.getdata())
    img_array = np.array([(255.0 - x) / 255.0 for x in imgdata])
    return img_array

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=True,
    help="File for parsing")
args = vars(ap.parse_args())

model_path = os.path.dirname(os.path.realpath(__file__)) + '/clever_model.bin'
labels_path = os.path.dirname(os.path.realpath(__file__)) + '/labels.bin'
model = load_model(model_path)
lb = pickle.loads(open(labels_path, "rb").read())

image = process_image(args['file'])
images = []
images.append(image)
images = np.array(images)

preds = model.predict(images)
i = preds.argmax(axis=1)[0]
label = lb.classes_[i]
print('Найдено число: {}'.format(label))