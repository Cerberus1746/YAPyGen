from numpy import random


def recessive(specieToMutate):
    newGenes = []
    for index in range(len(specieToMutate)):
        if random.choice((0, 1)):
            newGenes.append(random.choice(list(specieToMutate.recessiveGenes)))
        else:
            newGenes.append(specieToMutate.genes[index])

    for groupName, group in specieToMutate.groups.items():
        tmpGenes = []
        for index in range(len(group)):
            if random.choice((0, 1)):
                tmpGenes.append(random.choice(list(group.recessiveGenes)))
            else:
                tmpGenes.append(group.genes[index])
        specieToMutate[groupName].genes = tmpGenes

    specieToMutate.genes = newGenes

    return specieToMutate
