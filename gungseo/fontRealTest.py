import sys
from os import listdir
from os.path import isfile, join
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.callbacks import ModelCheckpoint,EarlyStopping
from keras.models import load_model
# import matplotlib.pyplot as plt
import numpy
import os
import tensorflow as tf
import cv2
from keras import backend as K
from .img_preprocessing import getTextImages


#데이터 로드
class getFontInfo:
  # def __init__(self, uploaded_file_url):
  #   self.img_url = uploaded_file_url[1:]
  def __init__(self, img):
    self.img = img


  def preprocessing(self, new_path):
    if not os.path.exists(new_path):
      os.makedirs(new_path)
      print(new_path)
    # fontFile=[k for k in listdir(path) if isfile(join(path, k)) and not k[0]=='.']
    getImages = getTextImages(new_path)
    # for file in fontFile:
    # img = cv2.imread(self.img_url)
    # print(self.img_url)
    getImages.get_texts(self.img)
    print('전처리 끝')

  def decision(self):
    newpath = 'newmedia/new/'
    self.preprocessing(newpath)

    test_datagen = ImageDataGenerator(rescale=1./255)
    test_generator = test_datagen.flow_from_directory('newmedia',
                                                      target_size=(28,28),
                                                      color_mode='grayscale',
                                                      batch_size = 1,
                                                      class_mode = 'categorical')
    #모델 로드
    model = load_model('gungseo/fontModel.h5')
    #테스트 셋 예측
    predictions = model.predict_generator(test_generator, steps=1)
    #클래스 이름 get
    class_dictionary = test_generator.class_indices
    #클리어
    K.clear_session()
    #예측값 저장
    y_pred = numpy.rint(predictions)

    return y_pred, class_dictionary
    
    # print("예측값: %s" %(y_pred))
    # 테스트 정확도 출력
    # scores = model.evaluate_generator(test_generator, steps=)
    # print("%s: %.2f%%" %(model.metrics_names[1], scores[1]*100))