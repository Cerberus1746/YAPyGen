import genetic
from numpy import random

def mutate(specieToMutate, mutationChance, mutationType):
    if random.randint(0, 100) < mutationChance:
        newGenes = []
        if mutationType == genetic.MUTATION_RECESSIVES:
            for index in range(len(specieToMutate)):
                if random.choice((0, 1)):
                    newGenes.append(random.choice(list(specieToMutate.recessiveGenes)))
                else:
                    newGenes.append(specieToMutate.genes[index])

        specieToMutate.setAllGenes(newGenes)
    return specieToMutate