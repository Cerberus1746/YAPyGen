import add_objects, chasis
import bge

if not bge.logic.globalDict.get("globalInit", False):
	bge.logic.globalDict['globalInit'] =  True
	bge.logic.globalDict['vehicles'] = []
	bge.logic.setTimeScale(10)

scene = bge.logic.getCurrentScene()
sceneObjects = scene.objects
cam = sceneObjects['Camera']
adder = add_objects.Add(sceneObjects["Floor"])

if not cam['init']:
	startingPoint = [0,0,0.5]
	recentChassi = chasis.Chasis(adder.inPosAndRot(
		"Master",
		startingPoint,
		[0, 0, 0])
	)
	recentChassi.startingCoordinate = startingPoint

	bge.logic.globalDict['currentVehicle'] = recentChassi

	cam['init'] = True

if cam['time'] >= 3:
	bge.logic.globalDict['currentVehicle'].recordFitness()
	bge.logic.globalDict['vehicles'].append(bge.logic.globalDict['currentVehicle'])
	
	if len(bge.logic.globalDict['vehicles']) <= 3:
		scene.restart()
	else:
		for vehicle in bge.logic.globalDict['vehicles']:
			print(vehicle.fitness())
		scene.end()