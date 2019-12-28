__author__ = 'Naumov-Web'

import os
import random
from PIL import Image
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD
import pickle

BASE_SIZE = 80
MAX_SIZE = 100
INIT_LR = 0.01
EPOCHS = 100
ANGLES = [-20, -15, -10, -5, 5, 10, 15, 20]
SCALES_X = [0.8, 0.9, 1.1, 1.2]
SCALES_Y = [0.8, 0.9, 1.1, 1.2]

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

def augment(file_path):
    image_bin = Image.open(file_path)
    image = transform_image(image_bin)

    # 5. Размножим картинку
    # - поворот на 10 градусов влево
    # - поворот на 20 градусов влево
    # - поворот на 10 градусов вправо
    # - поворот на 20 градусов вправо
    # - увеличение масштаба на 10% по высоте
    # - уменьшение масштаба на 10% по высоте
    # - увеличение масштаба на 10% по ширине
    # - уменьшение масштаба на 10% по ширине

    images = []
    for angle in ANGLES:
        new_image = image.rotate(angle, fillcolor='white')
        new_image = transform_image(new_image)
        imgdata = list(new_image.getdata())
        img_array = np.array([(255.0 - x) / 255.0 for x in imgdata])
        images.append(img_array)

    for scale_x in SCALES_X:
        width, height = image.size
        new_image = image.resize((int(width * scale_x), height))
        new_image = transform_image(new_image)
        imgdata = list(new_image.getdata())
        img_array = np.array([(255.0 - x) / 255.0 for x in imgdata])
        images.append(img_array)

    for scale_y in SCALES_Y:
        width, height = image.size
        new_image = image.resize((width, int(scale_y * height)))
        new_image = transform_image(new_image)
        imgdata = list(new_image.getdata())
        img_array = np.array([(255.0 - x) / 255.0 for x in imgdata])
        images.append(img_array)

    return images

print("[INFO] Загрузка изображений...")
data = []
labels = []
all_files = []

datasets_directory = os.path.dirname(os.path.realpath(__file__)) + '/../datasets'
directories = os.listdir(datasets_directory)

for directory in directories:
    current_dir = datasets_directory + '/' + directory
    files = os.listdir(current_dir)

    for file in files:
        all_files.append(current_dir + '/' + file)

random.seed(1000)
random.shuffle(all_files)

for file_path in all_files:
    # 40 * 40 * 3 = 4800
    image = process_image(file_path)
    label = file_path.split('/')[-2]

    data.append(image)
    labels.append(label)

    custom_images = augment(file_path)
    for custom_image in custom_images:
        data.append(custom_image)
        labels.append(label)

data = np.array(data, dtype="float") / 255.0
labels = np.array(labels)
print(data.shape)
lb = preprocessing.LabelBinarizer()
(trainX, testX, trainY, testY) = train_test_split(data,
    labels, test_size=0.2, random_state=50)
trainY = lb.fit_transform(trainY)
testY = lb.transform(testY)

print("[INFO] Обучение нейронной сети...")
nn_model = Sequential()
nn_model.add(Dense(MAX_SIZE * MAX_SIZE, input_shape=(MAX_SIZE * MAX_SIZE,), kernel_initializer="normal", activation="relu"))
nn_model.add(Dense(10, kernel_initializer="normal", activation="softmax"))
nn_model.compile(loss="categorical_crossentropy", optimizer="SGD", metrics=["accuracy"])
nn_model.fit(trainX, trainY, validation_data=(testX, testY),
     epochs=EPOCHS, batch_size=32)

print("[INFO] Сохранение нейронной сети...")
nn_model.save(os.path.dirname(os.path.realpath(__file__)) + '/clever_model.bin')

f = open(os.path.dirname(os.path.realpath(__file__)) + '/labels.bin', "wb")
f.write(pickle.dumps(lb))
f.close()