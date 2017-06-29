import add_objects, chasis
import bge

class Main():
	timePerSimulation = 3
	simulationsToMake = 1
	maxCycle = 2
	startingPoint = [0,0,0.5]

	vehicleNumber = 0
	simulationCycle = 0
	
	vehicles = []
	vehiclesStats = []
	
	def __init__(self):
		bge.logic.setTimeScale(5)

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
		
		
		if self.simulationCycle == 0:
			recentChassi.preBuild()
			recentChassi.build(recentChassi.pieces)
			
			print("Vehicle Created:\n" + str(recentChassi.pieces))
		elif self.simulationCycle > 0:
			recentChassi.build(self.vehiclesStats[self.vehicleNumber][1])
			
			print("Using Vehicle:\n" + str(self.vehiclesStats[self.vehicleNumber][1]))
		else:
			print("Shouldn't be shown")

		self.currentVehicle = recentChassi

	def perTick(self):
		if self.cam['time'] >= self.timePerSimulation:
			self.cam['time'] = 0.0

			bge.logic.globalDict['refresh'] = True
			
			self.currentVehicle.recordFitness()
			self.vehicles.append(self.currentVehicle)
			
			if self.vehicleNumber == self.simulationsToMake:
				self.simulationEnd()
			elif self.vehicleNumber < self.simulationsToMake:
				self.sceneRestart()
			else:
				print("Shouldn't be shown")

	def sceneRestart(self):
		self.vehicleNumber += 1
		self.scene.restart()

	def simulationEnd(self):
		self.vehicleNumber = 0

		self.vehiclesStats = []

		for vehicle in self.vehicles:
			self.vehiclesStats.append([
				vehicle.fitness(),
				vehicle.pieces
			])

		self.vehiclesStats = sorted(
			self.vehiclesStats,
			reverse=True,
			key=lambda vehicle: vehicle[0]
		)
		
		self.vehicles = []
		print("\n\nSimulation Cycle End:\n" + str(self.vehiclesStats))

		if self.simulationCycle == self.maxCycle:
			self.simulationCycle = 0
			self.scene.end()
		elif self.simulationCycle < self.maxCycle:
			self.scene.restart()
		else:
			print("Shouldn't be shown")
		
		self.simulationCycle += 1

if (bge.logic.globalDict.get("refresh", False) and
		bge.logic.globalDict.get('main', False)):
	bge.logic.globalDict['main'].refreshScene()
	bge.logic.globalDict['refresh'] = False

elif not bge.logic.globalDict.get("main", False):
	bge.logic.globalDict['main'] =  Main()
	bge.logic.globalDict['main'].refreshScene()

else:
	bge.logic.globalDict['main'].perTick()