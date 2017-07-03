import random
import genetic_object

def defineCharacteristics(specieValues, **kwargs):
    for key, value in kwargs.items():
        specieValues[2][key] = value
    return specieValues

class Genetic():
    allPopulation = []
    better = [0,0]
    maxSpecieAge = 5
    minimunParts = 3

    def tournament(self, *species):
        fitnessList = sorted([specie[0] for specie in species])
        for specie in species:
            if specie[0] == fitnessList[0]:
                return specie

    def mutate(self, specie):
        newSpecie = list(reversed(specie[1]))

        return [0, newSpecie, specie[2]]
    
    def rouletteChoice(self, population):
        maxFitness = sum([specie[0] for specie in population])
        pick = random.uniform(0, maxFitness)
        current = 0
        for specie in population:
            current += specie[0]
            if current > pick:
                return specie

    def chooseParent(self, population):
        father = mother = []
        while father == mother:
            father = self.rouletteChoice(population)
            mother = self.rouletteChoice(population)

        return (father, mother)

    def crossOver(self, father, mother):
        try:
            def chunksDivider(listValues, chunkSize):
                return [listValues[i:i + chunkSize] for i in range(0, len(listValues), chunkSize)]
    
            child = []
    
            fatherChunks = chunksDivider(father[1], 1)
            motherChunks = chunksDivider(mother[1], 1)
    
            for chunkNumber in range(len(list(fatherChunks))):
                if random.randint(0, 1):
                    child.append(list(fatherChunks)[chunkNumber])
                else:
                    child.append(list(motherChunks)[chunkNumber])
    
            child = sum(child, [])
            child = [0, child, {"child" : True, "species" : "".join(sorted([str(x)[0:3] for x in child]))}]
            
            defineCharacteristics(child, age = 0)
    
            if random.randint(0, 100) <= 20:
                child = defineCharacteristics(self.mutate(child), mutation = True)
    
            return child
        except IndexError:
            print("index error")
            return self.crossOver(father, mother)

    def createPopulation(self):
        totalPopulation = len(self.allPopulation)
        
        populationFilter = (
            int(len(self.allPopulation) * 0.3) +
            random.randint(0, int(len(self.allPopulation) * 0.20))
        )

        filteredPopulation = []
        for specie in self.allPopulation[:populationFilter]:
            if specie[2]["age"] < self.maxSpecieAge and len(specie[1]) >= self.minimunParts:
                filteredPopulation.append(specie)

        for n in range(len(filteredPopulation)):
            filteredPopulation[n][2]["age"] += 1
        
        if self.allPopulation[0][0] > self.better[0]:
            self.better = self.allPopulation[0]
        
        newPopulation = filteredPopulation

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
    geneticModule.allPopulation = [[8.265524713686293, ['wheelSlow', 'wheelFast', 'wheelFast', 'wheelFast'], {'age': 0, 'primordial': True}], [6.419438942671523, ['wheelSlow', 'none', 'none', 'wheelSlow'], {'age': 0, 'primordial': True}], [5.976333470045203, ['none', 'wheelFast', False, 'wheelFast'], {'age': 0, 'primordial': True}], [4.714227811853874, ['wheelFast', 'wheelFast', 'none', 'wheelSlow'], {'age': 0, 'primordial': True}], [4.482450498839169, ['none', 'wheelFast', 'wheelSlow', 'none'], {'age': 0, 'primordial': True}], [4.313566315963144, ['none', 'wheelSlow', False, 'wheelSlow'], {'age': 0, 'primordial': True}], [3.9939199693133602, ['wheelSlow', False, 'none', 'wheelSlow'], {'age': 0, 'primordial': True}], [3.3443714369845763, ['wheelSlow', 'wheelSlow', 'none', False], {'age': 0, 'primordial': True}], [3.1471945051321697, ['wheelSlow', 'none', 'wheelSlow', False], {'age': 0, 'primordial': True}], [3.0581027916275207, ['wheelFast', False, 'wheelSlow', 'none'], {'age': 0, 'primordial': True}], [3.030021886784759, ['wheelSlow', 'none', 'none', 'none'], {'age': 0, 'primordial': True}], [2.712929452799508, ['wheelFast', 'none', 'none', 'none'], {'age': 0, 'primordial': True}], [2.604375134047834, [False, 'none', 'wheelSlow', 'none'], {'age': 0, 'primordial': True}], [2.0014527878808157, ['none', False, 'wheelSlow', False], {'age': 0, 'primordial': True}], [1.6315843992109809, [False, False, 'wheelFast', 'wheelFast'], {'age': 0, 'primordial': True}]]
    for i in geneticModule.createPopulation():
        print(i)
        #pass
    print("Better: " + str(geneticModule.better))
