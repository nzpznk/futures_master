from sklearn import linear_model
from config import __models_dir__
from label_data import get_labeled_data
import pickle

def predict(class_name, test_sample):
    model_path = __models_dir__ + class_name
    with open(model_path, 'rb') as mdf:
        classifier =  pickle.load(mdf)
    return classifier.predict(test_sample).tolist()

labeled_sample = get_labeled_data([0])
print('loaded')
for i in ['A1', 'A3']:
    result = []
    prediction = predict(i, labeled_sample[0][i])
    print(prediction)
    for j in range(len(prediction)):
        result.append(prediction[j] - labeled_sample[1][i][j])
    print(result.count(0)/len(prediction))