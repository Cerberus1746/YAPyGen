import genetic
from genetic.genes import GeneGroup, Specie, Gene
from genetic.mutation import recessive
from genetic.population import Population
from genetic.selectors import simpleSplit
from genetic.cross_over import randomShuffle


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


W = 119
A = 97
S = 115
D = 100

TRAINING_EPOCHS = 100
NUMBER_OF_SPECIES = 5
GENES_PER_SPECIE = 0
GROUPS_PER_SPECIE = 4

POSSIBLE_GROUPS = [
    GeneGroup(
        [W, W],
        [A, A],
        [S, S],
        [D, D],

        [W, D],
        [W, A],
        [S, D],
        [S, A],
        name="Actions",
        maxGenes=3
    ),
    GeneGroup(
        "Front",
        "Back",
        "Right",
        "Left",
        name="Sensors",
        maxGenes=3
    )
]

POSSIBLE_GENES = []

defaultSpecies = Specie(POSSIBLE_GROUPS[0], POSSIBLE_GROUPS[1], maxGroups=2)

def runCode():
    newPopulation = Population()

    newPopulation.generatePopulationFromSpecie(defaultSpecies, 10)

    print(BOLD + GREEN + "Initial Population" + END + END)
    print(newPopulation)

    for epoch in range(TRAINING_EPOCHS):
        print((BOLD + GREEN + "\nEpoch: {}" + END + END).format(epoch))

        newPopulation.calcFitness(genetic.FITNESS_GROUP_BASED, {"Actions" : Gene([W, W]), "Sensors" : Gene("Front")})
        oldPopulation, newPopulation = newPopulation.filterPopulation(simpleSplit)
        toCreate = len(oldPopulation) - len(newPopulation)
        for _ in range(toCreate):
            father, mother = oldPopulation.selectParents(simpleSplit)
            child = newPopulation.crossOver(father, mother, randomShuffle)
            child.mutate(15, recessive)
            child.epoch = epoch

            newPopulation += child

        print("New Population: ", newPopulation)
        print(
            (BOLD + BLUE + "Best: {}" + END + END).format(newPopulation.best)
        )

        if newPopulation.best.fitness == 6:
            return newPopulation.best

runCode()