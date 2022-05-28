from Fundamentals import BaseCircuitElement, Board


class ANDGate(BaseCircuitElement):
    def __init__(self, board, i_number=2, o_number=1) -> None:
        super().__init__(board, i_number, o_number)

    def operation(self):
        for i_pin in self.get_inputs():
            if i_pin.get_state is False:
                for o_pin in self.get_outputs():
                    o_pin.update_state(False)
                return
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

class XOR_Gate(BaseCircuitElement):
    def __init__(self) -> None:
        super().__init__(2, 1)
    def operation(self):
        if self.input_pins[0].signal is not None and self.input_pins[1].signal is not None:
            self.output_pins[0].change_signal(self.input_pins[0].father.signal ^ self.input_pins[1].father.signal)

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


def main():
    board = Board()

    one1 = board.create_element(ONEGenerator)
    one2 = board.create_element(ONEGenerator)
    zero = board.create_element(ZEROGenerator)
    and_gate = board.create_element(ANDGate)
    lamp = board.create_element(Lamp)

    try:
        board.connect_pins(one1.get_outputs()[0], and_gate.get_inputs()[0])
    except Exception as e:
        pass
    try:
        board.connect_pins(one2.get_outputs()[0], and_gate.get_inputs()[1])
    except Exception as e:
        pass

    board.connect_pins(and_gate.get_outputs()[0], lamp.get_inputs()[0])

    # board.update_board()

if __name__ == '__main__':
    main()
