from read_data import read_data
from config import dat_len, predict_len, data_file_list, data_format, theta, usefulkey
import datetime
import copy
import math
import pickle
import os
from config import __database_dir__

to_sec = lambda dt:(dt.seconds + dt.microseconds/1e6)

def __convert__(datlist):
    if not datlist:
        return [], []
    data, label = [], []
    n = len(datlist)
    d1 = math.floor(dat_len / 0.5)
    dim = d1 * 7
    d2 = math.floor(predict_len / 0.5)
    for i in range(n):
        datli = [0 for x in range(20)]
        datlab = []
        datli[0] = datlist[i]
        j = 1
        for cnt in range(1, d1):
            if not i + j < n:
                break
            dt = datlist[i + j]['datetime'] - datli[cnt-1]['datetime']
            if to_sec(dt) < 0.7:
                datli[cnt] = datlist[i+j]
                j += 1
            else:
                datli[cnt] = datli[cnt-1].copy()
                datli[cnt]['datetime'] = datli[cnt - 1]['datetime'] + datetime.timedelta(0, 0, 500000)
                datli[cnt]['bidv'] = datli[cnt]['askv'] = 0
        if not i + j < n:
            continue
        data.append(datli)
        stime = datli[-1]['datetime']
        if to_sec(datlist[i+j]['datetime'] - stime) < predict_len:
            while i + j < n and to_sec(datlist[i+j]['datetime'] - stime) < predict_len:
                datlab.append(datlist[i+j])
                j += 1
        label.append(datlab)
    return data, label

# extract_feature_1
# 得到特征向量维度为9，前五维为每隔2s的价格加权平均，之后是最高价格，最低价格，总成交量，成交均价
def extract_feature_1(data, label):
    def cal_feature(dat):
        vol = [min(dat[i]['bidv'], dat[i]['askv']) for i in range(20)]
        pri = [dat[i]['price'] for i in range(20)]
        tot = [vol[i] * pri[i] for i in range(20)]
        svol = sum(vol)
        mean = sum(tot) / (svol + 0.1)
        return [*(sum(tot[4*i:4*(i+1)]) / (sum(vol[4*i:4*(i+1)])+0.1) - mean for i in range(5)), max(pri) - mean, min(pri) - mean, svol, mean]
    feature_vec = [cal_feature(x) for x in data]
    #feature_vec_new = [x[:-1] for x in feature_vec]
    label_vec = []
    for i in range(len(label)):
        if not label[i]:
            label_vec.append(1)
            continue
        vol = [min(d['bidv'], d['askv']) for d in label[i]]
        pri = [d['price'] for d in label[i]]
        tot = [vol[i] * pri[i] for i in range(len(vol))]
        nextp = sum(tot) / (sum(vol) + 0.1)
        if feature_vec[i][-1] != 0:
            ratio = nextp / feature_vec[i][-1]
        else:
            ratio = 1
        if ratio < 1-theta:
            label_vec.append(0)
        elif 1-theta <= ratio <= 1+theta:
            label_vec.append(1)
        else:
            label_vec.append(2)
    return feature_vec, label_vec

def get_labeled_data(indexlist, extract_fun = extract_feature_1):
    data = copy.deepcopy(data_format)
    data_tot = copy.deepcopy(data_format)
    label = copy.deepcopy(data_format)
    label_tot = copy.deepcopy(data_format)
    for i in indexlist:
        with open(__database_dir__ + str(i) + 'extracted', 'rb') as dbf:
            (data, label) = pickle.load(dbf)
            for key in data:
                data_tot[key].extend([x[:] for x in data[key]])
                label_tot[key].extend(label[key])
    return data_tot, label_tot

def get_labeled_data_old(indexlist, extract_fun = extract_feature_1):
    data = read_data(indexlist)
    label = copy.deepcopy(data_format)
    for key, val in data.items():
        data[key], label[key] = extract_fun(*__convert__(val))
    return data, label

def extract_to_database(indexlist, extract_fun = extract_feature_1):
    for i in indexlist:
        if os.path.exists(__database_dir__ + str(i) + 'extracted') == False:
            tmp = get_labeled_data_old([i])
            with open(__database_dir__ + str(i) + 'extracted', 'wb') as dbf:
                pickle.dump(tmp, dbf)

if __name__ == '__main__':
    extract_to_database(range(1))
