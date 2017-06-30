import bge, bpy, random, mathutils
import numpy as np
import add_objects

class Chasis(bge.types.KX_GameObject):
	fitness = 0
	maximunSpeed = 0 
	startingCoordinate = [0,0,0]
	pieces = []
	
	def __init__(self, old_owner):
		self.piecesOptions = [ob.name for ob in bpy.context.scene.objects if ob.layers[1]]
		self.piecesOptions.append(False)
		
		self.Add = add_objects.Add(self)

	def preBuild(self):
		self.pieces = []
		for slot in self.children:
			pieceToAdd = random.choice(self.piecesOptions)
			self.pieces.append(pieceToAdd)

	def build(self, parts):
		self.pieces = parts
		for n in range(len(parts)):
			slot = self.children[n]
			part = self.pieces[n]
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
		self.maximunSpeed = max([
				self.maximunSpeed,
				#self.getLinearVelocity().magnitude,
				#self.worldPosition.y - abs(self.worldPosition.x),
				self.worldPosition.z - abs(self.worldPosition.x),
				#abs(self.worldPosition.x)
			])
		'''if False in self.pieces:
			self.maximunSpeed = self.maximunSpeed / self.pieces.count(False)'''
		return self.maximunSpeed

	def fitness(self):
		return self.maximunSpeed