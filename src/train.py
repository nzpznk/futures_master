from sklearn import linear_model
from label_data import get_labeled_data
from config import __models_dir__
import pickle

def train(class_name, sample, label):
    classifier = linear_model.SGDClassifier(max_iter=100000000,tol=0.0001)
    classifier.fit(sample, label)
    model_path = __models_dir__ + class_name
    with open(model_path, 'wb') as mdf:
        pickle.dump(classifier, mdf)

