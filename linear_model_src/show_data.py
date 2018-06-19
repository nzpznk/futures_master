# 用于绘制同一种合约的不同参数

from matplotlib import pyplot as plt
from read_data import read_data
from label_data import get_labeled_data
import config
import numpy as np

to_sec = lambda delta_t:delta_t.seconds+delta_t.microseconds/1e6

def show_data(contract, prop_list, data, label):
    xs = []
    for i in range(len(data)):
        xs.append(i)
    ys = data
    fall = []
    rise = []
    if (label[0] == 2):
        fall.append(0)
        rise.append(1)
    elif (label[0] == 0):
        fall.append(1)
        rise.append(0)
    else:
        fall.append(1)
        rise.append(1)
    for i in range(1, len(ys) - 1):
        if (label[i] == 2 or label[i + 1] == 2):
            fall.append(0)
        else:
            fall.append(1)
        if (label[i] == 0 or label[i + 1] == 0):
            rise.append(0)
        else:
            rise.append(1)
    if (label[len(ys) - 1] == 0):
        fall.append(1)
        rise.append(0)
    elif (label[len(ys) - 1] == 2):
        fall.append(0)
        rise.append(1)
    else:
        fall.append(1)
        rise.append(1)
    # print(rise)
    rise_masked = np.ma.array(ys, mask=rise)
    fall_masked = np.ma.array(ys, mask=fall)
    # print(rise_masked)
    plt.plot(xs, ys, 'k', linewidth=1)
    plt.plot(xs, fall_masked, 'r', linewidth=1)
    plt.plot(xs, rise_masked, 'g', linewidth=1)
    plt.savefig('./pictures/trends.png', dpi=120)
    plt.show()


if __name__ == '__main__':
    (data, label) = get_labeled_data([0])
    means = []
    for i in range(len(data['A1'])):
        means.append(data['A1'][i][8])
    print(label['A1'].count(0))
    print(label['A1'].count(1))
    print(label['A1'].count(2))
    #print(means)
    #print(label['A1'])
    show_data('A1', ['price'], means, label['A1'])
