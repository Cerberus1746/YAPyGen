import yapygen.constants
from yapygen.cross_over import random_shuffle
from yapygen.genes import GeneGroup, Specie, Gene
from yapygen.mutation import recessive
from yapygen.population import Population
from yapygen.selectors import simpleSplit

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
DEFAULT_SPECIES = Specie(POSSIBLE_GROUPS[0], POSSIBLE_GROUPS[1], maxGroups=2)

def runCode():
	newPopulation = Population()

	newPopulation.generate_population_from_specie(DEFAULT_SPECIES, 10)

	print("Initial Population")
	print(newPopulation)

	for epoch in range(TRAINING_EPOCHS):
		print(("\nEpoch: {}").format(epoch))

		newPopulation.calc_fitness(yapygen.constants.FITNESS_GROUP_BASED, {
			"Actions": Gene([W, W]),
			"Sensors": Gene("Front")
		})
		oldPopulation, newPopulation = newPopulation.filter_population(
			simpleSplit)
		toCreate = len(oldPopulation) - len(newPopulation)
		for _ in range(toCreate):
			father, mother = oldPopulation.select_parents(simpleSplit)
			child = newPopulation.cross_over(father, mother, random_shuffle)
			child.mutate(15, recessive)
			child.epoch = epoch

			newPopulation += child

		print("New Population: ", newPopulation)
		print(
			("Best: {}").format(newPopulation.best)
		)

		if newPopulation.best.fitness == 6:
			return newPopulation.best


if __name__ == "__main__":
	runCode()
