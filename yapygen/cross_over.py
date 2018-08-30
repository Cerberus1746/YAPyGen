'''module containing all cross over functions'''
from yapygen.genes.specie import Specie
from numpy.random import randint

def random_shuffle(mother, father, groups=False):
    '''add parents genes into one another, randomize their orders and exclude the
    excess genes automatically'''
    assert type(mother) == Specie, "mother needs to be of type Specie"
    assert type(father) == Specie, "father needs to be of type Specie"
    if groups:
        newSpecie = father.deepcopy() if randint(0, 1) else mother.deepcopy()
        
        for group in groups:
            newGroup = mother[group] + father[group]
            newGroup.shuffle_genes()
            newGroup.randomize_genes(keepGroups=True, recursiveRandom=True)
            newSpecie[group] = newGroup

        return newSpecie
            
    else:
        child = mother + father

        child.shuffle_genes()

        child.randomize_genes(keepGroups=True, recursiveRandom=True)

        return child

def mean(mother, father, groups):
    '''set the medium '''
    assert type(mother) == Specie, "mother needs to be of type Specie"
    assert type(father) == Specie, "father needs to be of type Specie"
    
    newSpecie = father.deepcopy() if randint(0, 1) else mother.deepcopy()

    for group in groups:
        new_values = []
        father_group = father[group]
        mother_group = mother[group]

        if len(mother[group]) < len(father[group]):
            minParent = mother
        else:
            minParent = father
        for i in range(len(minParent[group])):
            print("Father: " + str(father_group.genes[i].value))
            print("Mother: " + str(mother_group.genes[i].value))
            print("Medium: " + str((father_group.genes[i].value + mother_group.genes[i].value) / 2))
            print("\n")
            new_values.append((father_group.genes[i].value + mother_group.genes[i].value) / 2)

        newSpecie[group].genes = new_values
        

    return newSpecie