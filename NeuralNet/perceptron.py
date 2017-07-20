import numpy as np
import NeuralNet.utils as utils


class Perceptron():
    training_set = []
    labels = []
    errors = []

    weights = []
    bias = 0
    seed = 0
    
    numberOfInputs = 0

    def __init__(self, numberOfInputs, seed=False):
        if seed:
            np.random.seed(seed)
        
        self.seed = seed
        self.numberOfInputs = numberOfInputs
        
        self.weights = np.random.random(numberOfInputs)
        self.bias = np.random.random()

    def __str__(self):
        return "Wheights: %s\nBias: %f" % (self.weights, self.bias)

    def train(self, epochs, learning_rate=0.1):
        for _ in range(epochs):
            numberOfData = len(self.training_set)

            for n in range(numberOfData):
                actualTrainingSet = self.training_set[n]

                output = self.predict(actualTrainingSet)

                error = self.labels[n] - output

                fixedError = learning_rate * error

                self.weights += fixedError * actualTrainingSet
                self.bias += fixedError

                self.errors.append(error)

    def predict(self, inputs):
        return utils.sigmoid(np.dot(inputs, self.weights) + self.bias)
    
    def netPredict(self, inputs):
        return utils.sigmoid(np.dot(inputs, self.weights))

if __name__ == "__main__":
    import pylab
    perc = Perceptron(2, seed=1)

    perc.training_set = np.array([[0, 0],
                                  [0, 1],
                                  [1, 0],
                                  [1, 1]])

    perc.labels = np.array([0, 1, 1, 1])

    perc.train(10000, .01)

    pylab.ylim([-1, 1])
    pylab.plot(perc.errors)
    pylab.show()

    print("[0, 0] -> ?: ")
    print(perc.predict(np.array([0, 0])))

    print("[0, 1] -> ?: ")
    print(perc.predict(np.array([0, 1])))

    print("[1, 0] -> ?: ")
    print(perc.predict(np.array([1, 0])))

    print("[1, 1, 1] -> ?: ")
    print(perc.predict(np.array([1, 1])))
    print(perc)
