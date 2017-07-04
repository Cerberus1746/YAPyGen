import bge, bpy, random, mathutils
import numpy as np
import add_objects, genetic_object

class Chasis(bge.types.KX_GameObject):
	startingCoordinate = [0,0,0]
	geneticObject = None
	
	def __init__(self, _, useOldObject = False):
		self.Add = add_objects.Add(self)
		
		if useOldObject:
			self.geneticObject = useOldObject
		else:
			self.geneticObject = genetic_object.Specie()
			self.piecesOptions = [ob.name for ob in bpy.context.scene.objects if ob.layers[1]]
	
	def __str__(self):
		return str(self.__dict__)

	def preBuild(self):
		self.geneticObject.chromosomes = []
		for _ in self.children:
			pieceToAdd = random.choice(self.piecesOptions)
			self.geneticObject.chromosomes.append(pieceToAdd)

		self.geneticObject.primordial = True
		self.geneticObject.age = 0
		self.geneticObject.createName()

	def build(self):
		for n in range(len(self.children)):
			slot = self.children[n]
			try:
				part = self.geneticObject.chromosomes[n]
			except IndexError:
				part = False
			if part:
				lastPiece = self.Add.inPosAndRot(part, slot.worldPosition, [0, 90, 0])

				lastPiecePhysics = lastPiece.getPhysicsId()

				#create 6 Degress of Freedom Constraint
				DOF = bge.constraints.createConstraint(
					lastPiecePhysics,
					self.getPhysicsId(),
					bge.constraints.GENERIC_6DOF_CONSTRAINT,
					flag = 128
				)
				DOF.setParam(3, 0.0, 0.0) #Lock rotation in X axis
				DOF.setParam(4, 0.0, 0.0) #Lock rotation in Y axis
				#To lock axis Z if necessary: DOF.setParam(4, 0.0, 0.0)
				
	def recordFitness(self):
		self.geneticObject.fitness = max([
				self.geneticObject.fitness,
				#self.getLinearVelocity().magnitude - abs(self.worldPosition.x)
				#self.worldPosition.y - abs(self.worldPosition.x),
				abs(self.worldPosition.z),
			])

		return self.geneticObject.fitness