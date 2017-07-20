import numpy as np
import NeuralNet.perceptron as perc


class NeuralNet():
    seed = False

    training_set = []
    labels = []

    hiddenLayer = []
    outputLayer = []
    
    hiddenLayerOutput = []
    outputLayerOutput = []

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
        
    def predict(self, values):
        self.hiddenLayerOutput = []
        self.outputLayerOutput = []

        values = np.append(values, 1)
        for perceptron in self.hiddenLayer:
            self.hiddenLayerOutput.append(perceptron.netPredict(values))

        self.hiddenLayerOutput = np.append(self.hiddenLayerOutput, 1)
        for perceptron in self.outputLayer:
            self.outputLayerOutput.append(perceptron.netPredict(self.hiddenLayerOutput))

        return np.array(self.outputLayerOutput)

    def train(self, epochs, learning_rate=0.1):
        for _ in range(epochs):
            numberOfData = len(self.training_set)
            for n in range(numberOfData):
                currentSet = self.training_set[n]
                output = self.predict(currentSet)

                error = sum((self.labels[n] - output) * learning_rate)

                self.errors.append(error)
                
                print(self.hiddenLayerOutput)
    
                for n in range(len(self.hiddenLayer)):
                    self.hiddenLayer[n].weights += error
    
                for n in range(len(self.outputLayer)):
                    self.outputLayer[n].weights += error
                
                self.hiddenLayerBias += error
                self.outputLayerBias += error


if __name__ == "__main__":
    import pylab

    numberOfInputs = 2
    numberOfHiddenNodes = 3
    numberOfOutputLayers = 1

    training_set = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    labels = np.array([0, 1, 1, 1])

    net = NeuralNet(numberOfInputs, numberOfHiddenNodes,
                    numberOfOutputLayers, 1)

    net.training_set = training_set
    net.labels = labels

    net.train(1000, 0.1)

    pylab.ylim([-1, 1])
    pylab.plot(net.errors)
    pylab.show()

    print(net.predict([0, 0]))
    print(net.predict([0, 1]))
    print(net.predict([1, 0]))
    print(net.predict([0, 1]))
