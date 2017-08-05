from numpy import random

import genetic
from genetic.cross_over import randomShuffle
from genetic.filters import simpleSplit
from genetic.population import Population
from genetic.selectors import tournament
from genetic.mutation import mutate

class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

if __name__ == "__main__":    
    random.seed(0)
    
    W = 119
    A = 97
    S = 115
    D = 100
    
    TRAINING_EPOCHS = 100000
    NUMBER_OF_SPECIES = 10
    GENES_PER_SPECIE = 10
    GROUPS_PER_SPECIE = 0
    
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

    def runCode():
        newPopulation = Population()
    
        newPopulation.setAllGenes(POSSIBLE_GENES)
        newPopulation.generatePopulation(NUMBER_OF_SPECIES, GENES_PER_SPECIE, GROUPS_PER_SPECIE)
        
        print(Color.BOLD + Color.GREEN + "Initial Population" + Color.END)
        print(newPopulation)
    
        for epoch in range(TRAINING_EPOCHS):
            print((Color.BOLD + Color.GREEN + "\nEpoch: %d" + Color.END) % epoch)
            
            newPopulation.calcFitness(genetic.FITNESS_GENE_BASED, [S, S])
            oldPopulation, newPopulation = newPopulation.filterPopulation(simpleSplit)
            toCreate = len(oldPopulation) - len(newPopulation)
            for _ in range(toCreate):
                father, mother = oldPopulation.selectParents(tournament)
                child = newPopulation.crossOver(father, mother, randomShuffle)
                child = mutate(child, 25, genetic.MUTATION_RECESSIVES)
    
                newPopulation += child
    
            print("New Population: ", newPopulation)
            print((Color.BOLD + Color.BLUE + "Best: %s" + Color.END) % newPopulation.best)
    
            if newPopulation.best.fitness == GENES_PER_SPECIE:
                return
    
    runCode()