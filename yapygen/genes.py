import copy

from numpy import random, NINF

from yapygen import genes, error_handling, utils, FITNESS_GENE_BASED, FITNESS_GROUP_BASED


class GeneGroup:
    '''
    Main class used for all types of objects, but for the Gene object.
    GeneGroups are the object used to keep multiple Genes inside.
    '''
    def __init__(self, *addGenes, name="", maxGenes=0, maxGroups=0):
        '''
        Create the group

        :param addGenes: Add genes to the group, anything that is not a GeneGroup will be converted to a Gene object.
        Any inserted gene will be added to the recessive genes too.
        :param str name: Name of the group. Groups with same names will be crossed over depending on the use.
        :param int maxGenes: Maximun number of genes.
        :param int maxGroups: Maximun numbers of groups.
        '''
        
        self.name = name
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

    def __iterable__(self):
        '''
        Iterator. It will iterableate along the genes.
        '''
        return self

    def __next__(self):
        '''
        Next Gene.
        '''
        self._index += 1
        if self._index > len(self) - 1:
            self._index = -1
            raise StopIteration

        return self.genes[self._index]

    def __len__(self):
        '''
        Number of Genes
        '''
        return len(self.genes)

    def __getitem__(self, name):
        '''
        Get group.

        :param str name: Name of the group to get.

        :raises KeyError: if the group is not found.
        :raises AttributeError: if key is not a string.
        '''
        if type(name) == str:
            if name in self.groups:
                return self.groups[name]

            raise KeyError("Group not found")

        else:
            raise AttributeError("%s object only accepts string as a key" % type(self))

    def __setitem__(self, name, value):
        '''
        Set value of the group, it needs to be a GeneGroup too.

        :param str name: Name of the new group or name of the group to create. This value will overlay the group name.
        :param GeneGroup value: New Group.
        :raises AttributeError: If value is not a GeneGroup or if key is not string.
        '''
        if type(name) == str:
            if type(value) != GeneGroup:
                raise AttributeError("Value must be a GeneGroup")
            value.name = name
            self.groups[name] = value

        else:
            raise AttributeError("%s object only accepts string as a key" % type(self))

    def __add__(self, other):
        '''
        Add Gene or GeneGroup to Group

        :param other: GeneGroup or Gene to add.
        '''
        selfCopy = self.deepcopy()
        if type(other) == genes.Gene:
            selfCopy.addGene(other)

        elif type(other) == GeneGroup:
            selfCopy.genes += other.genes
            selfCopy.recessiveGenes.union(other.recessiveGenes)
            if len(other.groups):
                selfCopy.addMultipleGroups(list(other.groups.values()))

        else:
            return NotImplemented

        return selfCopy

    def __repr__(self):
        '''
        Representation of the GeneGroup
        '''
        return "\n\tGeneGroup: {} Genes({:_<10}) Groups({})".format(
            self.name,
            str(self.genes),
            list(self.groups.values()) if len(self.groups) > 0 else "No Groups"
        )

    def copy(self):
        '''Copy the object.'''
        return copy.copy(self)

    def deepcopy(self):
        '''Copy group recursively.'''
        return copy.deepcopy(self)

    def getGroup(self, name, defaultReturn=False):
        '''Get group, if group don't exist, return defaultReturn

        :param str name: name of the group to get
        :param bool defaultReturn: value to return if group is not found.
        '''
        if name in self.groups:
            return self.groups[name]

        return defaultReturn

    def shuffleGenes(self):
        '''Randomize position of the genes.'''
        random.shuffle(self.genes)

    def setAllGenes(self, genes):
        '''Reset genes and add new ones

        :param iterable genes: list of genes to add.
        '''
        if len(genes) > 0:
            self.genes = []
            for gene in genes:
                self.addGene(gene)
        else:
            raise error_handling.Genes("Gene List can't be empty")

    def setAllGroups(self, groups, setLimits=False):
        '''Reset groups and add new ones. If set limits is true, remove the excess genes randomly.
        
        :param iterable groups: New Groups to add.
        :param bool setLimits: Remove excess genes or not.
        '''
        if len(groups) > 0:
            self.groups = {}
            for group in groups:
                if type(group) != GeneGroup:
                    raise AttributeError("Invalid type")

                self.addGroup(group, setLimits)
        else:
            raise error_handling.Genes("Gene List can't be empty")

    def generateRandomGeneSequence(self, possibleGenes=0, possibleGroups=0, numberOfGenes=0, numberOfGroups=0):
        '''Create gene sequence randomly based on the supplied GeneGroups or Genes.
        
        :param iterable possibleGenes: List of possible genes to choose.
        :param iterable possibleGroups: List of possible GeneGroups to choose.
        :param int numberOfGenes: Number of Genes to add.
        :param int numberOfGroups: Number of GeneGroups to add.
        '''
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
    
    def randomizeGenes(self, keepGroups=False, recursiveRandom=False):
        '''Randomize genes or randomize genes inside group.
        
        :param bool keepGroups: If True: Do not erase or add new groups, keep them the same.
        :param bool recursiveRandom: Recursively randomize genes inside groups too.
        '''
        if not keepGroups:
            self.generateRandomGeneSequence(
                possibleGenes=self.genes,
                possibleGroups=list(self.groups.values()),
                numberOfGenes=self.maxGenes,
                numberOfGroups=self.maxGroups)
        else:
            if self.maxGenes > 0:
                self.generateRandomGeneSequence(possibleGenes=self.genes, numberOfGenes=self.maxGenes)
        
        for groupName, group in self.groups.items():
            group.randomizeGenes(keepGroups=recursiveRandom)
            self[groupName] = group


    def addMultipleGenes(self, geneList):
        '''Add list of genes, any variable that isn't a gene will be transformed into one.
        
        :param iterable geneList: List of Genes to ADD
        '''
        if len(geneList) == 0:
            raise AttributeError("geneList value can't be empty")

        for gene in geneList:
            if type(gene) == GeneGroup:
                raise AttributeError
            self.addGene(gene)

    def addMultipleGroups(self, groupList, setLimits=False):
        '''Add list of Groups
        
        :param groupList: List of groups to add.
        :param setLimits: Remove excess genes or not.
        '''
        if len(groupList) == 0:
            raise AttributeError("Group list can't be empty")
        for group in groupList:
            self.addGroup(group, setLimits)

    def addGene(self, newValue):
        '''Add new gene.
        
        :param newValue: Gene to add, if any object is added they will be converted to Gene object automatically
        '''
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
        '''Add new group
        
        :param newGroup: Group to be added.
        :param setLimits: Remove excess genes or not.
        '''
        if type(newGroup) != GeneGroup:
            raise AttributeError("Invalid type")

        if not self.getGroup(newGroup.name, False):
            newGroup = newGroup.deepcopy()
            self.recessiveGroups.add(newGroup)
            self[newGroup.name] = newGroup

        else:
            self[newGroup.name] += newGroup

        if setLimits:
            if newGroup.maxGenes > 0 and len(newGroup.genes) > newGroup.maxGenes:
                newGroup.generateRandomGeneSequence(possibleGenes=newGroup.genes, numberOfGenes=newGroup.maxGenes)

            if newGroup.maxGroups > 0 and len(newGroup.groups) > newGroup.maxGroups:
                newGroup.generateRandomGeneSequence(possibleGroups=newGroup.groups, numberOfGroups=newGroup.maxGroups)

        return self


class Gene:
    '''Basic object for the yapygen processing.'''
    def __init__(self, value):
        '''Create a new gene
        
        :param value: Value to be used.
        '''
        self.recessive = False
        self.groups = []

        self.value = value

    def __add__(self, other):
        if type(other) == type(self):
            return GeneGroup(self, other)

        else:
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
        return "\n\tGene(%s)" % str(self.value)


class Specie(GeneGroup):
    def __init__(self, *values, name="", maxGenes=False, maxGroups=False):
        self.fitness = NINF
        self.age = 0
        self.primordial = True
        self.child = False
        self.conditionsMet = False
        self.parents = ()
        self.isMutation = False

        GeneGroup.__init__(self, *values, name=name,
                           maxGenes=maxGenes, maxGroups=maxGroups)

    def __repr__(self):
        return "\n<Specie: {} Genes({}) \nGroups({})\n\tFitness: {}>".format(self.name, self.genes, list(self.groups.values()), self.fitness)
    
    def __add__(self, other):
        '''
        Merge Species, add GeneGroup or Gene to Specie

        :param other: Specie to Merge, GeneGroup or Gene to add.
        '''
        selfCopy = self.deepcopy()
        if type(other) == Specie:
            selfCopy.genes += other.genes
            selfCopy.recessiveGenes.union(other.recessiveGenes)
            if len(other.groups):
                selfCopy.addMultipleGroups(list(other.groups.values()))

        else:
            return GeneGroup.__add__(self, other)

        return selfCopy

    def initChild(self, parents):
        self.fitness = NINF
        self.age = 0
        self.primordial = False
        self.child = True
        self.conditionsMet = False
        self.isMutation = False
        self.parents = parents

    def mutate(self, mutationChance, mutationType):
        if random.randint(0, 100) < mutationChance:
            self.isMutation = True
            self = mutationType(self)

    def calcFitness(self, calculationType, handler=None):
        if calculationType == FITNESS_GENE_BASED:
            if type(handler) not in (genes.Gene, genes.GeneGroup):
                handler = Gene(handler)
            self.fitness = self.genes.count(handler)
        elif calculationType == FITNESS_GROUP_BASED:
            self.fitness = 0
            for groupName, group in self.groups.items():
                if type(group) != GeneGroup:
                    print("Fail!")
                    print(self)
                    raise
                self.fitness += group.genes.count(handler.get(groupName, 0))
        else:
            raise AttributeError("calculationType is invalid")

    def createName(self, namesOptions):
        self.speciesName = "%s.%d" % (random.choice(namesOptions), random.randint(100000))
        return self.speciesName