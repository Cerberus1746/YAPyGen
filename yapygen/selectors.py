from numpy import random

from yapygen import error_handling, utils


def tournament(population, **kargs):
    popLen = len(population)
    winners = []

    if popLen == 0:
        raise error_handling.NoPopulation("Population list can't be empty")

    if popLen < kargs["numberOfSpecies"]:
        raise error_handling.NoPopulation(
            "numberOfSpecies value is over the number of avaiable species")

    for _ in range(kargs["numberOfSpecies"]):
        randomPop = utils.globalChoice(population, 2)
        if randomPop[0].fitness > randomPop[1].fitness:
            winners.append(randomPop[0])

        else:
            winners.append(randomPop[1])

    return winners


def roulette(species, **kargs):
    fitnessSum = sum((sFitness.fitness for sFitness in species))
    chosenSpecies = []

    for _ in range(kargs["numberOfSpecies"]):
        randomFitness = random.random() * fitnessSum
        actualSum = 0
        for specie in species:
            actualSum += specie.fitness
            if actualSum > randomFitness:
                chosenSpecies.append(specie)
                break

    return chosenSpecies


def simpleSplit(population, **kargs):
    return population[:kargs["numberOfSpecies"]]
