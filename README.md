futures_master

周沁泓 2016010493 钮泽平 2015010467

运行说明：

- 测试：运行```predict.py```使用```myModels/```目录下的模型进行测试集上的预测

- 数据生成：```futuresData/```目录下为数据集，初次运行 首先运行```read_data.py```将数据提取并存入```myDatabase/```目录下，再运行```label_data.py```生成带标记的数据存入```myDatabase/```目录下

- 训练：运行```train.py```使用myDatabase目录下的extract文件训练模型，生成模型存储在```myModels/```目录下

注意：
1. 提交的文件中包含模型，可以直接运行测试；
2. 数据生成需要将原始数据集拷贝入featuresData目录下，依次运行```read_data.py```和```label_data.py```用于生成训练需要的的带标记的数据（myDatabase目录下的extract文件）。
3. 生成带标记的数据后可以运行```train.py```进行训练

