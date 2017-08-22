import tflearn

import numpy as np


data = np.array([
    [0, 0, 0],
    [0, 0, 1],
    [0, 1, 0],
    [1, 0, 0],
    [0, 1, 1],
    [1, 1, 0],
    [1, 0, 1],
    [1, 1, 1]
])

labels = np.array([
    [1, 1, 1],
    [1, 1, 0],
    [1, 0, 1],
    [0, 1, 1],
    [1, 0, 0],
    [0, 0, 1],
    [0, 1, 0],
    [0, 0, 0]
])

net = tflearn.input_data(shape=[None, 3])
net = tflearn.fully_connected(net, 5, activation='relu')
net = tflearn.fully_connected(net, 3, activation='softmax')
net = tflearn.regression(net)

model = tflearn.DNN(net)
model.fit(data, labels, n_epoch=1000)

pred = model.predict(labels)

for result in pred:
    tmpResult = [0, 0, 0]
    tmpResult[np.argmax(result)] = 1
    print(tmpResult)
