import random

import numpy as np


def scale_linear_bycolumn(rawpoints, high=100.0, low=0.0):
    mins = np.min(rawpoints, axis=0)
    maxs = np.max(rawpoints, axis=0)
    rng = maxs - mins
    return high - (((high - low) * (maxs - rawpoints)) / rng)

def gradientRandomSelection(sequence, numberOfElementsToRemove):
    numberOfItens = len(sequence)
    rangeList = range(numberOfItens)
    listCopy = list(sequence)
    
    indexes = np.random.choice(
        rangeList,
        size=numberOfElementsToRemove,
        replace=False,
        p=scale_linear_bycolumn(range(numberOfItens, 0, -1),
        (1 / numberOfItens) * 2)
    )

    for index in sorted(indexes, reverse=True):
        del listCopy[index]

    return listCopy
    
def chunksDivider(listValues, chunkSize):
    return [listValues[i:i + chunkSize] for i in range(0, len(listValues), chunkSize)]
    
def selRandom(species, n):
    return [random.choice(species) for _ in range(n)]

def tournament(population, numberOfSpecies):
    winners = []

    while len(winners) < numberOfSpecies:
        randomPop = selRandom(population, 2)

        fitnessList = sorted([specie.fitness for specie in randomPop], reverse=True)
        for specie in randomPop:
            if specie.fitness == fitnessList[0]:
                winners.append(specie)
    winners = sorted(
        winners,
        reverse=True,
        key=lambda specie: specie.fitness
    )
    return winners

def rouletteChoice(population):
    maxFitness = sum([specie.fitness for specie in population])
    pick = random.uniform(0, maxFitness)
    current = 0
    for specie in population:
        current += specie.fitness
        if current > pick:
            return specie
