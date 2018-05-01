from sklearn import linear_model
from label_data import get_labeled_data
from config import __models_dir__
from config import contract_list
import pickle

def train(class_name, sample, label):
    classifier = linear_model.SGDClassifier(max_iter=100000,tol=0.1,warm_start='true')
    classifier.fit(sample, label)
    model_path = __models_dir__ + class_name
    with open(model_path, 'wb') as mdf:
        pickle.dump(classifier, mdf)

labeled_sample = get_labeled_data([0,1,2])
print('loaded')
for i in ['A1', 'A3']:
    train(i, labeled_sample[0][i], labeled_sample[1][i])
    