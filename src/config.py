import os

__data_dir__ = '../futuresData/'

data_file_list = [__data_dir__ + x for x in os.listdir(__data_dir__)]

contract_list = ['A1', 'A3', 'B2', 'B3']

data_format = {'A1':[], 'A3':[], 'B2':[], 'B3':[]}

dat_len = 20
predict_len = 10
