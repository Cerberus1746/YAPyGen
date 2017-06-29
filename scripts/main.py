import add_objects, chasis
import bge

class Main():
	vehicles = []
	def __init__(self):
		bge.logic.setTimeScale(10)
		self.startingPoint = [0,0,0.5]

	def refreshScene(self):
		self.scene = bge.logic.getCurrentScene()
		self.sceneObjects = self.scene.objects
		self.cam = self.sceneObjects['Camera']
		self.adder = add_objects.Add(self.sceneObjects["Floor"])
		
		recentChassi = chasis.Chasis(self.adder.inPosAndRot(
			"Master",
			self.startingPoint,
			[0, 0, 0])
		)
		
		
		recentChassi.startingCoordinate = self.startingPoint
		recentChassi.build(recentChassi.pieces)

		self.currentVehicle = recentChassi

	def perTick(self):
		if self.cam['time'] >= 3:
			self.currentVehicle.recordFitness()
			self.vehicles.append(self.currentVehicle)
			
			if len(self.vehicles) <= 3:
				self.sceneRestart()
			else:
				self.simulationEnd()

	def sceneRestart(self):
		bge.logic.globalDict['refresh'] = True
		self.scene.restart()
	
	def simulationEnd(self):
		for vehicle in self.vehicles:
			print(vehicle.fitness())
		self.scene.end()

if (bge.logic.globalDict.get("refresh", False) and
		bge.logic.globalDict.get('main', False)):
	bge.logic.globalDict['main'].refreshScene()
	bge.logic.globalDict['refresh'] = False

if not bge.logic.globalDict.get("main", False):
	bge.logic.globalDict['main'] =  Main()
	bge.logic.globalDict['main'].refreshScene()
else:
	bge.logic.globalDict['main'].perTick()