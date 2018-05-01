import os

__data_dir__ = '../futuresData/'

__database_dir__ = '../myDatabase/'

__models_dir__ = '../myModels/'

data_file_list = [__data_dir__ + x for x in os.listdir(__data_dir__)]

data_file_list = sorted(data_file_list)

contract_list = ['A1', 'A3', 'B2', 'B3']

data_format = {'A1':[], 'A3':[], 'B2':[], 'B3':[]}

dat_len = 10
predict_len = 10