#This is a test script to interact with GDB to set a breakpoint and wait 
# 10sec for a response from the Calculator console.
# NOTE: This requires calc.exe to be compiled WITHOUT -02 or other optimization flags
from pygdbmi.gdbcontroller import GdbController
from pygdbmi.constants import GdbTimeoutError
from pprint import pprint
import subprocess
import sys

def main():
	# Start gdb process
	gdbmi = GdbController(["arm-rtems5-gdb", "--nx", "--quiet", "--interpreter=mi3"])
	#print(gdbmi.get_subprocess_cmd())  # print actual command run as subprocess

	# Load binary a.out and get structured response
	print("\n######\n-file-exec-and-symbols build/arm-rtems5-realview_pbx_a9_qemu/rtems/calc.exe\n")
	response = gdbmi.write("-file-exec-and-symbols build/arm-rtems5-realview_pbx_a9_qemu/rtems/calc.exe")
	print_output(response)
	[{'message': u'thread-group-added',
	  'payload': {u'id': u'i1'},
	  'type': 'notify'},
	 {'message': u'done', 'payload': None, 'type': 'result'}]

	# Connect to the remote host 
	print("\n######\n-target-select remote localhost:1234\n")
	response = gdbmi.write("-target-select remote localhost:1234")
	print_output(response)

	"""
	#Set a breakpoint. Specific line value isn't very robust though. Needed for initial input
	print("\n######\n-break-insert --source main.c --line 101\n")
	response = gdbmi.write("-break-insert --source main.c --line 101")
	print_output(response)

	# Allow it to continue
	continue_to_running(gdbmi, response)

	# Wait for first response
	print("\n######\nWait 10seconds for response\n")
	response = gdbmi.get_gdb_response(10)
	print_output(response)
	"""

	# Create watch point now that input is in scope (had to set known breakpoint above then interact to get in scope)
	print("\n######\n-break-watch flag\n")
	response = gdbmi.write("-break-watch flag")
	watchpoint_flag = response[0]['payload']['wpt']['number']
	print_output(response)
	print("Watchpoint #: " + str(response[0]['payload']['wpt']['number']))
	pprint(response)

	print("\n######\nprint &input\n")
	response = gdbmi.write("print &input")
	pprint(response)
	# Get the memory address of "input" while the program is stopped in scope
	addr_of_input = get_addr_of_var(gdbmi, "input")
	addr_of_flag = get_addr_of_var(gdbmi, "flag")

	print("\n######\nprint flag\n")
	response = gdbmi.write("print flag")
	pprint(response)

	# TESTING Set the first value (can this be removed?)
	print("\n######\nset Input (hardcoded address) to ASCII 53\n")
	response = gdbmi.write("-gdb-set *((char*) " + str(addr_of_input) + ") = 53")
	pprint(response)
	print("\n######\nprint input\n")
	response = gdbmi.write("print input")
	pprint(response)

	# Set flag to 0 to indicate Calculator can continue
	print("\n######\nChange flag to 0\n")
	response = gdbmi.write("-gdb-set *((_Bool *) " + str(addr_of_flag) + ") = 0")
	pprint(response)
	print("\n######\nprint flag\n")
	response = gdbmi.write("print flag")
	pprint(response)

	response = gdbmi.write("-exec-continue")
	pprint(response)
	if is_breakpoint(response):
		# Find breakpoint message, get old/new values and compare, change memory

	# Allow it to continue
	#continue_to_running(gdbmi, response)

	#TODO How to poll for a response without being tied to an X second timer?
	#Can I wait at the GDB prompt and know when something comes through or do I have to check?

	# Wait for response that will break on 'input'
	while(True):
		print("\n######\nWait 10 seconds for response\n")
		try:
			response = gdbmi.write("-exec-continue")
			#response = gdbmi.get_gdb_response(10)
			print_output(response)
			pprint(response)
			#TODO Trying to find out what the old and new values are after a watchpoint is hit to make decisions
			# on, this could be useful for allowing this to escape with a "q" or to know when the Calc
			# is ready for another input when testing via memory manipulation only

			# If a breakpoint was hit and the breakpoint number matches the watchpoint set above
			# then get the Old and New values to assess and/or modify
			if response[0]['message'] == "breakpoint-modified":
				bkpt_hit = response[0]['payload']['bkpt']['number']
				if bkpt_hit == watchpoint_flag:
					values = get_old_new_value(response)

					# Transitioned from 0 to 1, so ready to set input
					if (str(values[0]) == "false" and str(values[1]) == "true"):
						# Modify input value to equal "5"
						print("\n######\nset Input (hardcoded address) to ASCII 53\n")
						response = gdbmi.write("-gdb-set *((char*) " + str(addr_of_input) + ") = 53")
						pprint(response)
						print("\n######\nprint input\n")
						response = gdbmi.write("print input")
						pprint(response)

						# Set flag to 0 to indicate Calculator can continue
						response = gdbmi.write("-gdb-set *((_Bool *) " + str(addr_of_flag) + ") = 0")
						pprint(response)
						"""

			#response = _gdbmi.write("-exec-continue")
			#continue_to_running(gdbmi, response)
		except GdbTimeoutError:
			print("***Try Again***")

	# This works to modify memory since we know the location. This is happening in vscanf scope.
	#print("\n######\nset Input (hardcoded address) to ASCII 53\n")
	#response = gdbmi.write("-gdb-set *((char*) 0x2080b7) = 53")
	#pprint(response)

	#continue_to_running(gdbmi, response)

def execute_breakpoint_x(_gdbmi, _response, bkpt_num):


def is_breakpoint(_response):
	"""
	This will take a response and return if it contains a "breakpoint-modified" message


	"""
	for i in _response:
		if str(i['message']) == "breakpoint-modified":
			return True	
	return False


def get_addr_of_var(_gdbmi, variable):
	"""
	This returns the memory address of a variable passed in. This assumes the variable is in scope 
	at the time of execution

	Parameters: Variable name to get the address of

	Returns: String of the memory address
	"""
	_response = _gdbmi.write("print &" + variable)
	output = get_payloads(_response)
	output = output.split("=",1)[1].split()
	output = [i for i in output if i.startswith('0x')]
	return output[0]



def get_old_new_value(_response):
	"""
	This will return the Old Value and New Value when GDB hits a Watch-Point

	Paramters:
	arg1: THe List of Dicts response from GDBMI

	Returns a list with the Old [0] and New [1] values
	"""
	values = ["", ""]
	payload = get_payloads(_response).replace("\\"," ")
	values[0] = payload.split("Old value =",1)[1].split()[0]
	values[1] = payload.split("New value =",1)[1].split()[0]
	return values


def get_payloads(_response):
	"""
	Iterate through response and pull the all of the "none" payloads out

	It seems the "none" payloads contain a lot of the information after a watch-point is hit.
	This may not be a long term function or need additional parameters for the types of payloads
	to get,s uch as "none" or "stopped" etc.
	"""
	retr_val = ""
	for i in _response:
		if str(i['message']) == "None":
			retr_val += i['payload']
	return retr_val


def continue_to_running(_gdbmi, _response):
	"""
	This function executes the "continue" command until the messages being returned are "running"
	
	When this returns GDB should be in a continually running state waiting for GDB input or program breaks
	If the latest response was "running" then this won't execute any more "continue" commands

	Parameters:
	arg1: GDBMI instance that controls the GDB intercace
	arg2: The most recent GDBMI response. 
	"""
	while _response[-1]['message'] != "running":
		print("\n#####\n-exec-continue #\n")
		_response = _gdbmi.write("-exec-continue")
		print_output(_response)

	
def print_output(output):
	"""
	This function prints all values for the "message" field in the response structure

	Parameters:
	arg1 (list of dicts): Response structure returned from GDBMI response
	"""
	for i in output:
		print("Message: " + str(i['message']))

	

if __name__ == "__main__":
    main()