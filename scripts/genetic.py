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
        
        populationFilter = int(len(self.species) / 2)

        filteredPopulation = self.species[:populationFilter]
        
        while len(filteredPopulation) != totalPopulation:
            father = random.choice(filteredPopulation)
            mother = random.choice(filteredPopulation)
    
            child = [min([father[0], mother[0]])]
    
            dividerPoint = int(len(father[1]) / 2)
            
            child.append(mother[1][:dividerPoint] + father[1][dividerPoint:])
            filteredPopulation.append(child)

        return filteredPopulation

if __name__ == '__main__':
    population = [
        [7.269671401648707,     [['Cube.004', 'Wheel'], ['Cube.003', 'Wheel'], ['Cube.002', 'Wheel'], ['Cube.001', 'Wheel']]],
        [7.2078545389380757,    [['Cube.004', 'Wheel'], ['Cube.003', False], ['Cube.002', 'Wheel'], ['Cube.001', 'Wheel']]],
        [5.325168709325296,     [['Cube.004', 'Wheel'], ['Cube.003', 'Wheel'], ['Cube.002', False], ['Cube.001', 'Wheel']]],
        [5.325168709325296,     [['Cube.004', False], ['Cube.003', 'Wheel'], ['Cube.002', False], ['Cube.001', 'Wheel']]],
        [0,                     [['Cube.004', False], ['Cube.003', False], ['Cube.002', False], ['Cube.001', False]]]
    ]
    geneticModule = Genetic(population)
    geneticModule.population()
    for i in geneticModule.population():
        print(i)