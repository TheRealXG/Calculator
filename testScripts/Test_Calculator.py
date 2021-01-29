import subprocess
import shlex
import sys
import shutil
import os
## Parameters
# QEMU command to execute
qemu_cmd = shlex.split("qemu-system-arm -net none -no-reboot -nographic -monitor none -serial stdio -M realview-pbx-a9 -m 256M -kernel build/arm-rtems5-realview_pbx_a9_qemu/rtems/calc.exe")
logDir = "logs"
logName = "test_calculator"
logExt = ".log"
# Declare/init values
prompt_1 = "Enter 1st Value"
prompt_op = "Enter an Operator"
prompt_2 = "Enter 2nd Value"
result = "Final Output"
passMsg = "Test Pass"
failMsg = "Test Fail"
test_pass = False

log_name = logDir + "/" + logName + sys.argv[5] + logExt
if os.path.exists(log_name):
    os.remove(log_name)
if not os.path.exists(logDir):
        os.makedirs(logDir)
file = open(log_name, 'a')

process = subprocess.Popen(qemu_cmd,
                        stdin =subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True,
                        bufsize=0)

while True:
    output = process.stdout.readline()
    file.write(output)
    if prompt_1 in output:
        print(output.strip())
        process.stdin.write(sys.argv[1] + "\n")
    elif prompt_op in output:
        print(output.strip())
        process.stdin.write(sys.argv[2] + "\n")
    elif prompt_2 in output:
        print(output.strip())
        process.stdin.write(sys.argv[3] + "\n")
    # TODO Return the output value instead of Pass vs Fail so Test Suite can determine pass/fail,
    #   but this will allow substitution into current script.
    elif result in output:
        print(output.strip())
        # Parse output on spaces to get final entry in line
        output_parsed = output.split()
        # Compare last element in list against expected and remove last character (script ends with ".")
        if sys.argv[4] == str(output_parsed[-1][:-1]):
            print("Test Pass")
            test_pass = True
    elif output:
        print(output.strip())
    # Do something else
    return_code = process.poll()
    if return_code is not None:
        print('RETURN CODE', return_code)
        
        # Process has finished, read rest of the output 
        for output in process.stdout.readlines():
            print(output.strip())
            file.write(output)
        # Print results of test
        if test_pass:
            print(passMsg)
            file.write(passMsg)
        else:
            print(failMsg)
            file.write(failMsg)
        break

# Close stdin
process.stdin.close()
# Close file
file.close