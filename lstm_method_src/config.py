import os
import re
from datetime import datetime

__data_dir__ = '../futuresData/'

__database_dir__ = '../myDatabase/'

__labeled_data_dir__ = '../labeled_data/'

__models_dir__ = '../myModels/'

data_file_list = [__data_dir__ + x for x in os.listdir(__data_dir__)]

data_file_list = sorted(data_file_list)

contract_list = ['A1', 'A3', 'B2', 'B3']

data_format = {'A1':[], 'A3':[], 'B2':[], 'B3':[]}

usefulkey = ['highp', 'lowp', 'price', 'askp', 'bidp', 'askv', 'bidv', 'turnover', 'volume']

test_list = [i for i in range(32, 54)]

train_list = [i for i in range(32)]

dates = sorted([x for x in os.listdir(__data_dir__)])
datepat = re.compile(r'[0, 1]-(?P<year>[0-9]{4})(?P<month>[0-9]{2})(?P<day>[0-9]{2}).*')
dates = [re.match(datepat, x).groupdict() for x in dates]
dates = [datetime(year = int(d['year']), month = int(d['month']), day = int(d['day'])) for d in dates]

# use 5 miniutes to predict [t+5s, t+20s]
seg_time = 10
train_time = 300
predict_st = 5
predict_ed = 40

theta = 0.0015

