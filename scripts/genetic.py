import random

class Genetic():
    def __init__(self, species):
        self.species = species
        
    def removeDuplicates(self, listToFilter):
        filtered = []
        for newItem in listToFilter:
            if newItem not in filtered:
                filtered.append(newItem)

        return filtered
    
    def chooseParent(self, population):
        father = random.choice(population)
        mother = random.choice(population)

        return (father, mother)
    
    def crossOver(self, father, mother):
        child = [0]
    
        dividerPoint = int(len(father[1]) / 2)
        if random.randint(0, 1):
            child.append(mother[1][:dividerPoint] + father[1][dividerPoint:])
        else:
            child.append(father[1][:dividerPoint] + mother[1][dividerPoint:])
        
        return child
    
    def population(self):
        totalPopulation = len(self.species)
        
        populationFilter = int(len(self.species) / 2) + random.randint(0, 2)

        filteredPopulation = self.species[:populationFilter]
        #filteredPopulation = [[0, y] for _, y in filteredPopulation]
        
        filteredPopulation = self.removeDuplicates(filteredPopulation)
        
        if len(filteredPopulation ) == 0:
            return filteredPopulation
        
        maxLoop = 0
        while len(filteredPopulation) < totalPopulation:
            father, mother = self.chooseParent(filteredPopulation)
    
            
            filteredPopulation.append(self.crossOver(father, mother))
            
            maxLoop += 1
            if maxLoop >= 100:
                break

        return filteredPopulation

if __name__ == '__main__':
    population = [
        [0, ['Wheel.001', 'Wheel.001', 'Wheel.001', 'Wheel.001']],
        [0, ['Wheel.001', 'Wheel', 'Wheel.001', 'Wheel.001']],
        [0, ['Wheel.001', 'Wheel', 'Wheel.001', 'Wheel.001']],
        [0, ['Wheel.001', 'Wheel', 'Wheel.001', 'Wheel.001']],
        [0, ['Wheel.001', 'Wheel', 'Wheel.001', 'Wheel.001']]
    ]
    geneticModule = Genetic(population)
    for i in geneticModule.population():
        print(i)