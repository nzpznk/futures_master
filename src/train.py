from sklearn import linear_model
from label_data import get_labeled_data
from config import __models_dir__
from config import contract_list
import pickle

def train(class_name, sample, label):
    classifier = linear_model.SGDClassifier(max_iter=100000000,tol=0.0001)
    classifier.fit(sample, label)
    model_path = __models_dir__ + class_name
    with open(model_path, 'wb') as mdf:
        pickle.dump(classifier, mdf)

labeled_sample = get_labeled_data()
for i in contract_list:
    train(i, labeled_sample[0][i], labeled_sample[1][i])
    