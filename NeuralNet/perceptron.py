import numpy as np

def sigmoid_gradient(x):
    return x * (1 - x)

def sigmoid(x):
    return 1/ (1 + np.exp(-x))

class Perceptron():
    training_set = []
    labels = []
    errors = []

    weights = []
    bias = 0

    def __init__(self, numberOfInputs, seed=False):
        if seed:
            np.random.seed(seed)

        self.weights = np.random.random(numberOfInputs)
        self.bias = np.random.random()

    def __str__(self):
        return "Wheights: %s\nBias: %f" % (self.weights, self.bias)

    def train(self, epochs, learning_rate=0.1):
        for _ in range(epochs):
            numberOfData = len(self.training_set)
            totalError = 0
            for n in range(numberOfData):
                actualTrainingSet = self.training_set[n]

                output = self.predict(actualTrainingSet)

                error = self.labels[n] - output

                totalError +=  1/(2*(error**2))
                

                self.weights += learning_rate * (error * sigmoid_gradient(output)) * actualTrainingSet
                self.bias += learning_rate * (error * sigmoid_gradient(output))

            self.errors.append(totalError)

    def predict(self, inputs):
        return sigmoid(np.dot(inputs, self.weights) + self.bias)

if __name__ == "__main__":
    import pylab
    perc = Perceptron(3, seed=1)

    perc.training_set = np.array([[0, 0, 0],
                                  [0, 1, 0],
                                  [1, 0, 0],
                                  [0, 0, 1],
                                  [1, 0, 1],
                                  [0, 1, 1],
                                  [1, 1, 0],
                                  [1, 1, 1]])

    perc.labels = np.array([0, 1, 1, 1, 1, 1, 1, 1])

    perc.train(100, 0.1)

    pylab.ylim([-1, 1])
    pylab.plot(perc.errors)
    pylab.show()

    print("[0, 0, 0] -> ?: ")
    print(perc.predict(np.array([0, 0, 0])))

    print("[0, 1, 0] -> ?: ")
    print(perc.predict(np.array([0, 1, 0])))

    print("[1, 0, 0] -> ?: ")
    print(perc.predict(np.array([1, 0, 0])))

    print("[1, 1, 1] -> ?: ")
    print(perc.predict(np.array([1, 1, 1])))
    print(perc)
