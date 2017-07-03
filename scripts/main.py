import add_objects, chasis, genetic
import bge

#Better:[3561.5621985477046, ['FastWheel', 'FastWheel', 'FastWheel', 'ZeroWheel'], {'child': True, 'mutation': True, 'age': 5, 'species': 'FasFasFasZer'}]
#Better:[6369.298383083718, ['FastWheel', 'FastWheel', 'SlowWheel', 'ZeroWheel'], {'child': True, 'mutation': True, 'age': 5, 'species': 'FasFasSloZer'}]

class Main(genetic.Genetic):
	timePerSimulation = 3
	simulationsToMake = 10
	maxCycle = 15
	timeScale = 5
	startingPoint = [0,0,0.5]

	vehicleNumber = 0
	simulationCycle = 0

	vehicles = []

	def __init__(self):
		bge.logic.setTimeScale(self.timeScale)
		self.maxSpecieAge = 5

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
			
			print("Vehicle Created:\n" + str(recentChassi.pieces))
			print(recentChassi.characteristicsDict)
		else:
			recentChassi.build(
				self.allPopulation[self.vehicleNumber][1],
				self.allPopulation[self.vehicleNumber][2]
			)
			
			print("Using Vehicle:\n" + 	str(self.allPopulation[self.vehicleNumber][1]))
			print(str(self.allPopulation[self.vehicleNumber][2]))

		self.currentVehicle = recentChassi

	def perTick(self):
		self.currentVehicle.recordFitness()
		if self.cam['time'] >= self.timePerSimulation:
			self.cam['time'] = 0.0

			bge.logic.globalDict['refresh'] = True
			
			self.currentVehicle.recordFitness()
			self.vehicles.append(self.currentVehicle)
			print(self.currentVehicle.fitness())
			
			self.vehicleNumber += 1
			
			if self.vehicleNumber < self.simulationsToMake:
				self.sceneRestart()
			else:
				self.simulationEnd()

	def sceneRestart(self):
		self.scene.restart()

	def simulationEnd(self):
		self.vehicleNumber = 0
		self.vehiclesStats = []

		for vehicle in self.vehicles:
			self.vehiclesStats.append([
				vehicle.fitness(),
				vehicle.pieces,
				vehicle.characteristicsDict
			])

		self.allPopulation = sorted(
			self.vehiclesStats,
			reverse=True,
			key=lambda vehicle: vehicle[0]
		)
		print("\n\nPre Filter:\n" + str(self.allPopulation))
		
		self.createPopulation()
		
		self.simulationsToMake = len(self.allPopulation)
		
		self.vehicles = []
		print("\nAfter Filter:" + str(self.allPopulation))
		
		print("\nBetter:" + str(self.better))
		
		if self.better[2]["age"] >= self.maxSpecieAge:
			self.scene.end()
		
		
		self.simulationCycle += 1

		if self.simulationCycle < self.maxCycle:
			self.scene.restart()
		else:
			self.simulationCycle = 0
			self.scene.end()

if (bge.logic.globalDict.get("refresh", False) and
		bge.logic.globalDict.get('main', False)):
	bge.logic.globalDict['main'].refreshScene()
	bge.logic.globalDict['refresh'] = False

elif not bge.logic.globalDict.get("main", False):
	bge.logic.globalDict['main'] =  Main()
	bge.logic.globalDict['main'].refreshScene()

else:
	bge.logic.globalDict['main'].perTick()