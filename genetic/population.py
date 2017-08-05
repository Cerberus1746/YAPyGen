import copy

from numpy import NINF

from genetic import genes, error_handling
import genetic
from genetic.genes import Specie


class Population(genes.Dna):
    def __init__(
                self,
                *values,
                defaultSpeciesCount = False,
                specieObject = genes.Specie,
                name = "",
                maxGenes = False,
                maxGroups = False
            ):
        self._allPopulation = []

        self.specieObject = specieObject

        self.historic = []
        self.defaultSpeciesNumber = defaultSpeciesCount

        self.best = genes.Specie()

        genes.Dna.__init__(self, *values, name, maxGenes, maxGroups)

    def __getitem__(self, name):
        if type(name) == int:
            return self._allPopulation[name]
        elif type(name) == str:
            return genes.Dna.__getitem__(self, name)
        else:
            raise AttributeError("Use int to get specie from population or string to get avaiable GeneGroup")

    def __setitem__(self, name, value):
        if type(name) == int:
            self._allPopulation[name] = value
        elif type(name) == str:
            genes.Dna.__setitem__(self, name, value)
        else:
            raise AttributeError("Use int to define specie from population or string to define value of GeneGroup")

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
        if type(other) == Specie:
            self._allPopulation.append(other)
            return self
        return genes.Dna.__add__(self, other)

    def calcFitness(self, calculationType, handler = ""):
        for index in range(len(self)):
            self[index].calcFitness(calculationType, handler)

    def filterPopulation(self, filterType):
        for species in self:
            if species.fitness == NINF:
                raise error_handling.NoFitnessValue("%s have no fitness value." % species)

        oldPopulation = copy.deepcopy(self)

        self._allPopulation = sorted(self._allPopulation, reverse = True, key = lambda specie: specie.fitness)
        
        if self[0].fitness > self.best.fitness:
            self.best = self[0]

        self._allPopulation = filterType(self._allPopulation)
        return (oldPopulation, self)

    def selectParents(self, selectionType):
        return selectionType(self._allPopulation, numberOfSpecies = 2)

    def generatePopulation(self, numberOfSpecies, genesPerSpecie, groupsPerSpecie, reset = True):
        if reset:
            self._allPopulation = []
        for newSpecie in range(numberOfSpecies):
            newSpecie = self.specieObject()

            newSpecie.maxGenes = genesPerSpecie
            newSpecie.maxGroups = groupsPerSpecie

            newSpecie.generateRandomGeneSequence(
                possibleGroups = list(self.groups.values()),
                possibleGenes = self.genes,
                numberOfGenes = genesPerSpecie,
                numberOfGroups = groupsPerSpecie
            )

            self._allPopulation.append(newSpecie)

    def crossOver(self, father, mother, crossOverType, speciesNamesOptions = "default"):
            child = crossOverType(father, mother)

            child.initChild((father, mother))

            if father.name != mother.name:
                if speciesNamesOptions == "default":
                    child.createName(genetic.SPECIES_OPTIONS)
                else:
                    child.createName(speciesNamesOptions)
            else:
                child.name = father.name
            return child
