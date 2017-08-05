from genetic import genes, error_handling, utils, FITNESS_GENE_BASED
import copy
from numpy import random, NINF

class Dna:
    def __init__(self, *addGenes, name = "", mutable = False, maxGenes = False, maxGroups = False):
        self.name = name
        self.mutable = mutable
        self.maxGenes = maxGenes
        self.maxGroups = maxGroups
        
        self.genes = []
        self.groups = {}

        self.recessiveGenes = set()
        self.recessiveGroups = set()

        self._index = -1

        for gene in addGenes:
            if type(gene) == genes.GeneGroup:
                self.addGroup(gene)

            else:
                self.addGene(gene)

    def __iter__(self):
        return self

    def __next__(self):
        self._index += 1
        if self._index > len(self) - 1:
            self._index = -1
            raise StopIteration

        return self.values[self._index]
    
    def __len__(self):
        return len(self.genes)

    def __getitem__(self, name):
        if type(name) == str:
            if name in self.groups:
                return self.groups[name]

            raise KeyError("Group not found")

        else:
            raise AttributeError("%s object only accepts string as a key" % type(self))

    def __setitem__(self, name, value):
        if type(name) == str:
            self.groups[name] = value

        else:
            raise AttributeError("%s object only accepts string as a key" % type(self))

    def __add__(self, other):
        selfCopy = self.deepcopy()
        if type(other) == genes.Gene:
            selfCopy.addGene(other)

        elif type(other) in (genes.GeneGroup, Specie):
            selfCopy.genes += other.genes
            selfCopy.recessiveGenes.union(other.recessiveGenes)
            if len(other.groups):
                selfCopy.addMultipleGroups(list(other.groups.values()))

        else:
            return NotImplemented

        return selfCopy

    def copy(self):
        return copy.copy(self)
    
    def deepcopy(self):
        return copy.deepcopy(self)

    def get(self, name, defaultReturn = False):
        if name in self.groups:
            return self.groups[name]

        return defaultReturn
    
    def shuffleGenes(self):
        random.shuffle(self.genes)

    def setAllGenes(self, genes):
        if len(genes) > 0:
            self.genes = []
            for gene in genes:
                self.addGene(gene)
        else:
            raise error_handling.Genes("Gene List can't be empty")
    
    def setAllGroups(self, groups, setLimits = False):
        if len(groups) > 0:
            self.groups = {}
            for group in groups:
                if type(group) != GeneGroup:
                    raise AttributeError("Invalid type")

                self.addGroup(group, setLimits)
        else:
            raise error_handling.Genes("Gene List can't be empty")

    def generateRandomGeneSequence(self, possibleGenes = 0, possibleGroups = 0, numberOfGenes = 0, numberOfGroups = 0):
        if numberOfGenes == 0 and numberOfGroups == 0:
            raise AttributeError("numberOfGenes or numberOfGroups can be zero, not both")

        if numberOfGenes > 0:
            if len(possibleGenes) == 0:
                raise AttributeError("Number of Genes is set but none is defined")

            totalGenes = utils.globalChoice(possibleGenes, numberOfGenes, True)
            self.setAllGenes(totalGenes)

        if numberOfGroups > 0:
            if len(possibleGroups) == 0:
                raise AttributeError("Number of Groups is set but none is defined")

            totalGroups = utils.globalChoice(possibleGroups, numberOfGroups, True)
            self.setAllGroups(totalGroups, True)
        

    def addMultipleGenes(self, geneList):
        if len(geneList) == 0:
            raise AttributeError("geneList list can't be empty")

        for gene in geneList:
            self.addGene(gene)
    
    def addMultipleGroups(self, groupList, setLimits=False):
        if len(groupList) == 0:
            raise AttributeError("Group list can't be empty")
        for group in groupList:
            self.addGroup(group, setLimits)

    def addGene(self, newValue):
        newValueType = type(newValue)
        if newValueType == Gene:
            self.genes.append(newValue)
            self.recessiveGenes.add(newValue)

        elif newValueType in (GeneGroup, Specie):
            raise TypeError("Object of type %s is not supported by this method" % newValueType)

        else:
            self.addGene(Gene(newValue))

        return self

    def addGroup(self, newGroup, setLimits=False):
        if type(newGroup) != GeneGroup:
            raise AttributeError("Invalid type")
        
        if not self.get(newGroup.name, False):
            newGroup = newGroup.deepcopy()
            self.recessiveGroups.add(newGroup)
            self[newGroup.name] = newGroup

        else:
            self[newGroup.name] += newGroup
        
        if setLimits:
            if newGroup.maxGenes > 0 and len(newGroup.genes) > newGroup.maxGenes:
                newGroup.generateRandomGeneSequence(possibleGenes = newGroup.genes, numberOfGenes = newGroup.maxGenes)
    
            if newGroup.maxGroups > 0 and len(newGroup.groups) > newGroup.maxGroups:
                newGroup.generateRandomGeneSequence(possibleGroups = newGroup.groups, numberOfGroups = newGroup.maxGroups)

        return self

class Gene:
    def __init__(self, value, mutable = False):
        self.recessive = False
        self.groups = []
        
        self.mutable = mutable
        self.value = value

    def __add__(self, other):
        if type(other) == type(self):
            return GeneGroup(self, other)

        elif type(other) == GeneGroup:
            return other + self

    def __eq__(self, other):
        if type(self) == type(other):
            return self.__hash__() == other.__hash__()

        else:
            return NotImplemented

    def __hash__(self):
        if type(self.value) == list:
            return hash(tuple(self.value))
        else:
            return hash(self.value)

    def __repr__(self):
        return "Gene(%s)" % str(self.value)

class GeneGroup(Dna):
    def __init__(self, *values, name = "", mutable = False, maxGenes = False, maxGroups = False):
        Dna.__init__(self, *values, name = name, mutable = mutable, maxGenes = maxGenes, maxGroups = maxGroups)

    def __repr__(self):
        return "Group: %s(%s)" % (self.name, self.genes)

class Specie(Dna):
    def __init__(self, *values, name = "", maxGenes = False, maxGroups = False):
        self.fitness = NINF
        self.age = 0
        self.primordial = True
        self.child = False
        self.conditionsMet = False
        self.parents = ()
        
        genes.Dna.__init__(self, *values, name = name, maxGenes = maxGenes, maxGroups = maxGroups)

    def __repr__(self):
        return "<Specie: %s\n\tGenes(%s)\n\tGroups(%s)\n\tFitness: %s>\n" % (self.name, self.genes, list(self.groups.values()), self.fitness)

    def initChild(self, parents):
        self.fitness = NINF
        self.age = 0
        self.primordial = False
        self.child = True
        self.conditionsMet = False
        self.parents = parents


    def calcFitness(self, calculationType, handler = None):
        if calculationType == FITNESS_GENE_BASED:
            if type(handler) not in (genes.Gene, genes.GeneGroup):
                handler = Gene(handler)
            self.fitness = self.genes.count(handler)
        else:
            raise AttributeError("calculationType needs to be defined")

    def createName(self, namesOptions):
        self.speciesName = "%s.%d" % (random.choice(namesOptions), random.randint(100000))
        return self.speciesName
