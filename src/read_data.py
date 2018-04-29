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

def read_data():
    pass
