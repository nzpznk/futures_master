# 用于绘制同一种合约的不同参数

from matplotlib import pyplot as plt
from read_data import read_data
import config

to_sec = lambda delta_t:delta_t.seconds+delta_t.microseconds/1e6

def show_data(contract, prop_list, data):
    if contract not in data:
        print('--- contract', contract, 'not in data ---')
        return
    xs = [to_sec(d['datetime']-data[contract][0]['datetime']) for d in data[contract]]
    for prop in prop_list:
        ys = [d[prop] for d in data[contract]]
        plt.plot(xs, ys)
    plt.show()

if __name__ == '__main__':
    dat = read_data([0])
    show_data('A1', ['price'], dat)
