import math
import mathutils


class Add():
    def __init__(self, mainObj):
        self.mainObj = mainObj
        self.adder = self.mainObj.scene.addObject

    def inPos(self, obj, pos, dur=0):
        crObj = self.adder(obj, self.mainObj, dur)
        crObj.worldPosition = pos
        return crObj

    def inPosAndRot(self, obj, pos, rot, dur=0, local=False):
        crObj = self.adder(obj, self.mainObj, dur)
        rot = [math.radians(angle) for angle in rot]
        if not local:
            crObj.worldPosition = pos
            crObj.worldOrientation.rotate(mathutils.Euler(rot))
        return crObj
