from keras.layers import GRU
from keras.layers import Activation, Dense
import config
from keras.utils import np_utils
from keras.models import Sequential
from label_data import get_labeled_data
UNIT_SIZE = 10
TIME_STEPS = 30
INPUT_SIZE = 20
OUTPUT_SIZE = 1
from keras import backend as K
def model_structure(model):
    model.add(GRU(
        units = UNIT_SIZE,
        batch_input_shape=(None, TIME_STEPS, INPUT_SIZE),))
        #output_dim = CELL_SIZE,
        #unroll=True,))
    model.add(Dense(OUTPUT_SIZE))
    model.add(Activation('softmax'))
    model.compile(optimizer='sgd',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

train_sample, train_label = get_labeled_data('A1', 'A3', 'train_')
train_label /= 3.0
#print(train_sample)
#train_sample = train_sample.reshape(train_sample.shape[0], 1, config['image_size'], config['image_size']) / 255
#train_label = np_utils.to_categorical(train_label, config['number_types'])

K.set_image_dim_ordering('th')
#生成一个model
model = Sequential()
#model结构见model_structure.py
model_structure(model)

#batch大小设为128, 训练17轮, 验证集划分设成0.05
model.fit(train_sample, train_label, batch_size=128, epochs=17, verbose=1, validation_split=0.05)
model.save_weights(config['model_file'])
