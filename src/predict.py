from sklearn import linear_model
from config import __models_dir__
from config import test_sample
from label_data import get_labeled_data
from config import contract_list
import pickle

def predict(class_name, test_sample):
    model_path = __models_dir__ + class_name
    with open(model_path, 'rb') as mdf:
        classifier =  pickle.load(mdf)
    return classifier.predict(test_sample).tolist()

labeled_sample = get_labeled_data(test_sample)
print('loaded')
for i in contract_list:
    result = []
    prediction = predict(i, labeled_sample[0][i])
    for j in range(len(prediction)):
        result.append(prediction[j] + 3 * labeled_sample[1][i][j])
    accuracy = (result.count(8) + result.count(4) + result.count(0)) / len(result)
    recall_up = result.count(8) / (result.count(6) + result.count(7) + result.count(8))
    recall_down = result.count(0) / (result.count(0) + result.count(1) + result.count(2))
    recall_flat = result.count(4) / (result.count(3) + result.count(4) + result.count(5))
    print('Model', i, 'accuracy : ',accuracy)
    print('Model', i, 'recall up : ',recall_up)
    print('Model', i, 'recall down : ',recall_down)
    print('Model', i, 'recall flat : ',recall_flat, '\n')