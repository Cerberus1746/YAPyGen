import bge
import bpy
import mathutils

import add_objects
from genetic.specie import Specie
import numpy as np


W = 119
A = 97
S = 115
D = 100


class Chasis(bge.types.KX_GameObject):
    startingCoordinate = [0, 0, 0]
    geneticObject = None
    multiplier = -1
    wheels = np.empty(0)
    init = False
    parts = np.empty(0)
    target = None

    actualAction = 0

    maximunSimulationTime = 0
    rawFitness = 0
    numberOfTicks = 0

    commandsOptions = [
        [W, W],
        [A, A],
        [S, S],
        [D, D],

        [W, D],
        [W, A],
        [S, D],
        [S, A]
    ]
    # commandsOptions = [W]

    currentTime = 0
    currentInstruction = 0

    namesOptions = ["buffalo", "dog", "cat", "merkat",
                    "dolphin", "croc", "alpaca", "raven"]

    def __init__(self, _, useOldObject=False):
        self.Add = add_objects.Add(self)
        self.collisionCallbacks.append(self.on_collision_one)
        self.piecesOptions = [
            ob.name for ob in bpy.context.scene.objects if ob.layers[1]]

        if useOldObject:
            self.geneticObject = useOldObject
        else:
            self.geneticObject = Specie()

    def __str__(self):
        return str(self.__dict__)

    def preBuild(self):
        self.geneticObject.chromosomes = np.empty((0, 2))

        self.geneticObject.primordial = True
        self.geneticObject.age = 0
        self.geneticObject.createName(self.namesOptions)

    def build(self):
        for _ in self.children:
            pieceToAdd = np.random.choice(self.piecesOptions)
            self.parts = np.append(self.parts, pieceToAdd)

        for n in range(len(self.children)):
            slot = self.children[n]
            part = self.parts[n]
            if part:
                lastPiece = self.Add.inPosAndRot(
                    part, slot.worldPosition, [0, 90, 0])
                lastPiece["steering"] = slot.get("steering", False)
                lastPiece["torque"] = slot.get("torque", False)
                lastPiece["right"] = slot.get("right", False)
                lastPiece["left"] = slot.get("left", False)

                lastPiecePhysics = lastPiece.getPhysicsId()

                # create 6 Degress of Freedom Constraint
                DOF = bge.constraints.createConstraint(
                    lastPiecePhysics,
                    self.getPhysicsId(),
                    bge.constraints.GENERIC_6DOF_CONSTRAINT,
                    flag=128
                )
                DOF.setParam(3, 0.0, 0.0)  # Lock rotation in X axis
                DOF.setParam(4, 0.0, 0.0)  # Lock rotation in Y axis
                # To lock axis Z if necessary: DOF.setParam(4, 0.0, 0.0)

                self.wheels = np.append(self.wheels, lastPiece)

    def on_collision_one(self, colObject):
        if not self.geneticObject.conditionsMet and colObject.get("target", False):
            self.geneticObject.conditionsMet = True
            self.multiplier = 2

        if colObject.get("floor", False):
            self.multiplier += -10

    def update(self):
        if self.init:
            if self.numberOfTicks % 10 == 0:
                self.actualAction += 1

                if self.geneticObject.primordial:
                    self.currentInstruction = np.random.randint(
                        len(self.commandsOptions) - 1)
                    self.currentInstruction = self.commandsOptions[self.currentInstruction]
                    self.geneticObject.chromosomes = np.vstack(
                        (self.geneticObject.chromosomes, self.currentInstruction))
                else:
                    self.currentInstruction = self.geneticObject.chromosomes[self.currentTime]

        self.numberOfTicks += 1

        for wheel in self.wheels:
            if W in self.currentInstruction:
                wheel.applyTorque([0, 0, -10], True)
            elif S in self.currentInstruction:
                wheel.applyTorque([0, 0, 10], True)
            if D in self.currentInstruction:
                if wheel["right"]:
                    wheel.applyTorque([0, 0, -10], True)
                elif wheel["left"]:
                    wheel.applyTorque([0, 0, 10], True)
            elif A in self.currentInstruction:
                if wheel["right"]:
                    wheel.applyTorque([0, 0, 10], True)
                elif wheel["left"]:
                    wheel.applyTorque([0, 0, -10], True)

        '''self.rawFitness += (-1 * (self.worldPosition - self.target.worldPosition).length)
        + (self.worldPosition - mathutils.Vector(self.startingCoordinate)).length
        self.geneticObject.fitness = self.rawFitness / self.numberOfTicks'''

        self.geneticObject.fitness = max([
            self.geneticObject.fitness,
            self.multiplier * (self.worldPosition -
                               mathutils.Vector(self.startingCoordinate)).length
        ])
