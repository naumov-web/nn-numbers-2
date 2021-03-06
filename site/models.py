from codecs import open
import uuid
import os

class Image(object):
  def __init__(self):
    self.nothing = 0

  def save_temp(self, image):
    directory = os.path.dirname(os.path.realpath(__file__)) + '/../temp/'

    try:
      os.stat(directory)
    except:
      os.mkdir(directory)

    filename = str(uuid.uuid1()) + '.jpg'

    path = directory + filename
    with open(path, 'wb+') as f:
      f.write(image)

    return path

  def save(self, drawn_digit, image):
    directory = os.path.dirname(os.path.realpath(__file__)) + '/../datasets/' + str(drawn_digit)

    try:
      os.stat(directory)
    except:
      os.mkdir(directory)

    path = directory + '/' + str(uuid.uuid1()) + '.jpg'
    with open(path, 'wb+') as f:
      f.write(image)