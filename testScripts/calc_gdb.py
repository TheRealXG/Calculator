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

	# Create the watchpoing on the flag to know when to modify Input
	print("\n######\n-break-watch flag\n")
	response = gdbmi.write("-break-watch flag")
	watchpoint_flag = response[0]['payload']['wpt']['number']
	print_output(response)
	print("Watchpoint #: " + str(response[0]['payload']['wpt']['number']))
	pprint(response)

	# Get the memory addresses of the relevant variables (input and flag to restart the Calculator)
	addr_of_input = get_addr_of_var(gdbmi, "input")
	addr_of_flag = get_addr_of_var(gdbmi, "flag")
	addr_of_output = get_addr_of_var(gdbmi, "outC.outputDisplay")
	# Set the first input value
	set_input(gdbmi, addr_of_input, addr_of_flag, "53")
	
	response = gdbmi.write("-exec-continue")
	pprint(response)

	# This will continually loop and set the input value, trigger the flag, and try again.
	while(True):
		# If the response contains a breakpoint message then process to see if it is what we want
		if is_breakpoint(response):
			# Iterate through all messages in response to find the break-point message
			for i in response:
				if str(i['message']) == "breakpoint-modified":
					# Found the breakpoint message, get the breakpoint number to make sure it matches our watch above
					bkpt_hit = i['payload']['bkpt']['number']
					if bkpt_hit == watchpoint_flag:
						# Get the old and new values to confirm the transition
						values = get_old_new_value(response)
						# Transitioned from 0 to 1, so ready to set input
						if (str(values[0]) == "false" and str(values[1]) == "true"):
							# Modify input value to equal "5" (ASCII 53)
							set_input(gdbmi, addr_of_input, addr_of_flag, "53")
							response = gdbmi.write("print outC.outputDisplay")
							print("\n#####\nPrint outC\n")
							print(get_output(response))
		response = gdbmi.write("-exec-continue")
		pprint(response)

def is_error(_response):
	"""Determines if there is an error in the response. Returns True if there was an error
	"""
	for i in _response:
		if str(i['message']) == "error":
			return True
	return False

def set_input(_gdbmi, _addr_of_input, _addr_of_flag, value):
	"""
	This will set the variable input to the value passed and set the flag to 0 to release the Calculator
	"""
	print("\n######\nset Input (hardcoded address)\n")
	response = _gdbmi.write("-gdb-set *((char*) " + str(_addr_of_input) + ") = " + str(value))
	pprint(response)
	print("\n######\nprint input\n")
	response = _gdbmi.write("print input")
	pprint(response)

	# Set flag to 0 to indicate Calculator can continue
	response = _gdbmi.write("-gdb-set *((_Bool *) " + str(_addr_of_flag) + ") = 0")
	pprint(response)


def is_breakpoint(_response):
	"""
	This will take a response and return if it contains a "breakpoint-modified" message

	Parameters: The response list of dicts from a GDBMI write
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

def get_output(_response):
	"""This will extract the outC.outputDisplay value from a GDB response that called "print outC.outputDisplay"
	"""
	output = get_payloads(_response).split('\\')
	output = [i for i in output if i.startswith('"')]
	return output[0][1:]


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
	to get, such as "none" or "stopped" etc.
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