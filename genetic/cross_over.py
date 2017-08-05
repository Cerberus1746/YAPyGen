def randomShuffle(mother, father):
    child = mother + father

    child.shuffleGenes()

    child.generateRandomGeneSequence(
        possibleGenes = child.genes,
        numberOfGenes = child.maxGenes,
        possibleGroups = list(child.groups.values()),
        numberOfGroups = child.maxGroups
    )

    for group in child.groups.values():
        group.generateRandomGeneSequence(possibleGenes = group.genes, numberOfGenes = group.maxGenes)

    return child
