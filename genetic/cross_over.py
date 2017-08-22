def randomShuffle(mother, father):
    child = mother + father

    child.shuffleGenes()

    child.randomizeGenes(keepGroups=True, recursiveRandom=True)

    return child
