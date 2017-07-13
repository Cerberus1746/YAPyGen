import numpy as np

def relu(x):
    return x * (x > 0)


def sigmoid(x):
    return 1/ (1 + np.exp(-x))

def sigmoid_gradient(x):
    return x * (1 - x)

def gaussian(x):
    return np.exp(-1 * (x**2))

def logistic(x, maximunLineValue=1, curveSteepness=1, midPoint=0):
    exponent = np.exp(-1 * (curveSteepness * (x - midPoint)))
    return maximunLineValue / (1 + exponent)





def unit_step(x):
    return 1 if x >= 0 else 0


def htan(x):
    return (np.exp(x) + np.exp(-1 * x)) / (np.exp(x) - np.exp(-1 * x))


if __name__ == "__main__":
    wheights = [4.84951189, 4.85902507, 4.8399756]
    bias = -12.337268
    
    print(logistic(np.dot([0,0,0], wheights) + bias))
    
    print(np.dot([0,0,0], wheights) + bias)