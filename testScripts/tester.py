import os
import sys
import argparse
import random
from random import seed
from random import randint
import xml.etree.ElementTree as ET

# Uncomment below to set to constant for testing purposes
#seed(1)

# define your test params
numRandTests = 15
maxFailedTestsAllowed = 2
addedIntegerMax = 9
addedIntegerMin = 0
ops = ['+', '-', '\*', '/']
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
# List of the values passed into the test
testList = []
failureList = []
resultsList = []
numTestsPassed = 0
numTestsFailed = 0

#Create XML tree for JUnit output
testsuite = ET.Element('testsuite')

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
	
	outputResults_junit(numTestsRun)

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
				
				testInput = str(firstInt) + " " + str(operator) + " " + str(secondInt)
				testOutput = str(total)
				
				testList.append(ET.SubElement(testsuite,'testcase'))
				testList[testCtr].set('classname','Calc')
				testList[testCtr].set('name',testInput + ' = ' + testOutput + ':  ' + inputs[4])

				os.system("./" + expScriptName + ".exp " + testInput + " " + testOutput + " " + str(testCtr))
				
				testCtr += 1
				
	return testCtr

    
# run the tests in expect scripts with random inputs
def runRandTests():
	for i in range(numRandTests):
		if randint(1,10) >= 5:
			failure = 2
		else:
			failure = 1
		# This will set the expected test output to always match the values
		if failure == 2:
			failureList.append("F")
		else:
			failureList.append("P")
		
		firstInt = randint(addedIntegerMin, addedIntegerMax)
		secondInt = randint(addedIntegerMin, addedIntegerMax)
		op_sel = randint(0,3)

		# Exception handling to prevent divide by 0 errors. Calculator doesn't work correctly with division right now so what is substituted doesn't matter right now.
		try: 
			outputs = [firstInt + secondInt,
						firstInt - secondInt,
						firstInt * secondInt,
						firstInt / secondInt]
		except ZeroDivisionError:
			outputs = [firstInt + secondInt,
						firstInt - secondInt,
						firstInt * secondInt,
						"N/A"]

		testInput = str(firstInt) + " " + str(ops[op_sel]) + " " + str(secondInt)
		testOutput = str(outputs[op_sel] * failure)
		
		testList.append(ET.SubElement(testsuite,'testcase'))
		testList[i].set('classname','Calc')
		testList[i].set('name',testInput + ' = ' + testOutput + ':  ' + failureList[i])

		os.system("./" + expScriptName + ".exp " + testInput + " " + testOutput + " " + str(i))


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
				setFailure(i)
			if (failureList[i].lower() == 'f' and resultsLine == failMessage):
				numTestsPassed += 1;
				resultsList.append("Test " + str(i+1) + ": Passed")
			if (failureList[i].lower() == 'f' and resultsLine != failMessage):
				numTestsFailed += 1;
				resultsList.append("Test " + str(i+1) + ": Failed")
				setFailure(i)

	return [numTestsPassed, numTestsFailed]			

# Add a filure element to the XML Tree for JUnit outputs at the test # listed
def setFailure(testNum):
	failElement = ET.SubElement(testList[testNum], 'failure')
	failElement.set('type','Mis-Math')
	failElement.text = 'Output Not As Expected'

# Write the results out as a JUnit formatted XMl file
def outputResults_junit(numTestsRun):
	testsuite.set('tests', str(numTestsRun))

	tree = ET.ElementTree(testsuite)
	tree.write("results.xml")			
				
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
