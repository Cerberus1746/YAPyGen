from numpy import random

import genetic
from genetic.cross_over import randomShuffle
from genetic.filters import simpleSplit
from genetic.genes import GeneGroup
from genetic.population import Population
from genetic.selectors import tournament


if __name__ == "__main__":    
    random.seed(0)
    
    W = 119
    A = 97
    S = 115
    D = 100

    TRAINING_EPOCHS = 5
    NUMBER_OF_SPECIES = 5
    GENES_PER_SPECIE = 2
    GROUPS_PER_SPECIE = 1

    POSSIBLE_GROUPS = [
        GeneGroup(10, 5, 2, 4, name = "weights", maxGenes = 2),
    ]

    POSSIBLE_GENES = [
        [W, W],
        [A, A],
        [S, S],
        [D, D],
    
        [W, D],
        [W, A],
        [S, D],
        [S, A]
    ]

    newPopulation = Population()

    newPopulation.setAllGenes(POSSIBLE_GENES)
    newPopulation.setAllGroups(POSSIBLE_GROUPS)

    newPopulation.generatePopulation(NUMBER_OF_SPECIES, GENES_PER_SPECIE, GROUPS_PER_SPECIE)

    for epoch in range(TRAINING_EPOCHS):
        print("\n" + "*" * 10 + "Epoch:" + str(epoch) + "*" * 10)
        print("Old Population %s" % newPopulation)
    
        newPopulation.calcFitness(genetic.FITNESS_GENE_BASED, [W, W])
        oldPopulation, newPopulation = newPopulation.filterPopulation(simpleSplit)
        toCreate = len(oldPopulation) - len(newPopulation)
        for _ in range(toCreate):
            father, mother= oldPopulation.selectParents(tournament)
            newPopulation += newPopulation.crossOver(father, mother, randomShuffle)
        print("\nNew Population %s" % newPopulation)