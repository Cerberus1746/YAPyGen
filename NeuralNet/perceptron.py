import numpy as np
import matplotlib.pyplot as plt

class Perceptron():
    def unit_step(self, x):
        return 0 if x < 0 else 1

    trainingData = []
    expectedResults = []

    epochs = 10

    weight = []
    errors = []
    weightLogs = []

    def __init__(self, numberOfInputs):
        self.weight = np.random.rand(numberOfInputs)

    def addData(self, value, expectedResult):
        self.trainingData.append(value)
        self.expectedResults.append(expectedResult)

    def train(self, epochs, eta=0.2):
        self.trainingData = np.array(self.trainingData)
        self.expectedResults = np.array(self.expectedResults)
        for _ in range(epochs):
            for n in range(len(self.trainingData)):
                x = self.trainingData[n]
                expected = self.expectedResults[n]
    
                result = np.dot(self.weight, x)
    
                error = expected - self.unit_step(result)
                self.errors.append(error)
    
                self.weight += eta * error * x
                self.weightLogs.append(self.weight)

    def predict(self, value):
        return self.unit_step(np.dot(value, self.weight))

perc = Perceptron(3)

perc.addData([0, 0, 0], 0)
perc.addData([1, 0, 0], 1)
perc.addData([1, 1, 0], 1)
perc.addData([1, 1, 1], 1)

perc.train(10)

plt.ylim([-1, 1])
plt.plot(perc.errors)
plt.show()

print(perc.predict([0, 1, 1]))
