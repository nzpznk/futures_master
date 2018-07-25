from config import __database_dir__, contract_list, __labeled_data_dir__
from config import contract_list, train_list, test_list
from config import train_time, seg_time, predict_st, predict_ed, theta
import numpy as np
import pickle
import h5py

# 输入: 价格列表, 初始价格下标, 用于标注的区间左端点lo,区间右端点hi,区间为[lo, hi)
# 输出: d_ab(t)
def cal_delta(prices, t0, lo, hi):
    price_st = prices[t0] # 价位参考点
    max_delta = 0
    ans = 0
    for i in range(lo, hi): # 遍历需要标注的区域
        delta = prices[i] - price_st
        if abs(delta) > max_delta: # 找变化最大的点
            ans = delta
            max_delta = abs(delta)
    return ans / price_st # 返回变化率

# 输入: datelist日期列表(共54天,列表中数字范围[0, 53]), dat_name作为输入的期货种类, lab_name预测的期货种类
# 输出: 将标注后的数据使用h5py导入文件中备用
def label_and_dump(file_num, dat_name, lab_name, train_or_test):
    dataset = []
    label = []
    with open(__database_dir__ + str(file_num) + '_' + dat_name, 'rb') as fp:
        x_time, x_price = pickle.load(fp)
    with open(__database_dir__ + str(file_num) + '_' + lab_name, 'rb') as fp:
        y_time, y_price = pickle.load(fp)
    seg_len = int(seg_time / 0.5) # 数据以每seg_time为单位切段,每段长度seg_len
    data_len = int(train_time / 0.5) # 训练数据长度
    st_len = int(predict_st / 0.5) # 预测从t时刻后st_len个数据点开始
    ed_len = int(predict_ed / 0.5) # 预测到t时刻后ed_len个数据点结束

    # 自变量分段后, 每段为[seg_len*j, seg_len*(j+1)), 每段训练数据为[seg_len*i, seg_len*i+data_len]
    # 所以合理的i应该小于(len(x)-data_len) // seg_len
    # 被标注的段为[seg_len*i+data_len+st_len, seg_len*i+data_len+ed_len), 标注参考点为seg_len*i+data_len
    # 所以合理的i应该小于(len(y)-data_len-ed_len) // seg_len
    seg_num = min((len(x_time) - data_len) // seg_len, (len(y_time) - data_len - ed_len) // seg_len)
    for i in range(seg_num):
        dataset.append(x_price[i*seg_len:i*seg_len+data_len]) # 更改为直接存入600维数据
        # 增加一个样本, 样本包含data_time时长数据,有data_len维度,以seg_len为一个时间步输入数据长度,共有data_len//seg_len时间步
        # dataset.append([ x_price[(i+j)*seg_len:seg_len*(i+j+1)] for j in range(data_len // seg_len) ])
        delta = cal_delta(y_price, i*seg_len+data_len, i*seg_len+data_len+st_len, i*seg_len+data_len+ed_len)
        # 标注
        if delta <= -theta:
            label.append(0)
        elif delta >= theta:
            label.append(2)
        else:
            label.append(1)
    # 保存入labeled_data目录下, 名称为 "数据源头文件编号_输入数据_预测的数据.h5"
    store_dir = __labeled_data_dir__ + train_or_test + lab_name + '/' + str(file_num) + '_' + dat_name + '_' + lab_name + '.h5'
    with h5py.File(store_dir, 'w') as fp:
        fp.create_dataset('dataset', data = np.array(dataset))
        fp.create_dataset('label', data = np.array(label))

# 输入: 输入期货名,被预测期货名,训练集或者测试集
# 输出: dataset, label
def get_labeled_data(dat_name, lab_name, train_or_test):
    if train_or_test == 'train_':
        file_num_list = train_list
    elif train_or_test == 'test_':
        file_num_list = test_list
    else:
        print(" train_or_test should be 'train_' or 'test_' ")
        return None
    # dataset = np.zeros((0, train_time // seg_time, seg_time * 2))
    dataset = np.zeros((0, train_time * 2))
    label = np.zeros((0))
    for i in file_num_list:
        store_dir = __labeled_data_dir__ + train_or_test + lab_name + '/' + str(i) + '_' + dat_name + '_' + lab_name + '.h5'
        with h5py.File(store_dir, 'r') as fp:
            dataset = np.vstack( (dataset, np.array(fp['dataset'])) )
            label = np.hstack( (label, np.array(fp['label'])) )
    return dataset, label

def main():
    for lab_name in contract_list:
        for train_name in contract_list:
            for i in train_list:
                label_and_dump(i, train_name, lab_name, 'train_')
            print('finished dataset_train_' + train_name + '_' + lab_name)
    for lab_name in contract_list:
        for train_name in contract_list:
            for i in test_list:
                label_and_dump(i, train_name, lab_name, 'test_')
            print('finished dataset_test_' + train_name + '_' + lab_name)

if __name__ == '__main__':
    main()
