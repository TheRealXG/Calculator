import shlex
import subprocess
from pygdbmi.gdbcontroller import GdbController
from pygdbmi.constants import GdbTimeoutError
from pprint import pprint
import sys

class CalculatorLibrary(object):
    """Library for testing the Ansys *Calculator* App running in QEMU.

    This library interacts with the Console running QEMU to provide input, "Press Buttons" and read output to verify functionality.
    """
    prompt = "Input value" #"Press Button"
    prompt_display = "Display Output"
    bad_input = "Invalid Input"
    #Global variable for GDBMI responses for functions to access
    response = ""

    def __init__(self):
        """Method run at instantiation of Python object, simply initializes results to ''
        """
        self._result = ''


    def start_process(self):
        """Setup method to start QEMU process.
        """
        file_path = "build/arm-rtems5-realview_pbx_a9_qemu/rtems/calc.exe"
        qemu_cmd = shlex.split("qemu-system-arm -net none -no-reboot -nographic -monitor none -serial stdio -M realview-pbx-a9 -m 256M -kernel " + file_path + " -s")
        self.process= subprocess.Popen(qemu_cmd,
                        stdin =subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True,
                        bufsize=0)
        self._result = ''

        # Clear out frist printed responses from console
        output = self.process.stdout.readline()
        print(output.strip())
        output = self.process.stdout.readline()
        print(output.strip())
        
        # Setup the GDB Controller to connect to the QEMU server
        self.gdbmi = GdbController(["arm-rtems5-gdb", "--nx", "--quiet", "--interpreter=mi3"])

        # Load binary
        print("\n######\n-file-exec-and-symbols build/arm-rtems5-realview_pbx_a9_qemu/rtems/calc.exe\n")
        response = self.gdbmi.write("-file-exec-and-symbols " + file_path)
        self.print_output(response)

        # Connect to the remote host 
        print("\n######\n-target-select remote localhost:1234\n")
        response = self.gdbmi.write("-target-select remote localhost:1234")
        self.print_output(response)

        # Create the watchpoint on the flag to know when to modify Input
        print("\n######\n-break-watch flag\n")
        response = self.gdbmi.write("-break-watch flag")
        watchpoint_flag = response[0]['payload']['wpt']['number']
        self.print_output(response)
        print("Watchpoint #: " + str(response[0]['payload']['wpt']['number']))
        pprint(response)

        # Get the memory addresses of the relevant variables (input and flag to restart the Calculator)
        self.addr_of_input = self.get_addr_of_var(self.gdbmi, "input")
        self.addr_of_flag = self.get_addr_of_var(self.gdbmi, "flag")
        print(self.addr_of_input)
        print(self.addr_of_flag)
        

    def close_Streams(self):
        """Teardown method to ensure QEMU is quit and not left as a zombie process. Close STDIN stream.
        """
        try:
            if self.process.poll() is None:
                self.press_button("q")
                self.process.stdin.close()
        except:
            print("Unexpected error:", sys.exc_info()[0])   

    def press_button(self, value):
        """Enters the value or operator, passed in, to the calculator.

        Examples:
        | Press Button | 1 |
        | Press Button | + |
        """

        # Execute GDB commands to place input into memory and start the Calculator executing
        print("Set Input")
        self.set_input(self.gdbmi, self.addr_of_input, self.addr_of_flag, ord(value))
    
        print("Continue")
        self.response = self.gdbmi.write("-exec-continue")
        print(self.response)
        # Check if command errors
        self.is_error(self.response)
        
        # TODO Do we need to check this output to see if we got to a watchpoint? Or do this before button and run more exec-continues until getting there?

        # Use the following to print the Input Value lines to the console for logging purposes
        wait_for_prompt = True
        while wait_for_prompt:
            output = self.process.stdout.readline()

            if self.prompt in output:
                print(output.strip())
                #output = self.process.stdout.readline()
                #print(output.strip())
                wait_for_prompt = False
            else:
                print(output.strip())
                return_code = self.process.poll()
                if return_code is not None:
                    break

    def press_buttons(self, values):
        """Enters multiple button presses. passed in, using the `Press Button` method

        Examples:
        | Press Buttons | 1+2 |
        | Press Buttons | 1.5 + 2 |
        """
        print("In press_buttons")
        for value in values.replace(' ', ''):
            print("press a button")
            self.press_button(value)

    def result_should_be(self, expected):
        """Verifies that the current prompt_display is ``expected``. It compares the passed value with the value read at the end of the "Display Output: " line.
        
        Example:
        | Result should be | 3 |
        """
        self.response = self.gdbmi.write("print outC.outputDisplay")
        print(self.response)
        self._result = str(self.get_output(self.response))
        #if str(expected) == self._result:
        #    return self._result
        #else:   
        #    raise AssertionError('%s != %s' % (self._result, expected))
        #TODO Check for invalid input

        wait_for_prompt = True
        while wait_for_prompt:
            output = self.process.stdout.readline()

            if self.prompt_display in output:
                print(output.strip())
                # Parse output on spaces to get final entry in line
                #output_parsed = output.split()
                # Get last element in list and remove "." from end
                #self._result = str(output_parsed[-1])
                # Compare if the value is as expected, if not raise an error
                if str(expected) == self._result:
                    return self._result
                else:   
                    raise AssertionError('%s != %s' % (self._result, expected))
            # Check for Invalid Input error
            elif self.bad_input in output:
                print(output.strip())
                raise AssertionError('Bad Input')
            else:
                print(output.strip())

    def should_cause_error(self, expression):
        """Verifies that calculating the given ``expression`` causes an error.

        Example:
        | Should cause error | p |
        This would return ``Invalid Input``
        """
        try:
            print("Push Buttons")
            self.press_buttons(expression)
            print("Pushed Buttons")
            # Check if it accepts the input and shows prompt display or Errors out 
            #self.result_should_be(prompt_display)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            return str("Invalid Input")
        else:
            raise AssertionError("'%s' should have caused an error."
                                 % expression)

    def print_output(self, output):
        """
        This function prints all values for the "message" field in the response structure

        Parameters:
        arg1 (list of dicts): Response structure returned from GDBMI response
        """
        for i in output:
            print("Message: " + str(i['message']))

    def get_addr_of_var(self, _gdbmi, variable):
        """
        This returns the memory address of a variable passed in. This assumes the variable is in scope 
        at the time of execution

        Parameters: Variable name to get the address of

        Returns: String of the memory address
        """
        _response = _gdbmi.write("print &" + variable)
        output = self.get_payloads(_response)
        output = output.split("=",1)[1].split()
        output = [i for i in output if i.startswith('0x')]
        return output[0]

    def get_payloads(self, _response):
        """
        Iterate through response and pull all of the "none" payloads out

        It seems the "none" payloads contain a lot of the information after a watch-point is hit.
        """
        retr_val = ""
        for i in _response:
            if str(i['message']) == "None":
                retr_val += i['payload']
        return retr_val

    def set_input(self, _gdbmi, _addr_of_input, _addr_of_flag, value):
        """
        This will set the variable input to the value passed and set the flag to 0 to release the Calculator
        """
        print("\n######\nset Input (hardcoded address)\n")
        response = _gdbmi.write("-gdb-set *((char*) " + str(_addr_of_input) + ") = " + str(value))
        self.is_error(response)
        pprint(response)
        print("\n######\nprint input\n")
        response = _gdbmi.write("print input")
        self.is_error(response)
        pprint(response)

        # Set flag to 0 to indicate Calculator can continue
        response = _gdbmi.write("-gdb-set *((_Bool *) " + str(_addr_of_flag) + ") = 0")
        self.is_error(response)
        pprint(response)

    def get_output(self, _response):
        """This will extract the outC.outputDisplay value from a GDB response that called "print outC.outputDisplay"
        """
        output = self.get_payloads(_response).split('\\')
        output = [i for i in output if i.startswith('"')]
        return output[0][1:]

    def is_error(self, _response):
        """Determines if there is an error in the response. Returns True if there was an error
        """
        for i in _response:
            if str(i['message']) == "error":
                raise AssertionError('Error in GDB Response')
