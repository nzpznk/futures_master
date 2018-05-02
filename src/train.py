from sklearn import linear_model
from label_data import get_labeled_data
from config import __models_dir__
from config import contract_list
from numpy import random
import pickle

def train(class_name, sample, label):
    model_path = __models_dir__ + class_name
    classifier = linear_model.SGDClassifier(max_iter=100000,tol=0.01,warm_start='true')
    classifier.fit(sample, label)
    with open(model_path, 'wb') as mdf:
        pickle.dump(classifier, mdf)

labeled_sample = get_labeled_data(range(20))
train_sample = {}
train_label = {}
print('loaded')
for i in ['A1', 'A3']:
    train_sample[i] = []
    train_label[i] = []
    c1 = labeled_sample[1][i].count(1)
    sum = len(labeled_sample[1][i])
    for j in range(len(labeled_sample[0][i])):
        if(labeled_sample[1][i][j] == 1):
            if(random.random() < (sum-c1)/(2*sum)):
                train_sample[i].append(labeled_sample[0][i][j])
                train_label[i].append(labeled_sample[1][i][j])
        else:
            train_sample[i].append(labeled_sample[0][i][j])
            train_label[i].append(labeled_sample[1][i][j])
    print(train_label[i].count(0), train_label[i].count(1), train_label[i].count(2))
    train(i, train_sample[i], train_label[i])