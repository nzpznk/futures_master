# futures_master

周沁泓 2016010493 钮泽平 2015010467

修改说明：（2018.6.10）

1. 原报告重命名为```report_ori.pdf```，新报告为```report.pdf```
2. 此次提交主要对之前的源码进行一些除错，主要增加了可视化部分对原始数据进行分析，并计算了预测后的正确率与召回率。作业使用之前编写的源码，可利用jupyter notebook进行交互式运行，位于```./src/visualization.ipynb```
3. ```./src/visualization.ipynb```导出为```report_latest.pdf```放置于根目录下

此次修改分工如下：

周沁泓：原始期货数据标注结果可视化与召回率计算

钮泽平：特征提取后的高维数据可视化与文档撰写

------------------------------- 分割线 -------------------------

运行说明：

- 测试：运行```predict.py```使用```myModels/```目录下的模型进行测试集上的预测

- 数据生成：```futuresData/```目录下为数据集，初次运行 首先运行```read_data.py```将数据提取并存入```myDatabase/```目录下，再运行```label_data.py```生成带标记的数据存入```myDatabase/```目录下

- 训练：运行```train.py```使用myDatabase目录下的extract文件训练模型，生成模型存储在```myModels/```目录下

注意：
1. 提交的文件中包含模型，可以直接运行测试；
2. 数据生成需要将原始数据集拷贝入featuresData目录下，依次运行```read_data.py```和```label_data.py```用于生成训练需要的的带标记的数据（myDatabase目录下的extract文件）。
3. 生成带标记的数据后可以运行```train.py```进行训练
