from NeuralNet.perceptron import Perceptron
from genetic import population, specie
import genetic.selectors as sel
import numpy as np

import copy


class GeneticPerceptron(Perceptron, specie.Specie):
    specieObject = None

    def __init__(self, numberOfInputs, seed=False):
        Perceptron.__init__(self, numberOfInputs, seed)
        self.chromosomes = [self.weights, self.bias]

    def __str__(self):
        return "Wheights: %s Fitness: %s" % (self.chromosomes, self.fitness)


class PerceptronPopulation(population.Population):
    def __init__(self):
        population.Population.__init__(self)
        self.better = GeneticPerceptron(0)
        self.better.fitness = np.NINF

    def mutate(self, specie):
        l = []
        for g in sel.chunksDivider(specie.weights, 1):
            l.extend(i for i in reversed(g * -1))

        specie.bias = np.random.random()
        specie.weights = np.array(l)
        specie.mutation = True

        return specie

    def crossOver(self, father, mother):
        a = 0.7
        child = copy.deepcopy(father)
        #child = GeneticPerceptron(father.numberOfInputs, father.seed)

        child.child = True
        child.primordial = False
        child.conditionsMet = False
        child.age = 0

        child.weights = np.array(
            (a * mother.weights) + ((1 - a) * father.weights))
        child.bias = (a * mother.bias) + ((1 - a) * father.bias)

        child.createName()

        if np.random.randint(0, 100) <= 20:
            child = self.mutate(child)

        return child