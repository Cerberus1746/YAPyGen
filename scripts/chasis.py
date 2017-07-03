import bge, bpy, random, mathutils
import numpy as np
import add_objects, genetic_object

#Better:[62.72278553864362, ['FastWheel', 'FastWheel', 'FastWheel', 'FastWheel'], {'child': True, 'age': 5, 'species': 'FasFasFasFas'}]
#Better:[62.72278553864362, ['FastWheel', 'FastWheel', 'FastWheel', 'FastWheel'], {'child': True, 'mutation': True, 'age': 5, 'species': 'FasFasFasFas'}]
#Better:[62.72278553864362, ['FastWheel', 'FastWheel', 'FastWheel', 'FastWheel'], {'species': 'FasFasFasFas', 'primordial': True, 'age': 5}]
#Better:[62.72278553864362, ['FastWheel', 'FastWheel', 'FastWheel', 'FastWheel'], {'species': 'FasFasFasFas', 'primordial': True, 'age': 5}]
#Better:[24.47828878089763, ['FastWheel', 'FastWheel', 'SlowWheel', 'ZeroWheel'], {'child': True, 'mutation': True, 'age': 5, 'species': 'FasFasSloZer'}]
class Chasis(bge.types.KX_GameObject, genetic_object.Specie):
	maximunSpeed = 0 
	startingCoordinate = [0,0,0]
	pieces = []
	characteristicsDict = {}
	
	def __init__(self, old_owner):
		self.piecesOptions = [ob.name for ob in bpy.context.scene.objects if ob.layers[1]]
		self.Add = add_objects.Add(self)

	def preBuild(self):
		self.pieces = []

		for slot in self.children:
			pieceToAdd = random.choice(self.piecesOptions)
			self.pieces.append(pieceToAdd)
			
		self.characteristicsDict = {
			"primordial" : True,
			"age": 0,
			"species" : "".join(sorted([str(x)[0:3] for x in self.pieces]))
		}

		self.build(self.pieces, self.characteristicsDict)
		
		

	def build(self, parts, characteristicsDict):
		self.pieces = parts
		self.characteristicsDict = characteristicsDict
		for n in range(len(self.children)):
			slot = self.children[n]
			try:
				part = self.pieces[n]
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
		self.maximunSpeed = max([
				self.maximunSpeed,
				#self.getLinearVelocity().magnitude - abs(self.worldPosition.x)
				#self.worldPosition.y - abs(self.worldPosition.x),
				abs(self.worldPosition.x) * abs(self.worldPosition.z),
			])
		'''if False in self.pieces:
			self.maximunSpeed = self.maximunSpeed / self.pieces.count(False)'''
		return self.maximunSpeed

	def fitness(self):
		return self.maximunSpeed