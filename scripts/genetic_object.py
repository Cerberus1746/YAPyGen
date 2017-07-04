class Specie():
    fitness = 0
    chromosomes = []
    age = 0
    primordial = False
    speciesName = ""
    child = False
    
    def __str__(self):
        return str(self.__dict__)
    
    def createName(self):
        self.speciesName = "".join(sorted([str(x)[0:3] for x in self.chromosomes]))
        return self.speciesName

if __name__ == '__main__':
    import random

    partsOptions = ['wheelSlow', 'wheelFast', 'wheelNone']

    specie = Specie()
    specie.fitness = random.randint(1, 10)
    specie.chromosomes = []
    specie.age = random.randint(1, 10)
    for _ in range(4):
        specie.chromosomes.append(random.choice(partsOptions))

    specie.createName()

    print(specie)