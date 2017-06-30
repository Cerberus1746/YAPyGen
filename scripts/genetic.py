class Genetic():
    def __init__(self, species):
        self.species = species
    
    def population(self):
        filteredPopulation = []
        for specie in self.species:
            if specie[0] > 1:
                filteredPopulation.append(specie)
        return filteredPopulation