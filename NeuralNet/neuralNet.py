import numpy as np
import NeuralNet.perceptron as perc
import NeuralNet.utils as utils


class NeuralNet():
    seed = False

    training_set = []
    labels = []

    hiddenLayer = []
    outputLayer = []

    hiddenLayerBias = 0
    outputLayerBias = 0

    errors = []

    def __init__(self, numberOfInputs, numberOfHiddenNodes, numberOfOutputNodes, seed=False):
        if seed:
            self.seed = seed
            np.random.seed(self.seed)

        for _ in range(numberOfHiddenNodes):
            newPerc = perc.Perceptron(
                numberOfInputs + 1, self.seed)
            self.hiddenLayer.append(newPerc)

        for _ in range(numberOfOutputNodes):
            newPerc = perc.Perceptron(
                numberOfHiddenNodes + 1, self.seed)
            self.outputLayer.append(newPerc)
        
        self.hiddenLayerBias = np.random.random()
        self.outputLayerBias = np.random.random()

    def predict(self, rawValues):
        outputs = []
        for value in rawValues:
            hiddenLayerOutput = []
            outputLayerOutput = []

            value = np.append(value, self.hiddenLayerBias)
            for perceptron in self.hiddenLayer:
                hiddenLayerOutput.append(perceptron.predict(value))

            hiddenLayerOutput = np.append(hiddenLayerOutput, self.outputLayerBias)
            for perceptron in self.outputLayer:
                outputLayerOutput.append(perceptron.predict(hiddenLayerOutput))

            outputs.append(outputLayerOutput)

        return np.array(outputs)

    def train(self, epochs, learning_rate=0.1):
        for _ in range(epochs):
            numberOfData = len(self.training_set)
            totalError = 0
            for n in range(numberOfData):
                output = self.predict([self.training_set[n]])

                error = self.labels[n] - output
                totalError += error * utils.sigmoid_gradient(output)

            totalError = sum(totalError)
            self.errors.append(totalError)
            
            adjustment = totalError * learning_rate

            for n in range(len(self.hiddenLayer)):
                self.hiddenLayer[n].weights += adjustment

            for n in range(len(self.outputLayer)):
                self.outputLayer[n].weights += adjustment
            
            self.hiddenLayerBias += adjustment
            self.outputLayerBias += adjustment


if __name__ == "__main__":
    import pylab

    numberOfInputs = 2
    numberOfHiddenNodes = 3
    numberOfOutputLayers = 1

    training_set = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    labels = np.array([0, 1, 1, 1])

    predictValues = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])

    net = NeuralNet(numberOfInputs, numberOfHiddenNodes,
                    numberOfOutputLayers, 1)

    net.training_set = training_set
    net.labels = labels

    net.train(1000, 0.1)

    pylab.ylim([-1, 1])
    pylab.plot(net.errors)
    pylab.show()

    print(net.predict(predictValues))
