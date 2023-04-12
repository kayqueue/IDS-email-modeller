# imports
import time

# read in logs file
def readLogs(filename):
	print(f"Commencing analysis for {filename}...\n")

	data = []
	eventName = []
	
	# get event names
	with open(filename, "r") as fin:
		fin.readline().strip() # day number
		noOfEvents = int(fin.readline().strip()) # number of events
		
		for i in range(noOfEvents):
			eventName.append(fin.readline().strip().split(":")[0])
	

	with open(filename, "r") as fin:	
		# total lines per day in logs #
		# first line - Day number
		# second line - number of events
		# inbetween = number of events
		# last line - \n
		# total number of lines per day = 3 + number of events
		
		fin.readline().strip()
		noOfEvents = int(fin.readline().strip()) # number of events logged

		count = 0 # track number of events processed
		
		# loop through the file for as many times as the number of events logged per day
		while count < noOfEvents:
			print(f"Processing event number {count + 1}...\n.\n.\n.")
			dailyData = []
			while True:
				line = fin.readline().strip()
				
				if not line: # EOF reached
					data.append(dailyData) # add daily data to list
					count += 1 # increment count
					fin.seek(0) # move cursor to the top of the file
				
					time.sleep(1)
					print(f"Event number {count} processed\n")
					
					# skip the irrelevant lines
					for i in range(2 + count):
						fin.readline().strip()
					
					break # break out of the inner while loop

				# split()
				lineInfo = line.split(":")
				
				# event type
				if lineInfo[1] == "D": # discrete events - integer
					dailyData.append(int(lineInfo[2])) # add daily data
				if lineInfo[1] == "C": # continuous events - 2 d.p.
					dailyData.append(round(float(lineInfo[2]), 2))
				
				
				# skip the remaining information
				for i in range(noOfEvents + 2):
					fin.readline().strip()
					
	return data, eventName

# write statistics to file
def outputData(data, eventName, filename):
	# get mean
	mean = calculateMean(data)
	
	# get variance
	variance = calculateVariance(data, mean)
	
	# get standard deviation
	stddev = calculateStddev(variance)
			
	# write to file
	with open(filename, "a") as fout:
		fout.write(str(len(eventName)))
		for i in range(len(eventName)): # number of events
			fout.write(f"\n{eventName[i]}:{str(mean[i])}:{str(stddev[i])}")
			
	return mean, stddev
		
# calculate mean
def calculateMean(data):
	mean = []
	
	# process data obtained from the logs file - MEAN
	for index, value in enumerate(data): # number of events
		sum = 0
		for i, v in enumerate(value): # number of days
			sum += v
			
			if i + 1 == len(value): # reached the last day
				# calculate mean - maintain at 2dp if exceeded
				mean.append(round(sum / (i + 1), 2))

	return mean
	
# calculate variance
def calculateVariance(data, mean):
	variance = []

	# process data obtained from the logs file - VARIANCE
	for index, value in enumerate(data): # number of events
		sum = 0
		for i, v in enumerate(value): # number of days
			sum += (v - mean[index]) ** 2
			
			if i + 1 == len(value): # reached the last day
				# calculate variance - maintain at 2dp if exceeded
				variance.append(round(sum / (i + 1), 2))

	return variance
	
# calculate standard deviation
def calculateStddev(variance):
	stddev = []
	
	# calculate the standard deviation based on the variance
	for index, value in enumerate(variance):
		stddev.append(round(value ** 0.5, 2)) # square root variance
	
	return stddev
