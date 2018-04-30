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
from config import __database_dir__
import os
import re
import datetime
import pickle

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

def read_to_database(indexlist):
    for i in indexlist:
        if os.path.exists(config.data_file_list[i]) == false:
            res = config.data_format.copy()
            with open(config.data_file_list[i], 'r', encoding='utf-8') as fp:
                print('---', config.data_file_list[i], '---')
                for line in fp.readlines():
                    dat = re.match(datapat, line).groupdict()
                    if not dat:
                        print(line, 'can not be parsed')
                        continue
                    if not dat['id'] in config.contract_list:
                        print(dat['id'], 'is not in constract list')
                        continue
                    dat['datetime'] = datetime.datetime(*[int(x) for x in re.split(puncpat, dat['datetime'] + '000')])
                    res[dat['id']].append(dat)
            with open(__database_dir__ + str(i), 'wb') as dbf:
                pickle.dump(res, dbf)
                dbf.close()

def read_data(indexlist):
    res = config.data_format.copy()
    tmp = config.data_format.copy()
    for i in indexlist:
        with open(__database_dir__ + str(i), 'rb') as dbf:
            tmp = pickle.load(dbf)
        for key in res:
            res[key].append(tmp[key])
    return res


if __name__ == '__main__':
    # for test
    #read_data(range(3, 5)) # read three data file in the range
    print(read_data(range(3, 5)))
    #print(res['B2'][2]['datetime'] - res['B2'][1]['datetime'])
