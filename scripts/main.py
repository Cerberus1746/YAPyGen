import add_objects, chasis
import bge

class Main():
	vehicles = []
	def __init__(self):
		bge.logic.setTimeScale(10)

	def refreshScene(self):
		self.scene = bge.logic.getCurrentScene()
		self.sceneObjects = self.scene.objects
		self.cam = self.sceneObjects['Camera']
		self.adder = add_objects.Add(self.sceneObjects["Floor"])
		
		startingPoint = [0,0,0.5]
		recentChassi = chasis.Chasis(self.adder.inPosAndRot(
			"Master",
			startingPoint,
			[0, 0, 0])
		)
		recentChassi.startingCoordinate = startingPoint

		self.currentVehicle = recentChassi

		self.cam['init'] = True

	def perTick(self):
		if self.cam['time'] >= 3:
			self.currentVehicle.recordFitness()
			self.vehicles.append(self.currentVehicle)
			
			if len(self.vehicles) <= 3:
				bge.logic.globalDict['refresh'] = True
				self.scene.restart()
			else:
				for vehicle in self.vehicles:
					print(vehicle.fitness())
				self.scene.end()

if not bge.logic.globalDict.get("main", False):
	bge.logic.globalDict['main'] =  Main()
	bge.logic.globalDict['refresh'] = True
else:
	bge.logic.globalDict['main'].perTick()

if (bge.logic.globalDict.get("refresh", False) and
		bge.logic.globalDict.get('main', False)):
	bge.logic.globalDict['main'].refreshScene()
	bge.logic.globalDict['refresh'] = False