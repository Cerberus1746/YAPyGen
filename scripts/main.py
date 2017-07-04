import add_objects, chasis, genetic
import bge

class Main():
	timePerSimulation = 3
	simulationsToMake = 5
	maxCycle = 50
	timeScale = 5
	startingPoint = [0,0,0.5]

	actualCycle = 0
	simulationCycle = 0

	vehicles = []

	def __init__(self):
		bge.logic.setTimeScale(self.timeScale)
		self.maxSpecieAge = 5
		self.genetics = genetic.Genetic()
		genetic.Genetic.__init__(self)

	def refreshScene(self):
		self.scene = bge.logic.getCurrentScene()
		self.sceneObjects = self.scene.objects
		self.cam = self.sceneObjects['Camera']
		self.adder = add_objects.Add(self.sceneObjects["Floor"])
		
		chassisAdded = self.adder.inPosAndRot("Master", self.startingPoint,	[0, 0, 0])
		
		if self.simulationCycle == 0:
			newVehicle = chasis.Chasis(chassisAdded)
			newVehicle.preBuild()
		else:
			newVehicle = chasis.Chasis(chassisAdded, self.genetics.allPopulation[self.actualCycle])

		newVehicle.startingCoordinate = self.startingPoint
		newVehicle.build()

		self.currentVehicle = newVehicle

	def perTick(self):
		self.currentVehicle.recordFitness()
		if self.cam['time'] >= self.timePerSimulation:
			self.cam['time'] = 0.0
			bge.logic.globalDict['refresh'] = True

			self.currentVehicle.recordFitness()
			
			if self.simulationCycle == 0:
				self.genetics.allPopulation.append(self.currentVehicle.geneticObject)
			
			self.actualCycle += 1
			
			if self.actualCycle < self.simulationsToMake:
				self.sceneRestart()
			else:
				self.simulationEnd()

	def sceneRestart(self):
		self.scene.restart()

	def simulationEnd(self):
		self.actualCycle = 0
		
		print("\n" + "#" * 10 + " Cycle Number: " + str(self.simulationCycle) + " " + "#" * 10)
				
		[print(x) for x in self.genetics.allPopulation]
		
		self.genetics.createPopulation()
		
		print("\n" + "#" * 5 + " After Filter: " + "#" * 5)
		
		[print(x) for x in self.genetics.allPopulation]
		
		print("Better: " + str(self.genetics.better))
		
		self.simulationsToMake = len(self.genetics.allPopulation)
		
		if self.genetics.better.age >= self.maxSpecieAge:
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