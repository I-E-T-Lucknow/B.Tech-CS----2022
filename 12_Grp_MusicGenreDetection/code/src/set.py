import pandas as pd
import numpy as np
np.random.seed(123)
import pickle

from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle

from config import SET_DATAPATH


class Set():

    def __init__(self, data):
        self.train_set  = None
        self.valid_set  = None
        self.test_set   = None
        self.data       = data
        self.le         = LabelEncoder().fit(self.data.GENRES)

        print("\n-> Set() object is initialized.")

    def make_dataset(self):
        df  = self.data.raw_data.copy()
        df  = shuffle(df)

        train_records, valid_records, test_records = list(), list(), list()
        for i, genre in enumerate(self.data.GENRES):
            genre_df    = df[df['genre'] == genre]
            train_records.append(genre_df.iloc[:700].values)
            valid_records.append(genre_df.iloc[700:900].values)
            test_records.append(genre_df.iloc[900:].values)

        train_records   = shuffle([record for genre_records in train_records    for record in genre_records])
        valid_records   = shuffle([record for genre_records in valid_records    for record in genre_records])
        test_records    = shuffle([record for genre_records in test_records     for record in genre_records])

        self.train_set  = pd.DataFrame.from_records(train_records,  columns=['spectrogram', 'genre'])
        self.valid_set  = pd.DataFrame.from_records(valid_records,  columns=['spectrogram', 'genre'])
        self.test_set   = pd.DataFrame.from_records(test_records,   columns=['spectrogram', 'genre'])
        return

    def get_train_set(self):
        x_train = np.stack(self.train_set['spectrogram'].values)
        x_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1], x_train.shape[2]))
        y_train = np.stack(self.train_set['genre'].values)
        y_train = self.le.transform(y_train)
        print("x_train shape: ", x_train.shape)
        print("y_train shape: ", y_train.shape)
        return x_train, y_train

    def get_valid_set(self):
        x_valid = np.stack(self.valid_set['spectrogram'].values)
        x_valid = np.reshape(x_valid, (x_valid.shape[0], 1, x_valid.shape[1], x_valid.shape[2]))
        y_valid = np.stack(self.valid_set['genre'].values)
        y_valid = self.le.transform(y_valid)
        print("x_valid shape: ", x_valid.shape)
        print("y_valid shape: ", y_valid.shape)
        return x_valid, y_valid

    def get_test_set(self):
        x_test  = np.stack(self.test_set['spectrogram'].values)
        x_test  = np.reshape(x_test, (x_test.shape[0], 1, x_test.shape[1], x_test.shape[2]))
        y_test  = np.stack(self.test_set['genre'].values)
        y_test  = self.le.transform(y_test)
        print("x_test shape : ", x_test.shape)
        print("y_test shape : ", y_test.shape)
        return x_test, y_test

    def save(self):
        with open(SET_DATAPATH, 'wb') as outfile:
            pickle.dump((self.train_set, self.valid_set, self.test_set), outfile, pickle.HIGHEST_PROTOCOL)
        print("-> Set() object is saved.\n")
        return

    def load(self):
        with open(SET_DATAPATH, 'rb') as infile:
            (self.train_set, self.valid_set, self.test_set) = pickle.load(infile)
        print("-> Set() object is loaded.\n")
        return