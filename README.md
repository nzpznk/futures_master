# futures_master

周沁泓 2016010493 钮泽平 2015010467

### 目录结构说明:

- ```futuresData```为训练数据文件夹
- ```myDatabase```, ```labeled_data```为中间数据存储的目录
- ```lstm_method_src```为源码目录
- ```lstm_model.html```为notebook文件导出的html文件, 方便查看
- ```report.pdf```大作业报告

### 配置文件说明:

- config.py文件为配置文件
- 修改theta即更改涨跌准则
- 修改predict_st,predict_ed即为预测未来[predict_st, predict_ed]秒区间的数据
- 修改seg_time可以更改提取训练数据时的采样间隔

### 运行说明：

1. 将futuresData数据集拷贝进对应的目录

2. 进入```futures_master/lstm_method/```目录下,依次运行```read_data.py```, ```process_data.py```, ```label_data.py```进行数据的预处理.

3. 运行```jupyter notebook```, 打开notebook文件```futures_master/lstm_method/lstm_model.ipynb```即可运行, 进行训练与预测.
