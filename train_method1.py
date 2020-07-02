
import os, csv, MyModel
from tensorflow.keras import models
import numpy as np

in_train, out_train = [], []

### Prepare training data
# headers = ['in', 'out']
record_path = 'record.csv'
with open(record_path) as f:
    record_csv = csv.DictReader(f)
    for row in record_csv:
        in_train.append(row['in'])
        out_train.append(row['out'])

x_train_origin = np.array(in_train).reshape((3,3,len(in_train)))
y_train_origin = np.array(out_train).reshape((3,3,len(in_train)))

x_train = np.concatenate(
    (x_train_origin,
     np.flip(x_train_origin),
     np.flip(x_train_origin,0),
     np.flip(x_train_origin,1))
)
y_train = np.concatenate(
    (y_train_origin,
     np.flip(y_train_origin),
     np.flip(y_train_origin,0)
     np.flip(y_train_origin,1))
)

x_train, y_train = x_train.reshape(9, x_train.shape), y_train.reshape(9, y_train.shape)

### Load the model
model_path = './models/model1/model.h5'
input_size = 9
if os.path.isfile(model_path):
    model = models.load_model(model_path)
else:
    model = MyModel()
    model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

### Set gpu auto allocate memory
gpus = tf.config.experimental.list_physical_devices(device_type='GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu,True)
    
### Train
with tf.device('/gpu:0'):
    model.fit(x_train, y_train)

model.save(model_path)
