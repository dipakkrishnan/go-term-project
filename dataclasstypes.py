import random 
import copy
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt

def manhattan(one,two): #records manhattan distance blocks between driver and passenger
	rows = abs(one[0]-two[0])
	cols = abs(one[1]-two[1])
	return rows+cols

def distance(passenger, driver): # finds the distance between driver and pas
	return (str(driver.id), manhattan(passenger.location,driver.driverLocation),passenger.id)

def distance1(driver, passenger): # finds the distance between pas and driver
	return (str(passenger.id), manhattan(passenger.location,driver.driverLocation),driver.id)

def index(drIndex,passPrior): # finds the specific driver index
	for i in range(len(passPrior)):
		if drIndex==passPrior[i][0]: return (drIndex,passPrior[i][1],passPrior[i][2])

def values(one, two): # helper to compare the indexed values
	return one[1] <= two[1]
	
def swap(a, i, j): #swaps values needed for driver and pas indexes
	(a[i], a[j]) = (a[j], a[i])
	
def switch(l):
	alltrue = False
	while not alltrue:
		alltrue = True
		for i in range(len(l)-1):
			if not values(l[i],l[i+1]):
				alltrue = False
				swap(l, i, i+1)
	return l

def optimalMatch(driverPref,passPref,taken_dr,taken_pass,drIn,paIn):
	# this takes in the preference lists and taken lists and returns true 
	# if the proposed pairing is optimal
	for i in driverPref:
		if i[0] not in taken_pass:
			if i[0]!=str(paIn): return False
			else: continue
	for i in passPref:
		if i[0] not in taken_dr:
			if i[0]!=str(drIn): return False
			else: continue
	return True

def closestDriver(pas, drivers,taken): #finds the closest driver to a passenger
	driver = 0
	val = manhattan(pas.location,drivers[0].driverLocation)
	for i in range(1,len(drivers)):
		current = manhattan(pas.location,drivers[i].driverLocation)
		if current < val:
			val = current
			driver = i
	chosen = drivers.pop(driver)
	chosen.occupant = pas
	chosen.passengerLocation = pas.location
	chosen.passengerDestination = pas.destination
	taken.append(chosen)
	return chosen

def moveTo(driver): #moves driver to passenger, one unit at a time
	if driver.driverLocation[0] < driver.passengerLocation[0]:
		driver.driverLocation = (driver.driverLocation[0]+1,driver.driverLocation[1])
		driver.pos=3
	elif driver.driverLocation[0] > driver.passengerLocation[0]: 
		driver.driverLocation = (driver.driverLocation[0]-1,driver.driverLocation[1])
		driver.pos=0
	elif driver.driverLocation[1] < driver.passengerLocation[1]:
		driver.driverLocation = (driver.driverLocation[0],driver.driverLocation[1]+1)
		driver.pos=2
	elif driver.driverLocation[1] > driver.passengerLocation[1]:
		driver.driverLocation = (driver.driverLocation[0],driver.driverLocation[1]-1)
		driver.pos=1

def destinationMove(driver,passenger,pos): #moves driver w/ passenger to
	# destination, one unit at a time
	if driver.driverLocation[0] < driver.passengerDestination[0]:
		driver.driverLocation=(driver.driverLocation[0]+1,driver.driverLocation[1])
		pos=2
	elif driver.driverLocation[0] > driver.passengerDestination[0]: 
		driver.driverLocation = (driver.driverLocation[0]-1,driver.driverLocation[1])
		pos=1
	elif driver.driverLocation[1] < driver.passengerDestination[1]:
		driver.driverLocation = (driver.driverLocation[0],driver.driverLocation[1]+1)
		pos=3
	elif driver.driverLocation[1] > driver.passengerDestination[1]:
		driver.driverLocation = (driver.driverLocation[0],driver.driverLocation[1]-1)
		pos=0

def destinationPassenger(passenger,driver): #moves driver w/ passenger to destination from pas location
	if passenger.location[0] < passenger.destination[0]:
		passenger.location = (passenger.location[0]+1,passenger.location[1])
		driver.pos=3
	elif passenger.location[0] > passenger.destination[0]: 
		passenger.location = (passenger.location[0]-1,passenger.location[1])
		driver.pos=0
	elif passenger.location[1] < passenger.destination[1]:
		passenger.location = (passenger.location[0], passenger.location[1]+1)
		driver.pos=2
	elif passenger.location[1] > passenger.destination[1]:
		passenger.location = (passenger.location[0], passenger.location[1]-1)
		driver.pos=1


def moveAssignedDriver(self, drivers, taken): 
	# moves assigned driver back to available driver list once it has dropped off customer 
	for i in taken:
		if taken[i].driver.driverLocation == driver.passengerDestination:
			driver = taken.pop(i)
			drivers.append(driver)

class Passenger(object):
	def __init__(self, idvalue):
		self.rowLocation = random.randint(0,14)
		self.colLocation = random.randint(0,14)
		self.destinationRow = random.randint(0,14)
		self.destinationCol = random.randint(0,14)
		self.location = (self.rowLocation, self.colLocation)
		self.destination = (self.destinationRow, self.destinationCol)
		self.id = idvalue
		self.assignTime = 0
		self.pickUpTime = 0
		self.dropOffTime = 0
		self.timePas = 0
		self.timeDes = 0
		self.globalTime = 0
		self.timerDelay = 100

	def timerFiredDropOff(self,driver): # this sets the timer for the 
	# drop off the passenger after the trip
		self.globalTime += self.timerDelay
		if self.globalTime % 1000 == 0:
			self.timeDes += 1
			destinationPassenger(self,driver)

class Match(object): # Matches the driver to closest passenger 
	def __init__(self,passNum,driveNum): #driver list, passenger list
		passengerList = []
		driverList = []
		self.takenPairs=[]
		for i in range(driveNum): driverList.append(Driver(i))
		for j in range(passNum): passengerList.append(Passenger(j))
		self.driverList = driverList
		self.passengerList = passengerList
		self.time = 0
		self.globalTime = 0
		self.timerDelay = 100

	def timerFiredPickUp(self): # sets the timer Fired for the pick up move
		self.globalTime += self.timerDelay
		if self.globalTime % 1000 == 0:
			self.time += 1
			self.timePas += 1
			moveTo(self)

	def timerFiredDropOff(self): # sets the timer Fired for the drop Off move
		self.globalTime += self.timerDelay
		if self.globalTime % 1000 == 0:
			self.time += 1
			self.timeDes += 1
			destinationMove(self,self.occupant)


	def totalTime(self): # compiles the total time
		return self.timeDes + self.timePas

	def availableDriverListUpdate(self): # calls the move driver function
		return moveAssignedDriver(self, drivers, taken)

	def priority(self): # multiple drivers, passengers, stable matching
	# this sets a priority ranking of sorts for the passengers and drivers based
	# on id
		passengerPriority = {}
		for i in range(len(self.passengerList)):
			passengerPriority[str(self.passengerList[i].id)] = []
			for j in range(len(self.driverList)):
				passengerPriority[str(self.passengerList[i].id)].append(distance(self.passengerList[i],self.driverList[j]))
		for row in passengerPriority:
			passengerPriority[row] = switch(passengerPriority[row])
		driverPriority = {}
		for i in range(len(self.driverList)):
			driverPriority[str(self.driverList[i].id)] = []
			for j in range(len(self.passengerList)):
				driverPriority[str(self.driverList[i].id)].append(distance1(self.driverList[i],self.passengerList[j]))
		for row in driverPriority:
			driverPriority[row] = switch(driverPriority[row])
		return (passengerPriority,driverPriority)

	def stableMatch(self, driverPriority,passengerPriority):
		# this is a key function, which matches each driver to a passenger 
		# optimally
		indexes = []
		available = []
		takenPas = []
		takenDr = []
		taken = []
		if len(self.driverList) == 1 and len(self.passengerList) == 1:
			return ('0', '0')
		for i in range(len(driverPriority)): 
			indexes.append(0)
			available.append(str(i))
		while len(taken) != min(len(driverPriority),len(passengerPriority)):
			pairing = []
			store = []
			for i in available: # loop through available drivers 
				pasChoice = driverPriority[str(i)][indexes[int(i)]]
				notFound = False
				while not notFound:
					if pasChoice not in takenPas: notFound = True
					else:
						indexes[int(i)] += 1
						pasChoice = driverPriority[str(i)][indexes[int(i)]]
				choice = index(str(i),passengerPriority[pasChoice[0]])
				driveP = driverPriority[str(i)]
				passP = passengerPriority[str(choice[2])]
				opt = optimalMatch(driveP,passP,takenDr,takenPas,str(i),str(choice[2]))
				if opt:
					takenPas.append(str(choice[2]))
					takenDr.append(str(i))
					taken.append(tuple([str(i),str(choice[2])]))
					available.remove(str(i))
				pairing.append(choice) #append the stable choice of drivers 
				# and passengers
			lst = []
			for i in pairing:
				lst.append(i[2])
			if min(len(passengerPriority),len(driverPriority))==len(set(lst)): 
				if len(lst) != len(set(lst)):
					numbers = []
					for i in pairing: numbers.append(i[2])
					dup = {}
					for i in range(len(set(lst))): dup[str(i)] = []
					for i in range(len(numbers)): dup[str(numbers[i])].append(i)
					same = []
					for i in dup: same.append(dup[i])
					change = []
					for i in range(len(same)):
						if len(same[i]) != 1: 
							assign = []
							for j in same[i]: 
								assign.append(pairing[j])
							dist = assign[0][1]
							third = 0			
							for j in range(1,len(assign)):
								if assign[j][1] < dist:
									change.append(assign[third])
									dist = assign[j][1]
									third = j 
								else: change.append(assign[j])
					for j in change: pairing.remove(j)
				for i in pairing:  # you have a pairings list now
				# break pairings down to smaller list parts
					takenPas.append(str(i[2])) 
					takenDr.append(str(i[0]))
					taken.append(tuple([str(i[0]),str(i[2])]))
					available.remove(str(i[0]))
			else:
				for i in pairing: 
					for j in pairing:
						if i != j:
							if i[2] == j[2]: # check pairing indexes for optimum
								if (j[0]not in store) and (i[0] not in store):
									if i[1] <= j[1]:
										indexes[int(j[0])] += 1
										store.append(j[0])
									elif i[1] > j[1]:
										indexes[int(i[0])] += 1
										store.append(i[0])
		return taken		

	def match(self, pairings): # this takes the pairings and adjusts them into 
	# self.takenPairs, and checks the base case of a 1 to 1 pairings 
	# then it assigns the locations to the attributes of the driver and pas
		if len(self.driverList) == 1 and len(self.passengerList)==1:
			self.driverList[0].passengerLocation = self.passengerList[0].location
			self.driverList[0].passengerDestination = self.passengerList[0].destination
			self.takenPairs.append((self.driverList[0],self.passengerList[0]))
			return
		for i in pairings:
			self.driverList[int(i[0])].passengerLocation = self.passengerList[int(i[1])].location
			self.driverList[int(i[0])].passengerDestination = self.passengerList[int(i[1])].destination
			self.takenPairs.append((self.driverList[int(i[0])],self.passengerList[int(i[1])]))

	def randomMatch(self): # this does the random matching algorithm
		pairings = []
		count = 0 
		while count != min(len(self.driverList), len(self.passengerList)):
			pairings.append((str(count),str(count)))
			count += 1
		return pairings

	def averageTime(self): # this finds the average time to Pas from driver 
	# to passenger
		total=0
		for pair in self.takenPairs:
			total+=pair[0].timePas
		return total/len(self.takenPairs)
		
	def final(self): #returns true if driver makes it to the destination
		for pair in self.takenPairs:
			if pair[1].location!=pair[1].destination:
				return False
		return True


class Driver(object):
	def __init__(self, idvalue):
		self.driverRow = random.randint(0,14)
		self.driverCol = random.randint(0,14)
		self.driverLocation = (self.driverRow, self.driverCol) 
		self.passengerLocation = (-1,-1)
		self.passengerDestination = (-1,-1)
		self.id = idvalue
		self.timePas = 0
		self.time = 0
		self.timeDes = 0
		self.globalTime = 0
		self.timerDelay = 100
		self.occupant = 0
		self.pos=0

	def timerFiredPickUp(self): # sets the timer Fired for the pick up move
		self.globalTime += self.timerDelay
		if self.globalTime % 1000 == 0:
			self.time += 1
			self.timePas += 1
			moveTo(self)	


###############################
# Previous tests
###############################

#Passenger1 = Passenger("Dipak")
#print(Passenger1.location)
#print(Passenger1.destination)
# print(Passenger1.location)
# Match1 = Match(10,14)

# passengerPriority,driverPriority=Match1.priority()
# dr_n_pas=Match1.stableMatch(driverPriority,passengerPriority)
# print(dr_n_pas)
# x=Match1.match(dr_n_pas)
# driver1 = Match1.findDriver(Passenger1)
# Driver1 = Driver("Fred", 0)
# print(driver1.driverLocation)
# driver1.timerFiredPickUp()
# print(driver1.driverLocation)2
# x=[1,2,3]
# driver1.timerFiredDropOff()
# print(driver1.driverLocation)
# print(driver1.timePas)
# print(driver1.timeDes)

#x = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
#print(type(x))


