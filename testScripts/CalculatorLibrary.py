import shlex
import subprocess

class CalculatorLibrary(object):
    """Library for testing the Ansys *Calculator* App running in QEMU.

    This library interacts with the Console running QEMU to provide input, "Press Buttons" and read output to verify functionality.
    """
    prompt = "Press Button"
    prompt_display = "Display Output"
    bad_input = "Invalid Input"

    def __init__(self):
        """Method run at instantiation of Python object, simply initializes results to ''
        """
        self._result = ''


    def start_process(self):
        """Setup method to start QEMU process.
        """
        qemu_cmd = shlex.split("qemu-system-arm -net none -no-reboot -nographic -monitor none -serial stdio -M realview-pbx-a9 -m 256M -kernel calc.exe")
        self.process= subprocess.Popen(qemu_cmd,
                        stdin =subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True,
                        bufsize=0)
        self._result = ''

    def close_Streams(self):
        """Teardown method to ensure QEMU is quit and not left as a zombie process. Close STDIN stream.
        """
        self.press_button("q")
        self.process.stdin.close()

    def press_button(self, value):
        """Enters the value or operator, passed in, to the calculator.

        Examples:
        | Press Button | 1 |
        | Press Button | + |
        """
        wait_for_prompt = True
        while wait_for_prompt:
            output = self.process.stdout.readline()

            if self.prompt in output:
                print(output.strip())
                self.process.stdin.write(value + "\n")
                output = self.process.stdout.readline()
                print(output.strip())
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
        for value in values.replace(' ', ''):
            self.press_button(value)

    def result_should_be(self, expected):
        """Verifies that the current prompt_display is ``expected``. It compares the passed value with the value read at the end of the "Display Output: " line.
        
        Example:
        | Result should be | 3 |
        """
        wait_for_prompt = True
        while wait_for_prompt:
            output = self.process.stdout.readline()

            if self.prompt_display in output:
                print(output.strip())
                # Parse output on spaces to get final entry in line
                output_parsed = output.split()
                # Get last element in list and remove "." from end
                self._result = str(output_parsed[-1])
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

    def get_display(self):
        """Gets the value most recently output as the Display value from the Calculator. If this is run, then the "result_should_be" cannot be run after this.
        
        Example:
        | Get Display |
        """
        wait_for_prompt = True
        while wait_for_prompt:
            output = self.process.stdout.readline()

            if self.prompt_display in output:
                print(output.strip())
                # Parse output on spaces to get final entry in line
                output_parsed = output.split()
                # Get last element in list and remove "." from end
                self._result = str(output_parsed[-1])
		return self._result
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
            self.push_buttons(expression)
            # Check if it accepts the input and shows prompt display or Errors out 
            self.result_should_be(prompt_display)
        except:
            return str("Invalid Input")
        else:
            raise AssertionError("'%s' should have caused an error."
                                 % expression)
