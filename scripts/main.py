import add_objects, chasis
import bge


sceneObjects = bge.logic.getCurrentScene().objects

cam = sceneObjects['Camera']

adder = add_objects.Add(sceneObjects["Floor"])
chassiList = []

if not cam['init']:
    totalChassis = 10

    for chassiNumber in range(totalChassis):
        startingCoordenate
        
        recentChassi = chasis.Chasis(adder.inPosAndRot(
            "Master",
            [(chassiNumber*10),0,0],
            [0, 0, 0])
        )
        recentChassi = startingPoint
        chassiList.append({
            'object':recentChassi
            'fitness': recentChassi.fitness
        })
    cam['init'] = True

