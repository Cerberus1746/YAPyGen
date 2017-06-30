import random

class Genetic():
    def __init__(self, species):
        self.species = species
    
    def population(self):
        totalPopulation = len(self.species)
        filteredPopulation = []
        father = []
        mother = []

        if totalPopulation == 0:
            return filteredPopulation
        
        populationFilter = int(len(self.species) / 2) + random.randint(0, 2)

        filteredPopulation = self.species[:populationFilter]
        filteredPopulation.append(self.species[-random.randint(2, 3)])
        
        while len(filteredPopulation) != totalPopulation:
            father = random.choice(filteredPopulation)
            mother = random.choice(filteredPopulation)
    
            child = [min([father[0], mother[0]])]
    
            dividerPoint = int(len(father[1]) / 2)
            if random.randint(0, 1):
                child.append(mother[1][:dividerPoint] + father[1][dividerPoint:])
            else:
                child.append(father[1][:dividerPoint] + mother[1][dividerPoint:])
            filteredPopulation.append(child)

        return filteredPopulation

if __name__ == '__main__':
    population = [
            [8.2092895426450347, ['Wheel', 'Wheel', 'Wheel', 'Wheel', 'Wheel', 'Wheel']],
            [7.4524994882128963, ['Wheel', 'Wheel', 'Wheel', False, 'Wheel', 'Wheel']],
            [6.5146376491401679, ['Wheel', 'Wheel', False, 'Wheel', False, 'Wheel']],
            [7.4524994882128963, ['Wheel', 'Wheel', 'Wheel', False, 'Wheel', 'Wheel']],
            [7.4524994882128963, ['Wheel', 'Wheel', 'Wheel', False, 'Wheel', 'Wheel']]
        ]
    geneticModule = Genetic(population)
    geneticModule.population()
    for i in geneticModule.population():
        print(i)