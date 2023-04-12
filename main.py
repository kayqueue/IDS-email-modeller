# imports
import time

# other files
from initial_input import userInput, readEvents, readStats, consistencyCheck, processEvents, processStats
from activity_simulation import generateDataSet, simulateActivity
from analysis_engine import readLogs, outputData
from alert_engine import getNewInput, getThreshold, anomalyCounter, flagging


# main()
def main():
	#################
	# INITIAL INPUT #
	#################
	eventFile, statsFile, days = userInput()
	eventData = readEvents(eventFile)
	statsData = readStats(statsFile)

	print("--------------------------------------------------------------------")
	print(f"Checking for inconsistencies between {eventFile} and {statsFile}...")
	print("--------------------------------------------------------------------")
	if not consistencyCheck(eventData, statsData):
		exit() # stop program if inconsistencies are found
		
	print("\n")
	
	time.sleep(1)

	print("------------------------")
	print(f"Processing {eventFile}...")
	print("------------------------")
	allWeight = processEvents(eventData)

	print("\n")
	time.sleep(1)

	print("------------------------")
	print(f"Processing {statsFile}...")
	print("------------------------")
	processStats(statsData)

	print("\n")
	time.sleep(1)

	###########################################
	# ACTIVITY SIMULATION ENGINE AND THE LOGS #
	###########################################

	# generate data set for each event for each day
	dataSet = generateDataSet(days, eventData, statsData)
	time.sleep(1)
	
	# simulate activity and write to logs file
	simulateActivity("logs.txt", days, eventData, dataSet)
	time.sleep(1)
	
	print("\n")
	
	###################
	# ANALYSIS ENGINE #
	###################
	
	# get data from logs file
	data, eventName = readLogs("logs.txt")
	
	# write result of analysis to text file - BASELINE
	mean, stddev = outputData(data, eventName, "Baseline_Statistics.txt")
	
	################
	# ALERT ENGINE #
	################
	logCount = 1
	while True:
		
		time.sleep(1)
		
		# get new stats file and number of days
		newStatsFile, newDays = getNewInput()

		# read new stats file
		newStatsData = readStats(newStatsFile)

		# generate data set for each event for each day
		newDataSet = generateDataSet(newDays, eventData, newStatsData)

		# new logs file
		newLogsFile = f"logs{logCount+1}.txt"
		logCount += 1
			
		# simulate activity and write to new logs file
		simulateActivity(newLogsFile, newDays, eventData, newDataSet)
		
		# get threshold
		threshold = getThreshold(allWeight)
		
		# anomaly counter
		dailyAnomalyCounter = anomalyCounter(newLogsFile, allWeight, mean, stddev)
		
		# check for anomaly
		print(f"\nThreshold: {threshold}")
		flagged = flagging(dailyAnomalyCounter, threshold)
		
		# continue reading new files?
		option = input("Continue to read new Stats file?(y/n): ")
		
		while True:	
			if option.lower() == "y" or option.lower() == "n":
				break
			else:
				option = input("Please enter y or n: ")
		
		if option.lower() == "n":
			break
	
	print("Exiting Alert Engine...Goodbye")
	exit()
	
	
# driver of the program
if __name__ == "__main__":
	main()
