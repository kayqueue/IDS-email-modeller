Grade: 14/14

# Goal:
to design and implement a command line Email system event modeller and intrusion detection system in accordance with the system description below.


Initial Input
--------------
During the execution of the program, an Event file and a Stats file will be requested, along with the number of Days.
Both files define the formats and the distributions of the events to be modelled.
Days is an integer used in the next section.
Here goes an example Events.txt file. This file describes the events and some of their parameters.

```
5
Logins:D:0::3:
Time online:C:0:1440:2:
Emails sent:D:0::1:
Emails opened:D:0::1:
Emails deteled:D:0::2:
```

The first line contains the number of events being monitored. Each subsequent line is of the form
Event name:[CD]:minimum:maximum:weight:
C and D represent continuous and discrete events respectively. Discrete events must take integer values
and occur one at a time, continuous events don’t need to take an integer value and an occurrence of that
event may be of any value. The minimum and maximum specify the allowed range for that event type
across a day. Continuous events need to be recorded to two decimal places. The weights are used in the
alert engine and will always be positive integers.

The file Stats.txt contains the distributions to be modelled for the events. Here goes an example
Stats.txt file.

```
5
Logins:4:1.5:
Time online:150.5:25.00:
Emails sent:10:3:
Emails opened:12:4.5:
Emails deteled:7:2.25:
```

The first line again contains the number of events being monitored. Each subsequent line is of the form
Event name:mean:standard deviation:

A report with the description of:
1. How the program stores the events and statistics internally.
2. Potential inconsistencies between Events.txt and Stats.txt.

Activity Simulation Engine and the Logs
---------------------------------------
Once the intial setup has taken place, the activity engine should start generating and logging events.
Program should give some indication as to what is happening.
The program will be attempting to produce statistics approximately consistent with the statistics specified in the file Stats.txt.
The program will log for the number of Days specified at the initial running of IDS.
This collection of events forms the baseline data for the system.

A report with the description of:
1. The process used to generate events approximately consistent with the particular distribution. This
is likely to differ between discrete and continuous events.
2. The name and format of the log file, with justification for the format. You will need to be able to
read the log entries for subsequent parts of the program.

Analysis Engine
---------------
Program should indicate it has completed event generation and is going to begin analysis.
Program can begin to measure that baseline data for the events and determine the statistics associated with the baseline.

Alert Engine
------------
The alert engine is used to check consistency between “live data” and the base line statistics. 
Once this phase is reached, program will prompt the user for a file, containing new statistics, and also request for the number of days.
The new statistics file should have the same format as Stats.txt from earlier but will generally have different parameters for the events.
The activity engine produces data for the number of days specified by the user, and the daily totals which will be used for alert detection.
For each day generated, compare an anomaly counter with a threshold to determine whether an alert should be created. 
The anomaly counter is calculated by adding up the weighted number of standard deviations each specific tested event value is from the mean for that event, where the standard deviation and mean are those you have generated from the base data and reported, and the weight is taken from the original Events.txt file.
For example, if the mean number of logins per day is 4 and the standard deviation is 1.5, then if we get 1 login in a day we are 2 standard deviations from the mean. Referring back to the weight of the login event we see it was 2 so the login event contributes 4 to our overall anomaly counter.
The threshold for detecting an intrusion is 2∗(Sums of weights) where the weights are taken from Events.txt.
If the anomaly counter is greater or equal to the threshold you should report this as an anomaly.
The program will output the threshold, and give the anomaly counter for each day as well as stating each day as okay or flagged as having an alert detected.
Once the alert engine part has finished the program returns to the start of this phase, so another set of statistics and number of days can be considered.


# Compilation Instructions
open up a terminal and run the program by typing the following into the command line:
python3 main.py

OR 

python main.py


NOTE:
If you have your own file for Events and Statistics, place them in the folder. Otherwise, I have one Events file named Events.txt and two Stats file named Stats.txt and Stats2.txt.
For the initial input, please use Events.txt and Stats.txt.
Stats2.txt can be used for the second activity simulation further in the program.

SECOND NOTE:
If you want to rerun the program, please delete Baseline_Statistics.txt and all logs.txt files (e.g. logs.txt, and logs2.txt)