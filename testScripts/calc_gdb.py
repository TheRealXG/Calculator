#This is a test script to interact with GDB to set a breakpoint and wait 
# 10sec for a response from the Calculator console.
from pygdbmi.gdbcontroller import GdbController
from pygdbmi.constants import GdbTimeoutError
from pprint import pprint
import subprocess

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

	#Set a breakpoint. Specific line value isn't very robust though. Needed for initial input
	print("\n######\n-break-insert --source main.c --line 88\n")
	response = gdbmi.write("-break-insert --source main.c --line 88")
	print_output(response)

	# Allow it to continue
	continue_to_running(gdbmi, response)

	# Wait for first response
	print("\n######\nWait 10seconds for response\n")
	response = gdbmi.get_gdb_response(10)
	print_output(response)

	# Create watch point now that input is in scope (had to set known breakpoint above then interact to get in scope)
	print("\n######\n-break-watch input\n")
	response = gdbmi.write("-break-watch input")
	print_output(response)
	print("Watchpoint #: " + str(response[0]['payload']['wpt']['number']))
	pprint(response)

	print("\n######\nprint &input\n")
	response = gdbmi.write("print &input")
	pprint(response)

	print("\n######\nprint input\n")
	response = gdbmi.write("print input")
	pprint(response)

	# Allow it to continue
	continue_to_running(gdbmi, response)

	#TODO How to poll for a response without being tied to an X second timer?
	#Can I wait at the GDB prompt and know when something comes through or do I have to check?

	# Wait for response that will break on 'input'
	while(True):
		print("\n######\nWait 1 second for response\n")
		try:
			response = gdbmi.get_gdb_response(1)
			print_output(response)
			pprint(response)
			# Assuming response is due to hitting Input breakpoint (can check later)
			print("\n######\nset Input (hardcoded address) to ASCII 53\n")
			response = gdbmi.write("-gdb-set *((char*) 0x2080b7) = 53")
			pprint(response)
			continue_to_running(gdbmi, response)
		except GdbTimeoutError:
			print("***Try Again***")

	# This works to modify memory since we know the location. This is happening in vscanf scope.
	#print("\n######\nset Input (hardcoded address) to ASCII 53\n")
	#response = gdbmi.write("-gdb-set *((char*) 0x2080b7) = 53")
	#pprint(response)

	#continue_to_running(gdbmi, response)




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