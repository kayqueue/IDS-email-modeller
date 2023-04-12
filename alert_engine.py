# imports
import os
from initial_input import readStats
from activity_simulation import generateDataSet, simulateActivity

# get new Stats file and the number of days from user
def getNewInput():
	while True:
		statsFile = input("Enter filename for new Stats File: ")
		
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
	
	return statsFile, int(days)
	
	
# get threshold
def getThreshold(allWeight):
	sum = 0
	for i in range(len(allWeight)):
		sum += allWeight[i]
		
	return 2 * sum
	
# read new log file
def readNewLogs(filename):
	print(f"Commencing analysis for {filename}...\n")

	dailyData = [] # track all the data for each day
	
	# get event names
	with open(filename, "r") as fin:
		while True:
			line = fin.readline().strip() # day number
			
			if not line: # EOF reached
				break
				
			daily = [] # track daily data

			noOfEvents = int(fin.readline().strip()) # number of events
		
			for i in range(noOfEvents): # go through each event for a day
				daily.append(fin.readline().strip().split(":")[2])
			
			dailyData.append(daily) # add to 2d list to track daily data
			fin.readline().strip() # new line
					
	return dailyData
	
# for each event:
# 	[total - mean(from Baseline.txt)] / stddev(from Baseline.txt) * weight(from Events.txt)
def anomalyCounter(filename, weight, mean, stddev):
	print("Currently calculating daily totals...\n.\n.\n.")

	# read new logs file and capture its data
	data = readNewLogs(filename) # data = [[], [], ..., []]
	
	# track the daily totals
	dailyCounter = []
	
	for index, value in enumerate(data): # loop through the number of days
		counter = 0 # track counter for daily events
		for i, v in enumerate(value): # loop through the number of events
			counter += float(round(((abs((float(v) - mean[i])) / stddev[i]) * weight[i]), 2))
		
		dailyCounter.append(counter)
	
	print("Daily totals calculated!\n")
	return dailyCounter


# check for anomaly
def flagging(data, threshold):
	print("Currently checking for anomalies...\n.\n.\n.")

	flagged = []
	
	for i in range(len(data)):
		alert = False
		if data[i] > threshold:
			flagged.append(i + 1) # day number
			alert = True
		
		print(f"Day {i + 1} anomaly count = {round(data[i], 2)} {'--- FLAGGED' if alert == True else ''}")

	print("\n")
			
	# alert
	if len(flagged) != 0:
		print("ALERT! Anomalies detected!")
		print("--------------------------")
		for index, value in enumerate(flagged):
			print(f"Day {value} has been flagged!")
		print("\n")
	else:
		print("Congratulations! There are no anomalies!\n")
	
			
	return flagged
