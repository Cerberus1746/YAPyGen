import chasis, bge, math, mathutils


W = 119
A = 97
S = 115
D = 100

try:
	chasisObj = chasis.bge.logic.getCurrentController().owner
	if chasisObj.get('init', False):
		keyboard = chasisObj.sensors['Keyboard']

		newEvents = [x[0] for x in keyboard.events]

		for wheel in chasisObj.wheels:
			if W in newEvents:
				wheel.applyTorque([0, 0, -10], True)
			elif S in newEvents:
				wheel.applyTorque([0, 0, 10], True)
			elif A in newEvents:
				if wheel["right"]:
					wheel.applyTorque([0, 0, -10], True)
				elif wheel["left"]:
					wheel.applyTorque([0, 0, 10], True)
			elif D in newEvents:
				if wheel["right"]:
					wheel.applyTorque([0, 0, 10], True)
				elif wheel["left"]:
					wheel.applyTorque([0, 0, -10], True)

		if newEvents != chasisObj.lastEvents:
			print(newEvents)
			chasisObj.lastEvents = newEvents
	else:
		chasisObj = chasis.Chasis(chasisObj)
		chasisObj.preBuild()
		chasisObj.build()

		chasisObj.lastEvents = []
		chasisObj["init"] = True
except:
	bge.logic.getCurrentScene().end()
	raise
