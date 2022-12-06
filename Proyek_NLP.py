# -*- coding: utf-8 -*-
"""Proyek_NLP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PIj_CFka4xHSPxovD2SVujw3OqYJ79Tk

Nama: Nuril Hidayati

Nomor Registrasi: 1494037162100-621

Pelatihan FGA DTS - Alur Machine Learning Developer

Sidoarjo, Jawa Timur

Dataset : https://www.kaggle.com/septa97/100k-courseras-course-reviews-dataset?select=reviews.csv
"""

import pandas as pd
df = pd.read_csv('reviews.csv')
df.head()

"""**Hapus kolom yang tidak diperlukan**"""

data = df.drop(columns=['Id'])
data

data.info()

"""**Data** **Cleaning**"""

data.isna().sum()

print(data.duplicated().sum())

data_baru = data.copy(deep=True)
data_baru.drop_duplicates(inplace=True)

print(data_baru.duplicated().sum())

data_baru.shape

"""**Proses** **One-Hot-Encoding**"""

category = pd.get_dummies(data_baru['Label'])
data_baru = pd.concat([data_baru, category], axis=1)
dataset = data_baru.drop(columns='Label')
dataset

"""**Mengubah nilai-nilai dari dataframe ke dalam tipe data numpy array**"""

x = dataset['Review'].values
y = dataset[[1, 2, 3, 4, 5]].values

"""**Membagi data untuk training dan data untuk testing**"""

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
len(x_test)

"""**Tokenization**"""

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

num_word = 100473
embedded_dim = 100

tokenizer = Tokenizer(num_words=num_word, oov_token='x', filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~0-9', lower=True)
tokenizer.fit_on_texts(x_train)
word_index=tokenizer.word_index
print("ditemukan %s token unik"% len(word_index))
 
sekuens_train = tokenizer.texts_to_sequences(x_train)
sekuens_test = tokenizer.texts_to_sequences(x_test)
 
padded_train = pad_sequences(sekuens_train, maxlen=250, padding='post') 
padded_test = pad_sequences(sekuens_test, maxlen=250, padding='post')
print("Shape of data tensor ", padded_train.shape)
print("Shape of data tensor ", y_train.shape)
print("Shape of data tensor ", padded_test.shape)
print("Shape of data tensor ", y_test.shape)

"""**Modelling menggunakan Embedding**"""

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Input, GlobalMaxPooling1D, Conv1D, MaxPool1D, Embedding, Dropout, LSTM

max_len = 250
vector_length = 100

model = Sequential()
model.add(Embedding(input_dim=num_word, output_dim=vector_length, input_length=max_len))
model.add(LSTM(100))
model.add(Dense(32, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(16, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(5, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

"""**Membuat Class Callback**"""

from tensorflow.keras.callbacks import Callback
class myCallback(Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy')>0.90 and logs.get('val_accuracy')>0.90):
      print("\nAkurasi telah mencapai >90%! dan val akurasi telah mencapai >90%!")
      self.model.stop_training = True
callbacks = myCallback()

"""**Melatih Model**"""

history = model.fit(padded_train, 
                    y_train, 
                    epochs=15,
                    batch_size=32,
                    callbacks=[callbacks],
                    validation_data=(padded_test, y_test),
                    verbose=2)

model.evaluate(padded_test, y_test)

import matplotlib.pyplot as plt
plt.plot(history.history['loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train'], loc='upper right')
plt.show()

plt.plot(history.history['accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train'], loc='lower right')
plt.show()