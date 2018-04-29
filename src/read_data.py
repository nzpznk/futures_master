# 调用read_data返回四类合约的数据
# 返回数据格式 {
#   'A1': list of data dict
#   'A2': list of data dict
#   'B2': list of data dict
#   'B3': list of data dict
# }

# 每个合约的数据是一个dict的列表，每个dict是一次交易
# 格式：
# {
#     'highp': highest price
#     'lowp': lowest price
#     'price': latest price
#     'askp': ask price
#     'bidp': bid price
#     'askv': ask volumn
#     'bidv': bid volumn
#     'time': 一个python datetime对象
# }

# 使用时传入一个文件index列表，返回指定范围内文件的数据

import config
import os
import re
import datetime
import time
# 2017-07-03 08:49:49.787  [KeyedThreadPool-60-1] INFO   - Quote[lastPrice=4640000,highestPrice=4675000,lowestPrice=4590000,volume=65738,turnover=304461420000,bidPrice1=4635000,bidVolume1=17,askPrice1=4640000,askVolume1=36,instrumentID=A3,exchangeID=] 

datapat = re.compile(r'.*(?P<datetime>[0-9]{4}[\\-][0-9]{2}[\\-][0-9]{2}.*[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}).*'
                    +r'.*lastPrice=(?P<price>[0-9]*)'
                    +r'.*highestPrice=(?P<highp>[0-9]*)'
                    +r'.*lowestPrice=(?P<lowp>[0-9]*)'
                    +r'.*bidPrice1=(?P<bidp>[0-9]*)'
                    +r'.*bidVolume1=(?P<bidv>[0-9]*)'
                    +r'.*askPrice1=(?P<askp>[0-9]*)'
                    +r'.*askVolume1=(?P<askv>[0-9]*)'
                    +r'.*instrumentID=(?P<id>[A-Z][0-9])')

puncpat = re.compile(r'[ -.\\:]')

def read_data(indexlist):
    res = config.data_format.copy()
    for i in indexlist:
        with open(config.data_file_list[i], 'r', encoding = 'utf-8') as fp:
            print('---', config.data_file_list[i], '---')
            for line in fp.readlines():
                dat = re.match(datapat, line).groupdict()
                if not dat:
                    print(line, 'can not be parsed')
                    continue
                if not dat['id'] in config.contract_list:
                    print(dat['id'], 'is not in constract list')
                    continue
                dat['datetime'] = datetime.datetime(*[int(x) for x in re.split(puncpat, dat['datetime']+'000')])
                res[dat['id']].append(dat)
    return res

if __name__ == '__main__':
    # for test
    res = read_data(range(3, 5)) # read three data file in the range
    print(res['A1'][2]['datetime'] - res['A1'][1]['datetime'])
