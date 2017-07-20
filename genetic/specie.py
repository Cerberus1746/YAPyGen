import numpy as np


class Specie():
    fitness = np.NINF
    chromosomes = np.empty(0)
    age = 0
    primordial = True
    speciesName = ""
    child = False
    conditionsMet = False
    father = None
    mother = None

    def __str__(self):
        return str(self.__dict__)

    def createName(self, namesOptions):
        self.speciesName = "%s.%d" % (np.random.choice(namesOptions), np.random.randint(1000))
        return self.speciesName