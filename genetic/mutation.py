from numpy import random


def recessive(specieToMutate):
    newGenes = []
    for index in range(len(specieToMutate)):
        if random.choice((0, 1)):
            newGenes.append(random.choice(list(specieToMutate.recessiveGenes)))
        else:
            newGenes.append(specieToMutate.genes[index])
    return newGenes
