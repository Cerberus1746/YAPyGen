"""Module used to hold all Gene related objects"""
from numpy import random, NINF

from yapygen.genes import gene_group


class Specie(gene_group.GeneGroup):
    def __init__(self, *values, name="", maxGenes=False, maxGroups=False):
        self.fitness = NINF
        self.age = 0
        self.primordial = True
        self.child = False
        self.conditionsMet = False
        self.parents = ()
        self.isMutation = False

        gene_group.GeneGroup.__init__(
            self, *values, name=name, maxGenes=maxGenes, maxGroups=maxGroups
        )

    def __repr__(self):
        return "<Specie: {} Genes({})\nGroups({})\nFitness: {}>".format(
            self.name, self.genes, list(self.groups), self.fitness
        )

    def __add__(self, other):
        """
        Merge Species, add GeneGroup or Gene to Specie

        :param other: Specie to Merge, GeneGroup or Gene to add.
        """
        selfCopy = self.deepcopy()
        if isinstance(other, Specie):
            selfCopy.genes += other.genes
            selfCopy.recessiveGenes.union(other.recessiveGenes)
            if len(other.groups):
                selfCopy.add_multiple_groups(list(other.groups.values()))

        else:
            return gene_group.GeneGroup.__add__(self, other)

        return selfCopy

    def init_child(self, parents):
        self.fitness = NINF
        self.age = 0
        self.primordial = False
        self.child = True
        self.conditionsMet = False
        self.isMutation = False
        self.parents = parents

    def mutate(self, mutationChance, mutationType):
        if random.randint(0, 100) <= mutationChance:
            self.isMutation = True
            self = mutationType(self)

        return self

    def calc_fitness(self, calculationType, handler=None):
        calculationType(self, handler)

    def create_name(self, namesOptions):
        self.name = "%s.%d" % (random.choice(namesOptions), random.randint(100000))
        return self.name
