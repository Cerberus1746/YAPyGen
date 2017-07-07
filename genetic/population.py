import random
import genetic.selectors as sel

from genetic.specie import Specie


class Population():
    allPopulation = []
    better = None
    maxSpecieAge = 10
    minimunParts = 3
    
    def __init__(self):
        self.better = Specie()

    def mutate(self, specie):
        l = []
        for g in sel.chunksDivider(specie.chromosomes, 2):
            l.extend(i for i in reversed(g))

        specie.chromosomes = l
        specie.mutation = True

        return specie

    def chooseParent(self, population):
        father = mother = []
        if len(population) > 2:
            while father == mother:
                father = sel.rouletteChoice(population)
                mother = sel.rouletteChoice(population)
            
        elif len(population) == 2:
            father = population[0]
            mother = population[1]
        else: 
            mother = father = population[0]

        return (father, mother)

    def crossOver(self, father, mother):

        child = Specie()
        freeChunks = []

        fatherChunks = sel.chunksDivider(father.chromosomes, 1)
        motherChunks = sel.chunksDivider(mother.chromosomes, 1)
        
        for chunkNumber in range(len(list(fatherChunks))):
            if random.randint(0, 1):
                freeChunks.append(list(fatherChunks)[chunkNumber])
            else:
                freeChunks.append(list(motherChunks)[chunkNumber])
        
        child.chromosomes = sum(list(freeChunks), [])
        child.createName()
        
        child.child = True

        if random.randint(0, 100) <= 20:
            child = self.mutate(child)

        return child

    def createPopulation(self):
        self.totalPopulation = len(self.allPopulation)

        self.allPopulation = sorted(
            self.allPopulation,
            reverse=True,
            key=lambda specie: specie.fitness
        )
        
        if self.allPopulation[0].fitness > self.better.fitness:
            self.better = self.allPopulation[0]

        populationFilter = int(len(self.allPopulation) * 0.5) + 1

        newPopulation = []
        for specie in self.allPopulation:
            if specie.age < self.maxSpecieAge and len(specie.chromosomes) >= self.minimunParts:
                newPopulation.append(specie)

        newPopulation = sel.gradientRandomSelection(newPopulation, populationFilter)

        if not (self.better in newPopulation) and self.better.age < self.maxSpecieAge:
            newPopulation.insert(0, self.better)

        for n in range(len(newPopulation)):
            newPopulation[n].age += 1
        
        maxLoop = 0
        while len(newPopulation) < self.totalPopulation:
            father, mother = self.chooseParent(self.allPopulation)
            newPopulation.append(self.crossOver(father, mother))

            maxLoop += 1
            if maxLoop >= 100:
                break

        self.allPopulation = newPopulation

        return newPopulation

if __name__ == '__main__':
    geneticModule = Population()
    partsOptions = ['wheelSlow', 'wheelFast', 'wheelNone']
    population = []
    
    for i in range(10):
        specie = Specie()
        specie.fitness = i
        specie.chromosomes = []
        specie.age = i if i < 10 else 3
        for _ in range(4):
            specie.chromosomes.append(random.choice(partsOptions))
        
        specie.createName()
        
        population.append(specie)

    geneticModule.allPopulation = population
    for i in geneticModule.createPopulation():
        print(i)
        # pass
    
    print("Better: " + str(geneticModule.better))
