import copy

import genetic.selectors as sel
from genetic.specie import Specie
import numpy as np


class NoFitnessValue(Exception):
    pass


class NoChromosomes(Exception):
    pass


class Population():
    allPopulation = np.empty(0, dtype=Specie)
    better = None
    maxSpecieAge = 5
    historic = list()
    
    namesOptions = ["buffalo", "dog", "cat", "merkat", "dolphin", "croc", "alpaca", "raven"]

    def __init__(self):
        self.better = Specie()
        self.better.fitness = np.NINF

    def mutate(self, specie):
        l = np.empty(0)
        for g in np.array_split(specie.chromosomes, 3):
            l = np.append(l, g[::-1])

        specie.chromosomes = l
        specie.mutation = True

        return specie

    def chooseParent(self, population):
        father = mother = None
        while father == mother:
            father = sel.tournament(population, 1)[0]
            mother = sel.tournament(population, 1)[0]

        return (father, mother)

    def crossOver(self, father, mother):
        chromosomesCount = len(father.chromosomes)
        child = copy.deepcopy(father)

        child.fitness = np.NINF
        child.chromosomes = np.empty(0)
        child.age = 0
        child.primordial = False
        child.child = True
        child.conditionsMet = False
        child.father = father
        child.mother = mother
        
        '''if father.speciesName != mother.speciesName:
            child.createName(self.namesOptions)'''

        while len(child.chromosomes) != chromosomesCount:
            if np.random.randint(0, 1):
                child.chromosomes = np.append(child.chromosomes, np.random.choice(father.chromosomes))
            else:
                child.chromosomes = np.append(child.chromosomes, np.random.choice(mother.chromosomes))

        if np.random.randint(0, 100) <= 20:
            child = self.mutate(child)

        return child

    def createPopulation(self):
        self.populationCount = len(self.allPopulation)


        self.allPopulation = sorted(
            self.allPopulation,
            reverse=True,
            key=lambda specie: specie.fitness
        )

        populationFilter = int(self.populationCount / 2)
        
        tmpHistoric = []
        for n in range(self.populationCount):
            currentSpecie = self.allPopulation[n]
            
            tmpHistoric.append(currentSpecie.__dict__)
            currentSpecie.age += 1
        
        self.historic.append(tmpHistoric)

        newPopulation = np.empty(0)
        for specie in self.allPopulation[:populationFilter]:
            if len(specie.chromosomes) == 0:
                raise NoChromosomes("Chromosomes list is empty in one of the objects")
            if specie.age <= self.maxSpecieAge:
                newPopulation = np.append(newPopulation, specie)

        while len(newPopulation) < self.populationCount:
            father, mother = self.chooseParent(self.allPopulation)
            newPopulation = np.append(newPopulation, self.crossOver(father, mother))

        self.allPopulation = newPopulation
        
        if self.allPopulation[0].fitness > self.better.fitness:
            self.better = self.allPopulation[0]

        return self.allPopulation


if __name__ == '__main__':
    import pandas as pd
    import matplotlib.pyplot as plt
    
    #plt.style.use('ggplot')

    geneticModule = Population()
    partsOptions = [119., 97., 100., 115.]
    population = []
    
    numberOfGenomes = 2

    for i in range(5):
        specie = Specie()
        for _ in range(numberOfGenomes):
            specie.chromosomes = np.append(np.array(specie.chromosomes), np.random.choice(partsOptions))

        specie.createName(geneticModule.namesOptions)

        population.append(specie)
    
    def run(population, numberOfGenomes):
        geneticModule.allPopulation = population
        end = False
        for _ in range(100):
            for i in range(len(geneticModule.allPopulation)):
                actualSpecie = geneticModule.allPopulation[i]
                actualSpecie.fitness = int(np.count_nonzero(actualSpecie.chromosomes == 119.))
                if actualSpecie.fitness == numberOfGenomes:
                    print("Converged", actualSpecie)
                    end = True
            
            geneticModule.createPopulation()
            if end:
                return geneticModule
    
        return False
    
    geneticModule = run(population, numberOfGenomes)
    
    if geneticModule:
        print([pd.DataFrame(epoch) for epoch in geneticModule.historic])
        
    else:
        print("Fail")