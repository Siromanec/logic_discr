from Fundamentals import BaseCircuitElement, Board, OutputPin, InputPin


class ANDGate(BaseCircuitElement):
    def __init__(self, board, i_number=2, o_number=1) -> None:
        super().__init__(board, i_number, o_number)

    def operation(self):
        for i_pin in self.get_inputs():
            if i_pin.get_state() is False:
                for o_pin in self.get_outputs():
                    o_pin.update_state(False)
                return
        for o_pin in self.get_outputs():
            o_pin.update_state(True)


class XORGate(BaseCircuitElement):
    def __init__(self, board, i_number=2, o_number=1) -> None:
        super().__init__(board, i_number, o_number)

    def operation(self):
        # xor gate with more than two inputs is ambiguous, so it is hardcoded here
        inputs = self.get_inputs()
        if inputs[0].get_state() != inputs[1].get_state():
            for o_pin in self.get_outputs():
                o_pin.update_state(True)

"""class NAND_Gate(BaseCircuitElement):
    def __init__(self, board, i_number=2, o_number=1) -> None:
        super().__init__(board, i_number, o_number)
    def operation(self):
        if self.input_pins[0].signal is not None and self.input_pins[1].signal is not None:
            self.output_pins[0].change_signal(not (self.input_pins[0].father.signal and self.input_pins[1].father.signal))

class OR_Gate(BaseCircuitElement):
    def __init__(self) -> None:
        super().__init__(2, 1)
    def operation(self):
        if self.input_pins[0].signal is not None and self.input_pins[1].signal is not None:
            self.output_pins[0].change_signal(self.input_pins[0].father.signal or self.input_pins[1].father.signal)

class NOR_Gate(BaseCircuitElement):
    def __init__(self) -> None:
        super().__init__(2, 1)
    def operation(self):
        if self.input_pins[0].signal is not None and self.input_pins[1].signal is not None:
            self.output_pins[0].change_signal(not (self.input_pins[0].father.signal or self.input_pins[1].father.signal))



class XNOR_Gate(BaseCircuitElement):
    def __init__(self) -> None:
        super().__init__(2, 1)
    def operation(self):
        if self.input_pins[0].signal is not None and self.input_pins[1].signal is not None:
            self.output_pins[0].change_signal(not (self.input_pins[0].father.signal ^ self.input_pins[1].father.signal))

class NOT_Gate(BaseCircuitElement):
    def __init__(self) -> None:
        super().__init__(1, 1)
    def operation(self):
        if self.input_pins[0].signal is not None:
            self.output_pins[0].change_signal(not self.input_pins[0].father.signal)
"""


class ZEROGenerator(BaseCircuitElement):
    def __init__(self, board, i_number=0, o_number=1) -> None:
        super().__init__(board, i_number, o_number)

    def operation(self):
        for o_pin in self.get_outputs():
            o_pin.update_state(False)


class ONEGenerator(BaseCircuitElement):
    def __init__(self, board, i_number=0, o_number=1) -> None:
        super().__init__(board, i_number, o_number)

    def operation(self):
        for o_pin in self.get_outputs():
            o_pin.update_state(True)


class Lamp(BaseCircuitElement):
    def __init__(self, board, i_number=1, o_number=0) -> None:
        super().__init__(board, i_number, o_number)

    def operation(self):
        if sum([0 if i_pin.get_state() is True else 1 for i_pin in self.get_inputs()]) == 0:
            print("shine")
        else:
            print('not shine')


