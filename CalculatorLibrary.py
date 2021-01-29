#from calculator import Calculator, CalculationError
import shlex
import subprocess

class CalculatorLibrary(object):
    """Test library for testing *Calculator* business logic.

    Interacts with the calculator directly using its ``push`` method.
    """
    prompt = "Press Button"
    prompt_display = "Display Output"
    bad_input = "Invalid Input"

    def __init__(self):
        qemu_cmd = shlex.split("qemu-system-arm -net none -no-reboot -nographic -monitor none -serial stdio -M realview-pbx-a9 -m 256M -kernel build/arm-rtems5-realview_pbx_a9_qemu/rtems/calc.exe")
        self.process= subprocess.Popen(qemu_cmd,
                        stdin =subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        universal_newlines=True,
                        bufsize=0)
        self._result = ''


    def press_button(self, value):
        """Enters the value to be operated on in the calculator"""
        wait_for_prompt = True
        while wait_for_prompt:
            output = self.process.stdout.readline()

            if self.prompt in output:
                print(output.strip())
                self.process.stdin.write(value + "\n")
                wait_for_prompt = False
            else:
                print(output.strip())
                return_code = self.process.poll()
                if return_code is not None:
                    break

    def press_buttons(self, values):
        for value in values.replace(' ', ''):
            self.press_button(value)

    def result_should_be(self, expected):
        """Verifies that the current prompt_display is ``expected``.
        """
        self.process.stdin.close()
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
            else:
                print(output.strip())


# TODO to update
    def should_cause_error(self, expression):
        """Verifies that calculating the given ``expression`` causes an error.

        The error message is returned and can be verified using, for example,
        `Should Be Equal` or other keywords in `BuiltIn` library.

        Examples:
        | Should Cause Error | invalid            |                   |
        | ${error} =         | Should Cause Error | 1 / 0             |
        | Should Be Equal    | ${error}           | Division by zero. |
        """
        try:
            self.push_buttons(expression)
        except CalculationError as err:
            return str(err)
        else:
            raise AssertionError("'%s' should have caused an error."
                                 % expression)
