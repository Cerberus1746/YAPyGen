import copy

from numpy import NINF

from yapygen import error_handling
from yapygen.constants import SPECIES_OPTIONS
from yapygen.genes import gene_group
from yapygen.genes import specie


class Population(gene_group.GeneGroup):
    def __init__(
        self,
        *values,
        defaultSpeciesCount=False,
        specieObject=specie.Specie,
        name="",
        maxGenes=False,
        maxGroups=False
    ):
        self._allPopulation = []

        self.specieObject = specieObject

        self.historic = []
        self.defaultSpeciesNumber = defaultSpeciesCount

        self.best = specie.Specie()

        gene_group.GeneGroup.__init__(self, *values, name, maxGenes, maxGroups)

    def __getitem__(self, name):
        if isinstance(name, int):
            return self._allPopulation[name]
        elif isinstance(name, str):
            return gene_group.GeneGroup.__getitem__(self, name)
        else:
            raise AttributeError(
                "Use int to getGroup specie from population or string to getGroup avaiable GeneGroup"
            )

    def __setitem__(self, name, value):
        if isinstance(name, int):
            self._allPopulation[name] = value
        elif isinstance(name, str):
            gene_group.GeneGroup.__setitem__(self, name, value)
        else:
            raise AttributeError(
                "Use int to define specie from population or string to define value of GeneGroup"
            )

    def __iter__(self):
        return self

    def __next__(self):
        self._index += 1
        if self._index > len(self._allPopulation) - 1:
            self._index = -1
            raise StopIteration
        return self._allPopulation[self._index]

    def __repr__(self):
        return "Population: %s" % self._allPopulation

    def __len__(self):
        return len(self._allPopulation)

    def __add__(self, other):
        if isinstance(other, specie.Specie):
            self._allPopulation.append(other)
            return self
        return gene_group.GeneGroup.__add__(self, other)

    def calc_fitness(self, calculationType, handler=""):
        for index in range(len(self)):
            self[index].calc_fitness(calculationType, handler)

    def filter_population(self, filterType, **kargs):
        for sIndex, specie in enumerate(self):
            if specie.fitness == NINF:
                raise error_handling.NoFitnessValue(
                    "%s have no fitness value." % specie
                )

            self[sIndex].age += 1
            if kargs.get("maxAge", False):
                if specie.age > kargs["maxAge"]:
                    del (self[sIndex])

        if "numberOfSpecies" not in kargs:
            kargs["numberOfSpecies"] = int(len(self) / 2)

        oldPopulation = copy.deepcopy(self)
        self._allPopulation = sorted(
            self._allPopulation, reverse=True, key=lambda specie: specie.fitness
        )

        if self[0].fitness > self.best.fitness:
            self.best = self[0]

        self._allPopulation = filterType(self._allPopulation, **kargs)
        return (oldPopulation, self)

    def select_parents(self, selectionType):
        return selectionType(self._allPopulation, numberOfSpecies=2)

    def generate_population(
        self, numberOfSpecies, genesPerSpecie, groupsPerSpecie, reset=True
    ):
        if reset:
            self._allPopulation = []
        for newSpecie in range(numberOfSpecies):
            newSpecie = self.specieObject()

            newSpecie.maxGenes = genesPerSpecie
            newSpecie.maxGroups = groupsPerSpecie

            newSpecie.generate_random_gene_sequence(
                possibleGroups=list(self.groups.values()),
                possibleGenes=self.genes,
                numberOfGenes=genesPerSpecie,
                numberOfGroups=groupsPerSpecie,
            )

            self._allPopulation.append(newSpecie)

    def generate_population_from_specie(self, baseSpecie, numberOfSpecie):
        tmpPopulation = []
        for _ in range(numberOfSpecie):
            tmpNewSpecie = baseSpecie.deepcopy()
            differentiate = getattr(tmpNewSpecie, "differentiation", None)
            if callable(differentiate):
                tmpNewSpecie.differentiation()
            else:
                tmpNewSpecie.randomize_genes(keepGroups=True, recursiveRandom=True)

            tmpPopulation.append(tmpNewSpecie)

        self._allPopulation = tmpPopulation

    def cross_over(self, father, mother, crossOverType, speciesNamesOptions="default"):
        child = crossOverType(father, mother)

        child.init_child((father, mother))

        if father.name != mother.name:
            if speciesNamesOptions == "default":
                child.create_name(SPECIES_OPTIONS)
            else:
                child.create_name(speciesNamesOptions)
        else:
            child.name = father.name
        return child
