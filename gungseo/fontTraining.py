#import matplotlib.pyplot as plt
import sys
import numpy
import os
from os import listdir
from os.path import isfile, join
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras.callbacks import ModelCheckpoint,EarlyStopping
from keras.models import load_model
import cv2
# import matplotlib.pyplot as plt
from img_preprocessing import getTextImages
from keras import optimizers
from keras import regularizers

def preprocessing(path, new_path):
  if not os.path.exists(new_path):
    os.makedirs(new_path)

  fontDir = [f for f in listdir(path) if not f[0] == '.' ]
  fontFile = {}

  for d in fontDir :
    fontFile[d]=[k for k in listdir(path+d) if isfile(join(path+d, k)) and not k[0]=='.']

  for dir_name in fontDir:
    orgpath = path+dir_name+'/'
    trimpath = new_path+dir_name+'/'
    if not os.path.exists(trimpath):
      os.makedirs(trimpath)

    getImages = getTextImages(trimpath)
    for file in fontFile[dir_name]:
      print(file)
      img = cv2.imread(orgpath+file)
      getImages.get_texts(img)
      print(getImages.count,"!!!!!!!!")



trainPath = './allfontData/train/trainAll/'
new_trainPath = './allfontData/train/newtrain/'
testPath = './allfontData/test/testAll/'
new_testPath = './allfontData/test/newtest/'


# preprocessing(trainPath, new_trainPath)
# preprocessing(testPath, new_testPath)



#seed 값 설정
# seed = 0
# numpy.random.seed(seed)
# tf.set_random_seed(seed)


# 데이터 로드 및 전처리
# the augmentation is not done within an epoch, but throughout the entire training process. 
train_datagen = ImageDataGenerator(rescale=1./255)
# Data Augmentation
# , rotation_range=90
# 	, width_shift_range=0.1, 
# 	height_shift_range=0.1, shear_range=0.5, zoom_range=0.3,
# 	 horizontal_flip=True, vertical_flip=True, fill_mode='nearest'

train_generator = train_datagen.flow_from_directory('./allfontData/train/newtrain/',
                                                    target_size=(28,28),
                                                    color_mode='grayscale',
                                                    batch_size=500,
                                                    class_mode='categorical')

test_datagen = ImageDataGenerator(rescale=1./255)
test_generator = test_datagen.flow_from_directory('./allfontData/test/newtest/',
                                                  target_size=(28,28),
                                                  color_mode='grayscale',
                                                  batch_size = 500,
                                                  class_mode = 'categorical')
#클래스명 
class_dictionary = test_generator.class_indices;
print(class_dictionary)
#y labeling 구체화 , 그래프
#y_true = test_generator.classes

# 모델 구성하기
model = Sequential()
#32개의 필터 , 필터 사이즈 3,3 , input 이미지 (28*28 흑백)
model.add(Conv2D(32, (3, 3), padding='same', input_shape=(28, 28, 1),
	kernel_initializer = 'he_normal',
	bias_initializer = 'he_normal',
	activation = 'relu',
	kernel_regularizer = regularizers.l2(0.01)))
#64개의 필터 , 필터 사이즈 3,3
model.add(Conv2D(64, (3, 3), activation='relu'))
#맥스풀링 사이즈 2,2
model.add(MaxPooling2D(pool_size=2))
#30%의 은닉층 노드 무시
model.add(Dropout(0.3))
#64개의 필터 , 필터 사이즈 3,3
model.add(Conv2D(128, (3, 3), activation='relu'))
#맥스풀링 사이즈 2,2
model.add(MaxPooling2D(pool_size=2))
#30%의 은닉층 노드 무시
model.add(Dropout(0.3))
#1차원벡터의 형태로 형태변환
model.add(Flatten())
model.add(Dense(128,  activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(8, activation='softmax'))

# adamAct = optimizers.adam(lr=0.00001)

#모델 컴파일(학습과정 설명하기)
model.compile(loss='categorical_crossentropy',
              optimizer="adam",
              metrics=['accuracy'])

# checkpointer = ModelCheckpoint(filepath=modelpath, monitor='val_loss', verbose=1, save_best_only=True)

early_stopping_callback = EarlyStopping(monitor='loss', patience=10)



# 모델의 실행(학습시작)
history= model.fit_generator(train_generator,
                    steps_per_epoch =90,#[트레이닝데이터수/배치사이즈]
                    #augmented data set = specifying 2x value of the original steps_per_epoch
                    epochs =200,
                    validation_data = test_generator,
                    validation_steps = 30,
                    callbacks=[early_stopping_callback])

y_acc = history.history['val_acc']

scores = model.evaluate_generator(test_generator, steps=30)
print("\n%s: %.2f%%" %(model.metrics_names[1], scores[1]*100))

# 클래스 이름
# print(test_generator.classes)
print(model.summary())

# x_len = numpy.arange(len(y_acc))
# plt.plot(x_len, y_acc, "o", c="red", markersize=3)
# plt.show()

#checkpointer 콜백추가
model.save('./fontModel.h5')


