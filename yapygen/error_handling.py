'''Module containing all custom exceptions'''


class Genes(Exception):
    '''Raised when a exception with genes happen'''
    pass


class Species(Exception):
    '''Raised when a exception with Species happen'''
    pass


class NoFitnessValue(Species):
    '''Raised by a filter when it founds a specie with no fitness value'''
    pass


class NoPopulation(Exception):
    '''Raised when the population is empt'''
    pass


class EmptyList(Exception):
    '''Raised when a iterator with contents is needed but nothing is found'''
    pass
