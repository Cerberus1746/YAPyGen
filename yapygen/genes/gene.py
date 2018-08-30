from yapygen.genes import gene_group

class Gene(object):
    '''Basic object for the yapygen processing.'''
    
    recessive = False
    groups = []

    value = 0

    def __init__(self, value):
        '''Create a new gene

        :param value: Value to be used.
        '''
        self.value = value

    def __add__(self, other):
        if isinstance(other, type(self)):
            return gene_group.GeneGroup(self, other)

        else:
            return other + self

    def __eq__(self, other):
        if isinstance(self, type(other)):
            return self.__hash__() == other.__hash__()

        else:
            return NotImplemented

    def __hash__(self):
        if isinstance(self.value, list):
            return hash(tuple(self.value))
        else:
            return hash(self.value)

    def __repr__(self):
        return "\n\tGene(%s)" % str(self.value)