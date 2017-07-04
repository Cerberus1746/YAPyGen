import random
from genetic_object import Specie

def defineCharacteristics(specieValues, **kwargs):
    for key, value in kwargs.items():
        specieValues[2][key] = value
    return specieValues

class Genetic():
    allPopulation = []
    better = None
    maxSpecieAge = 5
    minimunParts = 3
    
    def __init__(self):
        self.better = Specie()

    def tournament(self, *species):
        fitnessList = sorted([specie.fitness for specie in species])
        for specie in species:
            if specie.fitness == fitnessList[0]:
                return specie

    def mutate(self, specie):
        specie.chromosomes = list(reversed(specie.chromosomes))
        specie.mutation = True

        return specie
    
    def rouletteChoice(self, population):
        maxFitness = sum([specie.fitness for specie in population])
        pick = random.uniform(0, maxFitness)
        current = 0
        for specie in population:
            current += specie.fitness
            if current > pick:
                return specie

    def chooseParent(self, population):
        father = mother = []
        if len(population) > 2:
            while father == mother:
                father = self.rouletteChoice(population)
                mother = self.rouletteChoice(population)
            
        elif len(population) == 2:
            father = population[0]
            mother = population[1]
        else: 
            mother = father = population[0]

        return (father, mother)

    def crossOver(self, father, mother):
        try:
            def chunksDivider(listValues, chunkSize):
                return [listValues[i:i + chunkSize] for i in range(0, len(listValues), chunkSize)]
    
            child = Specie()
            freeChunks = []
    
            fatherChunks = chunksDivider(father.chromosomes, 1)
            motherChunks = chunksDivider(mother.chromosomes, 1)
            
            for chunkNumber in range(len(list(fatherChunks))):
                if random.randint(0, 1):
                    freeChunks.append(list(fatherChunks)[chunkNumber])
                else:
                    freeChunks.append(list(motherChunks)[chunkNumber])
            
            child.chromosomes = sum(list(freeChunks), [])
            
            child.child = True
    
            if random.randint(0, 100) <= 20:
                child = self.mutate(child)
    
            return child
        except IndexError:
            print("index error")
            return self.crossOver(father, mother)

    def createPopulation(self):
        totalPopulation = len(self.allPopulation)

        self.allPopulation = sorted(
            self.allPopulation,
            reverse=True,
            key=lambda specie: specie.fitness
        )

        populationFilter = (int(len(self.allPopulation) * 0.5))

        newPopulation = []
        for specie in self.allPopulation[:populationFilter]:
            if specie.age < self.maxSpecieAge and len(specie.chromosomes) >= self.minimunParts:
                newPopulation.append(specie)
                

        for n in range(len(newPopulation)):
            newPopulation[n].age += 1
        
        if self.allPopulation[0].fitness > self.better.fitness:
            self.better = self.allPopulation[0]
        
        maxLoop = 0
        while len(newPopulation) < totalPopulation:
            father, mother = self.chooseParent(self.allPopulation)
            newPopulation.append(self.crossOver(father, mother))

            maxLoop += 1
            if maxLoop >= 100:
                break

        self.allPopulation = newPopulation

        return newPopulation

if __name__ == '__main__':
    geneticModule = Genetic()
    partsOptions = ['wheelSlow', 'wheelFast', 'wheelNone']
    population = []
    
    for i in range(5):
        specie = Specie()
        specie.fitness = i
        specie.chromosomes = []
        specie.age = i if i < 10 else 3
        for _ in range(4):
            specie.chromosomes.append(random.choice(partsOptions))
        
        specie.speciesName = "".join(sorted([str(x)[0:3] for x in specie.chromosomes]))
        
        population.append(specie)

    geneticModule.allPopulation = population
    for i in geneticModule.createPopulation():
        print(i)
        #pass
    
    print("Better: " + str(geneticModule.better))
