import bge, bpy, random, math
import add_objects

class Chasis(bge.types.KX_GameObject):
    fitness = 0
    
	def __init__(self, old_owner):
		self.piecesOptions = [ob.name for ob in bpy.context.scene.objects if ob.layers[1]]
		self.piecesOptions.append(False)
		
		self.Add = add_objects.Add(self)
		
		for slot in self.children:
			pieceToAdd = random.choice(self.piecesOptions)
			if pieceToAdd:
				lastPiece = self.Add.inPosAndRot(pieceToAdd, slot.worldPosition, [0, 90, 0])

				lastPiecePhysics = lastPiece.getPhysicsId()

				DOF = bge.constraints.createConstraint(
					lastPiecePhysics,
					self.getPhysicsId(),
					bge.constraints.GENERIC_6DOF_CONSTRAINT,
					flag = 128
				)
				DOF.setParam(3, 0.0, 0.0)
				DOF.setParam(4, 0.0, 0.0)

	def fitness(self):
        