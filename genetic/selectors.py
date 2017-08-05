from genetic import error_handling, utils

def tournament(population, numberOfSpecies = 1):
    popLen = len(population)
    winners = []

    if popLen == 0:
        raise error_handling.NoPopulation("Population list can't be empty")

    if popLen < numberOfSpecies:
        raise error_handling.NoPopulation("numberOfSpecies value is over the number of avaiable species")

    for _ in range(numberOfSpecies):
        randomPop = utils.globalChoice(population, 2)
        if randomPop[0].fitness > randomPop[1].fitness:
            winners.append(randomPop[0])

        else:
            winners.append(randomPop[1])

    return winners
