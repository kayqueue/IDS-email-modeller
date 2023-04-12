import statistics as s
import time

# simulate activity and write to logs file - BASELINE
def simulateActivity(filename, days, eventData, dataSet):
	print(f"\nCurrently simulating activity with the data set generated...")

	noOfEvents = int(eventData[0])
	
	fout = open(filename, "a")

	for i in range(days):
		fout.write(f"Day {i + 1}\n")
		fout.write(f"{noOfEvents}\n")
		
		for j in range(noOfEvents):
			# deconstruct eventData
			data = eventData[j + 1].split(":")
			eventName = data[0]
			eventType = data[1]
			
			fout.write(f"{eventName}:{eventType}:{dataSet[j][i]}:\n")
		
		fout.write("\n")
		
	fout.close()
	
	time.sleep(0.5)
	print(f".\n.\n.\n{days} days of data has been written to {filename}!")
	

# generate data set for each event
def generateDataSet(days, eventData, statsData):
	print(f"Currently generating data for {days} days of events...")

	# get the number of events
	noOfEvents = int(eventData[0])
	
	# track the set of data to be used to simulate activity for the baseline
	activityData = []
	
	for i in range(days):
		for j in range(1, noOfEvents + 1):
			# split event data
			eData = eventData[j].split(":")
			eventName = eData[0] # name of event		
			eventType = eData[1] # type of event
			minimum = int(eData[2]) # min of event
			maximum = int(eData[3]) # max of event
		
			# split stats data
			sData = statsData[j].split(":")
			mean = float(sData[1]) # mean
			standardDeviation = float(sData[2]) # standard deviation
			
			# generate set of data as close to mean and stdev
			dataSet = generateData(mean, standardDeviation, days, minimum, maximum, eventType)
			activityData.append(dataSet) # add
		
	time.sleep(0.5)
	print(".\n.\n.\nData set generation completed!")
	return activityData

# generate set of data as close to mean and stdev
def generateData(mean, standardDeviation, days, minimum, maximum, eventType):
	while True:
		n = s.NormalDist(mu = mean, sigma = standardDeviation)
		samples = n.samples(days)
		
		# keep value within min/max bounds
		for index in range(len(samples)):
			if eventType == "D": # discrete event
				samples[index] = round(samples[index]) # round value to integer
				
			if eventType == "C": # continuous event
				samples[index] = round(samples[index], 2) # round value to 2 decimal places
				
			# check for out of bounds
			if samples[index] < minimum or samples[index] > maximum:
				continue
	
		if days >= 10:
			# keep mean and standard deviation within 0.5% +/-
			if s.mean(samples) < mean * 0.95 or s.mean(samples) > mean * 1.05 or s.stdev(samples) < standardDeviation * 0.95 or s.stdev(samples) > standardDeviation * 1.05:
				continue # continue looping and generating new sample data
			else:
				return samples # return generated sample data
		else:
			# keep mean and standard deviation within 1% +/-
			if s.mean(samples) < mean * 0.9 or s.mean(samples) > mean * 1.1 or s.stdev(samples) < standardDeviation * 0.9 or s.stdev(samples) > standardDeviation * 1.1:
				continue # continue looping and generating new sample data
			else:
				return samples # return generated sample data

