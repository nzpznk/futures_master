from read_data import read_data
from config import dat_len, predict_len, data_file_list, data_format, theta, usefulkey
import datetime
import copy
import math
import pickle
import os
from matplotlib import pyplot as plt
from config import __database_dir__
k = 0.3
year = 2017
time_period = datetime.timedelta(microseconds = 500000)

to_sec = lambda dt: (dt.seconds + dt.microseconds / 1e6)

def count_price(raw_data, time, contract_extracted = 0):
    has_contract = False
    turnover = 0; pre_turnover = 0
    volume = 0; pre_volume = 0
    bid_price = 0; ask_price = 0
    for contract in range(contract_extracted, len(raw_data) - 1):
        if raw_data[contract]['datetime'] + time_period > time and raw_data[contract]['datetime'] <= time:
            contract_extracted = contract
            turnover = raw_data[contract]['turnover']
            volume = raw_data[contract]['volume']
            bid_price = raw_data[contract]['bidp']
            ask_price = raw_data[contract]['askp']
            has_contract = True
        elif raw_data[contract]['datetime'] > time:
            break
        else:
            pre_turnover = raw_data[contract]['turnover']
            pre_volume = raw_data[contract]['volume']
    if has_contract is True:
        if volume == pre_volume:
            return -1, contract_extracted
        return k * (turnover - pre_turnover) / (volume - pre_volume) + (1 - k) * (bid_price + ask_price) / 2, contract_extracted
    else:
        return -1, contract_extracted

def process_data(data_list):
    #save data in (time, price) form
    for index in data_list:
        raw_tot_data = read_data([index])
        for species in raw_tot_data:
            raw_data = raw_tot_data[species]
            if (len(raw_data) != 0):
                contract_extracted = 0
                start_time = raw_data[0]['datetime']
                end_time = raw_data[len(raw_data) - 1]['datetime']
                tmp_time = copy.deepcopy(start_time)
                time_price_list = []
                #show_list = []
                i = 0
                while tmp_time < end_time:
                    i += 1
                    price, contract_extracted = count_price(raw_data, tmp_time, contract_extracted)
                    if price is -1:
                        if i is 1:
                            i = 0
                            tmp_time += time_period
                            continue
                        else:
                            price = time_price_list[-1][1]
                    time_price_list.append([tmp_time, price])
                    #show_list.append(price)
                    tmp_time += time_period
                with open(__database_dir__ + str(index) + str(species), 'wb') as pk:
                    pickle.dump(time_price_list, pk)
                #print(time_price_list)
                #plt.plot(show_list)
                #plt.show()

if __name__ == '__main__':
    process_data(range(108))