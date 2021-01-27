import os
import sys
import argparse
from random import seed
from random import randint

seed(1)

# define your test params
numRandTests = 1
maxFailedTestsAllowed = 2;
addedIntegerMax = 9
addedIntegerMin = 0
expScriptName = "testScripts/Test_Calculator"
logDir = "logs"
logName = "test_calculator"
logExt = ".log"
passMessage = "Test Pass"
failMessage = "Test Fail"

# initialize vars
firstInt = 0
secondInt = 0
failure = 1
failureList = []
resultsList = []
numTestsPassed = 0
numTestsFailed = 0

resultsLine = ""

def main():
	numTestsRun = 0
	
	inputFile = False
	inputFileName = ""
	
	# check for input file
	if len(sys.argv) > 1:
		inputFile = True
		inputFileName = sys.argv[1]
		if not os.path.exists(inputFileName):
			print("Input file not found. Generating random values.\n")
			inputFile = False

	# use input file if given, random if not given
	if inputFile:
		numTestsRun = runInputTests(inputFileName)
	else:
		runRandTests()
		numTestsRun = numRandTests
		
	numPassedFailed = aggregateResults(numTestsRun)
	outputResults(numPassedFailed[0], numPassedFailed[1])	
	
	if (numTestsFailed > maxFailedTestsAllowed):
		sys.exit(1)
	else:
		sys.exit(0)
    

# run the tests in expect scripts with input file
def runInputTests(inputFileName):
	testCtr = 0
	
	if not os.path.exists(logDir):
		os.makedirs(logDir)
	with open(inputFileName) as inputFile:
			for line in inputFile:
				inputs = line.split()
				print (inputs)
				if (len(inputs) != 5):
					print("Line " + str(testCtr + 1) + " of the input file is incorrectly formatted. Skipping.")
					continue
					
				firstInt = inputs[0]
				operator = inputs[1]
				secondInt = inputs[2]
				total = inputs[3]
				failureList.append(inputs[4])
				
				os.system("./" + expScriptName + ".exp " + str(firstInt) + " " + str(operator) + " " + str(secondInt) + " " + str(total) + " " + str(testCtr))
				
				testCtr += 1
				
	return testCtr

    
# run the tests in expect scripts with random inputs
def runRandTests():
	for i in range(numRandTests):
		if randint(1,10) >= 5:
			failure = 2
		else:
			failure = 1
		failureList.append(failure)
		
		firstInt = randint(addedIntegerMin, addedIntegerMax)
		secondInt = randint(addedIntegerMin, addedIntegerMax)
		os.system("./" + expScriptName + ".exp " + str(firstInt) + " " + str(secondInt) + " " + str((firstInt + secondInt) * failure) + " " + str(i))


# check test output
def aggregateResults(numTestsRun):
	numTestsPassed = 0
	numTestsFailed = 0
	
	for i in range(numTestsRun):
		# get last line of the log which has the pass/fail message
		with open(logDir + "/" + logName + str(i) + logExt) as logFile:
			for line in logFile:
				pass
			resultsLine = line.strip()
			# increment pass fail counters based on last line
			if (failureList[i].lower() == 'p' and resultsLine == passMessage):
				numTestsPassed += 1;
				resultsList.append("Test " + str(i+1) + ": Passed")
			if (failureList[i].lower() == 'p' and resultsLine != passMessage):
				numTestsFailed += 1;
				resultsList.append("Test " + str(i+1) + ": Failed")
			if (failureList[i].lower() == 'f' and resultsLine == failMessage):
				numTestsPassed += 1;
				resultsList.append("Test " + str(i+1) + ": Passed")
			if (failureList[i].lower() == 'f' and resultsLine != failMessage):
				numTestsFailed += 1;
				resultsList.append("Test " + str(i+1) + ": Failed")
				
	return [numTestsPassed, numTestsFailed]			
				
				
# output results				
def outputResults(numTestsPassed, numTestsFailed):
	resultFile = open("results.txt", "w")
	resultFile.write("***********\n")
	resultFile.write("Total Tests\n")
	resultFile.write("***********\n")
	resultFile.write("Passed: " + str(numTestsPassed) + "\n")
	resultFile.write("Failed: " + str(numTestsFailed) + "\n\n")
	resultFile.write("****************\n")
	resultFile.write("Individual Tests\n")
	resultFile.write("****************\n")

	for i in range (len(resultsList)):
		resultFile.write(resultsList[i] + "\n")
	resultFile.close()
	
	
if __name__ == "__main__":
    main()	
