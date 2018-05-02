# 用于绘制同一种合约的不同参数

from matplotlib import pyplot as plt
from read_data import read_data
import config
import numpy as np

to_sec = lambda delta_t:delta_t.seconds+delta_t.microseconds/1e6

def show_data(contract, prop_list, data):
    if contract not in data:
        print('--- contract', contract, 'not in data ---')
        return
    xs = np.array([to_sec(d['datetime']-data[contract][0]['datetime']) for d in data[contract]])
    for prop in prop_list:
        ys = [d[prop] for d in data[contract]]
        fall = [0 if y_ > 4840000 else 1 for y_ in ys]
        rise = [0 if y_ < 4780000 else 1 for y_ in ys]
        fall_masked = np.ma.array(ys, mask = fall)
        rise_masked = np.ma.array(ys, mask = rise)
        plt.plot(xs, ys, 'k', linewidth=0.4)
        plt.plot(xs, fall_masked, 'g', linewidth=0.5)
        plt.plot(xs, rise_masked, 'r', linewidth=0.6)
        plt.show()

if __name__ == '__main__':
    dat = read_data([0])
    show_data('A1', ['price'], dat)
