# imports
import os

# user input
def userInput():
	print("Welcome to IDS")
	
	while True:
		eventFile = input("Enter filename for Events: ")
		
		if not os.path.exists(eventFile):
			print("Please enter the correct Events File again")
			continue
		
		break
	
	print("")

	while True:
		statsFile = input("Enter filename for Stats: ")
		
		if not os.path.exists(statsFile):
			print("Please enter the correct Stats File again")
			continue
		
		break
		
	print("")
	
	while True:
		days = input("Enter the number of Days: ")
		
		if days.__contains__("."):
			print("Please enter a whole number")
			continue
			
		try:
			days = int(days)
		except:
			print("Please enter a whole number")
			continue
	
		if days == 0:
			print("Please enter number more than 0")
			continue
	
		break
		
	print("")
	
	return eventFile, statsFile, days

# read event file
def readEvents(filename):
	line = []

	with open(filename, "r") as fin:
		lines = fin.readlines()

		for each in lines:
			line.append(each.strip())
	
	return(line)
	
# read stats file
def readStats(filename):
	line = []

	with open(filename, "r") as fin:
		lines = fin.readlines()

		for each in lines:
			line.append(each.strip())
	
	return line
			
# check for inconsistencies between Events and Stats file
def consistencyCheck(eventData, statsData):
	noOfEventData = int(eventData[0])
	noOfStatsData = int(statsData[0])
	
	# different number of data
	if noOfEventData != noOfStatsData:
		print("Number of data is inconsistent")
		
	# loop through array of data and check the consistency between each event
	for i in range(1, noOfEventData):
		# different event
		if eventData[i].split(":")[0] != statsData[i].split(":")[0]:
			print(f"Inconsistencies found in line {i + 1}")
			return False
	
	print("No inconsistencies found")
	return True


# process Event file
def processEvents(data):
	noOfEvents = int(data[0]) # number of events on the first line
	allWeight = []
	
	for i in range(1, noOfEvents + 1):
		each = data[i].split(":")
		
		# capture each property
		eventName = each[0]
		eventType = each[1]	
		minimum = each[2]
		maximum = each[3]
		weight = each[4]
	
		# validations
		# neither Continuous or Discrete
		if eventType != "C" and eventType != "D":
			print("Event type must be either C or D")
			return
		
		# minimum value
		if minimum == "": # value empty
			print("Minimum values cannot be empty")
			return
	
		# maximum value
		if maximum == "": # value empty
			print("Maximum values cannot be empty")
			return
	
		# weight value
		if weight.find(".") > 0: # float value found in weight variable
			print("Weight values must be an integer")
			return
	
		if weight == "": # value empty
			print("Weight values cannot be empty")
	
		# in the case of Discrete events
		if eventType == "D":
			# float values found in minimum or maximum variable
			if minimum.find(".") > 0 or maximum.find(".") > 0:
				print("Float found in a Discrete Event")
				return
		
		# in the case of Continuous events
		if eventType == "C":
			minimum = "{:.2f}".format(float(minimum)) # 2 decimal places
			maximum = "{:.2f}".format(float(maximum)) # 2 decimal places
				
		# sum of weight
		allWeight.append(int(weight))
		
		print(f"Event:{eventName}, Type:{eventType}, Min:{minimum}, Max:{maximum}, Weight:{weight}")
	return allWeight

# process Stats file
def processStats(data):
	noOfEvents = int(data[0]) # number of events on the first line
	
	for i in range(1, noOfEvents + 1):
		each = data[i].split(":")
		
		# capture each property
		eventName = each[0]
		mean = each[1]
		standard_deviation = each[2]
		print(f"Event:{eventName}, Mean:{mean}, Standard Deviation:{standard_deviation}")
			
