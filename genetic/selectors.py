import numpy as np

def scale_linear_bycolumn(rawpoints, high=100.0, low=0.0):
    mins = np.min(rawpoints, axis=0)
    maxs = np.max(rawpoints, axis=0)
    rng = maxs - mins
    return high - (((high - low) * (maxs - rawpoints)) / rng)


def tournament(population, numberOfSpecies):
    winners = np.empty(0)

    while len(winners) < numberOfSpecies:
        randomPop = np.random.choice(population, 2)

        fitnessList = sorted([specie.fitness for specie in randomPop], reverse=True)

        for specie in randomPop:
            if specie.fitness == fitnessList[0]:
                winners = np.append(winners, specie)

    winners = sorted(
        winners,
        reverse=True,
        key=lambda specie: specie.fitness
    )

    return winners

def rouletteChoice(population):
    maxFitness = sum([specie.fitness for specie in population])
    pick = np.random.uniform(0, maxFitness)
    current = 0
    for specie in population:
        current += specie.fitness
        if current > pick:
            return specie
