import shlex
import subprocess

class CalculatorLibrary(object):
    """Test library for testing *Calculator* App.
    """
    prompt = "Press Button"
    prompt_display = "Display Output"
    bad_input = "Invalid Input"

    def __init__(self):
        """Method run at instantiation of Python object.
        """
        self._result = ''


    def start_process(self):
        """Setup method to start QEMU process. Could use ___init___ in this case, but testing Setup test case function
        """
        qemu_cmd = shlex.split("qemu-system-arm -net none -no-reboot -nographic -monitor none -serial stdio -M realview-pbx-a9 -m 256M -kernel build/arm-rtems5-realview_pbx_a9_qemu/rtems/calc.exe")
        self.process= subprocess.Popen(qemu_cmd,
                        stdin =subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True,
                        bufsize=0)
        self._result = ''

    def close_Streams(self):
        """Ensure QEMU is quit and not left as a zombie process. Close STDIN sream
        """
        self.press_button("q")
        self.process.stdin.close()

    def press_button(self, value):
        """Enters the value or operator to the calculator"""
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
        """Enters multiple button presses using the press_button method
        """
        for value in values.replace(' ', ''):
            self.press_button(value)

    def result_should_be(self, expected):
        """Verifies that the current prompt_display is ``expected``.
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
                if expected == self._result:
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
