from read_data import read_data
from config import dat_len, predict_len, data_file_list, data_format, theta, usefulkey
import datetime
import copy
import math

to_sec = lambda dt:(dt.seconds + dt.microseconds/1e6)

def __convert__(datlist):
    if not datlist:
        return [], []
    data, label = [], []
    n = len(datlist)
    d1 = math.floor(dat_len / 0.5)
    dim = d1 * 7
    d2 = math.floor(predict_len / 0.5)
    li = [0 for i in range(20)]
    for i in range(n):
        li[0] = datlist[i]
        j = 1
        for cnt in range(1, d1):
            if not i + j < n:
                break
            dt = datlist[i + j]['datetime'] - li[cnt-1]['datetime']
            if to_sec(dt) < 0.7:
                li[cnt] = datlist[i+j]
                j += 1
            else:
                li[cnt] = li[cnt-1].copy()
                li[cnt]['datetime'] = li[cnt - 1]['datetime'] + datetime.timedelta(0, 0, 500000)
                li[cnt]['bidv'] = li[cnt]['askv'] = 0
        if not i + j < n:
            continue
        data.append([li[k][x] for x in usefulkey for k in range(d1)])
        stime = li[-1]['datetime']
        price = li[-1]['price']
        meanprice = 0
        cnt = 0
        if to_sec(datlist[i+j]['datetime'] - stime) >= predict_len:
            ratio = 1
        else:
            while i + j < n and to_sec(datlist[i+j]['datetime'] - stime) < predict_len:
                meanprice += datlist[i+j]['price']
                cnt += 1
                j += 1
            meanprice /= cnt
            ratio = meanprice / price
        if ratio < 1 - theta:
            label.append(0)
        elif 1 - theta <= ratio <= 1 + theta:
            label.append(1)
        else:
            label.append(2)
    return data, label

def get_labeled_data(indexlist):
    data = read_data(indexlist)
    label = copy.deepcopy(data_format)
    for key, val in data.items():
        data[key], label[key] = __convert__(val)
    return data, label

if __name__ == '__main__':
    data, label = get_labeled_data([0])
    numup = len([x for x in label['A1'] if x == 2])
    numdown = len([x for x in label['A1'] if x == 0])
    numstable = len([x for x in label['A1'] if x == 1])
    print(numup, numdown, numstable)
