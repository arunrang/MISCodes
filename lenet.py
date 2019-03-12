# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers.normalization import BatchNormalization
from keras.layers.core import Dropout
class mymodel:
    @staticmethod
    def build(height,width,depth,classes):
        classifier=Sequential([
                Conv2D(32,(3,3),input_shape=(height,width,depth),activation='relu',
                       padding='same'),
                       BatchNormalization(axis=-1),
                       MaxPooling2D(pool_size=(3, 3)),
                       Dropout(0.25),
                       Conv2D(64, (3, 3), activation='relu', padding='same',),
                       BatchNormalization(axis=-1),
                       Conv2D(64, (3, 3), activation='relu', padding='same',),
                       MaxPooling2D(pool_size=(2, 2)),
                       Dropout(0.25),
                       Conv2D(128, (3, 3), activation='relu', padding='same',),
                       BatchNormalization(axis=-1),
                       Conv2D(128, (3, 3), activation='relu', padding='same',),
                       BatchNormalization(axis=-1),
                       MaxPooling2D(pool_size=(2, 2)),
                       Dropout(0.25),
                       Flatten(),
                       Dense(1024, activation='relu'),
                       BatchNormalization(axis=-1),
                       Dropout(0.25),
                       Dense(1024, activation='relu'),
                       BatchNormalization(axis=-1),
                       Dropout(0.25),
                       Dense(classes, activation='softmax')])
        
        return classifier