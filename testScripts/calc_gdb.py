#This is a test script to interact with GDB to set a breakpoint and wait 
# 10sec for a response from the Calculator console.
from pygdbmi.gdbcontroller import GdbController
from pprint import pprint
import subprocess

def main():
	# Start gdb process
	gdbmi = GdbController(["arm-rtems5-gdb", "--nx", "--quiet", "--interpreter=mi3"])
	#print(gdbmi.get_subprocess_cmd())  # print actual command run as subprocess

	# Load binary a.out and get structured response
	response = gdbmi.write("-file-exec-and-symbols build/arm-rtems5-realview_pbx_a9_qemu/rtems/calc.exe")
	pprint(response)
	[{'message': u'thread-group-added',
	  'payload': {u'id': u'i1'},
	  'type': 'notify'},
	 {'message': u'done', 'payload': None, 'type': 'result'}]

	# Connect to the remote host 
	response = gdbmi.write("-target-select remote localhost:1234")
	pprint(response)

	#Set a breakpoint
	response = gdbmi.write("-break-insert --source main.c --line 90")
	pprint(response)
	# Allow it to continue
	response = gdbmi.write("-exec-continue")
	pprint(response)
	response = gdbmi.get_gdb_response(10)
	pprint(response)

if __name__ == "__main__":
    main()