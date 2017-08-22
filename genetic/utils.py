import copy

from numpy import random

from genetic import error_handling


def globalChoice(a, numberOfItemsToGet=1, allowRepeats=False):
    tmpValues = []
    lenA = len(a)
    if lenA == 0:
        raise error_handling.EmptyList("a can't be empty")

    if lenA == numberOfItemsToGet and allowRepeats == False:
        return a

    if numberOfItemsToGet > lenA and allowRepeats == False:
        raise AttributeError(
            "a length can't be smaller than numberOfItemsToGet when allowRepeats is false")

    while len(tmpValues) != numberOfItemsToGet:
        if lenA == 1 and allowRepeats:
            tmpValues.append(a[0])
        else:
            randomIndex = random.randint(0, len(a) - 1)
            if allowRepeats:
                tmpValues.append(a[randomIndex])
            else:
                if a[randomIndex] not in tmpValues:
                    tmpValues.append(a[randomIndex])

    return tmpValues


def splitList(a):
    half = int(len(a) / 2)
    return (a[:half], a[half:])


def joinDictLists(*dictList):
    newDict = {}
    for actualDict in dictList:
        for keyName, itemValue in actualDict.items():
            if not newDict.getGroup(keyName, False):
                newDict[keyName] = copy.copy(itemValue)
            else:
                if type(itemValue) == list:
                    for newValue in itemValue:
                        newDict[keyName].append(newValue)
                elif type(itemValue) == dict:
                    newDict[keyName] = joinDictLists(
                        newDict[keyName], itemValue)
                else:
                    newDict[keyName] = itemValue

    return newDict
