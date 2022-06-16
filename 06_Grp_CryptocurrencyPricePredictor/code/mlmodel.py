import json
import requests
from keras.models import Sequential
from keras.layers import Activation, Dense, Dropout, LSTM
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.metrics import mean_absolute_error
from keras.preprocessing.sequence import TimeseriesGenerator
# %matplotlib inline
from GetDataAPI.models import CryptoPrice
from datetime import datetime

#BTC , ETH , 
#return df , performace score
class CryptoModel:
    def __init__(self,coin_passed):
        self.coin = coin_passed 
        self.flagg = 0
        print(self.coin)
        if self.coin == 'ETH':
            self.flagg = 2
        else:
            self.flagg = 1

    def runmodel(self):
        endpoint = 'https://min-api.cryptocompare.com/data/histoday'
        res = requests.get(endpoint + '?fsym=' +  self.coin + '&tsym=CAD&limit=800')
        hist = pd.DataFrame(json.loads(res.content)['Data'])
        hist = hist.set_index('time')
        hist.index = pd.to_datetime(hist.index, unit='s')
        hist['time'] = pd.to_datetime(hist.index, unit='s')
        target_col = 'close'

        hist.drop(["conversionType", "conversionSymbol","high","low","open","volumefrom","volumeto"], axis = 'columns', inplace = True)

        close_data = hist['close'].values
        close_data = close_data.reshape((-1,1))

        split_percent = 0.70
        split = int(split_percent*len(close_data))

        close_train = close_data[:split]
        close_test = close_data[split:]

        date_train = hist['time'][:split]
        date_test = hist['time'][split:]

        look_back = 15

        train_generator = TimeseriesGenerator(close_train, close_train, length=look_back, batch_size=20)     
        test_generator = TimeseriesGenerator(close_test, close_test, length=look_back, batch_size=1)

        model = Sequential()
        model.add(LSTM(100,activation='relu',input_shape=(look_back,1)))
        model.add(Dense(1))
        model.add(Dropout(.02))
        model.compile(optimizer='adam', loss='mse')

        num_epochs = 15
        model.fit(train_generator, epochs=num_epochs, verbose=1)

        prediction = model.predict(test_generator)

        close_train = close_train.reshape((-1))
        close_test = close_test.reshape((-1))
        prediction = prediction.reshape((-1))
        ct = close_test[:226]
        # from sklearn.metrics import mean_absolute_percentage_error
        # mean_absolute_percentage_error(ct, prediction)

        close_data = close_data.reshape((-1))

        num_prediction = 30

        prediction_list = close_data[-look_back:]
        for _ in range(num_prediction):
            x = prediction_list[-look_back:]
            x = x.reshape((1, look_back, 1))
            out = model.predict(x)[0][0]
            prediction_list = np.append(prediction_list, out)
        prediction_list = prediction_list[look_back-1:]
        forecast = prediction_list


        last_date = hist['time'].values[-1]
        prediction_dates = pd.date_range(last_date, periods=num_prediction+1).tolist()
        forecast_dates = prediction_dates

        print(forecast)

        forecast_dates

        df = pd.DataFrame({'time' : forecast_dates,'close':forecast})
        print(df)
        arr = df.to_numpy()
        for i in arr:
            k = str(i[0])
            k = k[:10]
            # print(k,i[1])
            cyptoObject = CryptoPrice.objects.create(date=datetime.strptime(k, '%Y-%m-%d'),value=i[1],flag=self.flagg)
            cyptoObject.save()
        # return df
