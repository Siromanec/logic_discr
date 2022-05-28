from Fundamentals import BaseCircuitElement, Board, OutputPin, InputPin


class AND_Gate(BaseCircuitElement):
    def __init__(self, board, i_number=2, o_number=1) -> None:
        super().__init__(board, i_number, o_number)

    def operation(self):


        bools = tuple(i_pin.get_state() for i_pin in self.get_inputs())

        val_prev = bools[0]

        for val in bools[1:]:
            val_prev = val and val_prev
        for o_pin in self.get_outputs():
            o_pin.update_state(val_prev)


class NAND_Gate(BaseCircuitElement):

    def __init__(self, board, i_number=2, o_number=1) -> None:
        super().__init__(board, i_number, o_number)
    def operation(self):



        bools = tuple(i_pin.get_state() for i_pin in self.get_inputs())

        val_prev = bools[0]

        for val in bools[1:]:
            val_prev = val and val_prev
        for o_pin in self.get_outputs():
            o_pin.update_state(not val_prev)


class OR_Gate(BaseCircuitElement):
    def __init__(self, board) -> None:
        super().__init__(board, 2, 1)
    def operation(self):
        bools = tuple(i_pin.get_state() for i_pin in self.get_inputs())

        val_prev = bools[0]

        for val in bools[1:]:
            val_prev = val or val_prev
        for o_pin in self.get_outputs():
            o_pin.update_state(val_prev)


class NOR_Gate(BaseCircuitElement):
    def __init__(self, board) -> None:
        super().__init__(board, 2, 1)
    def operation(self):
        bools = tuple(i_pin.get_state() for i_pin in self.get_inputs())

        val_prev = bools[0]

        for val in bools[1:]:
            val_prev = val or val_prev
        for o_pin in self.get_outputs():
            o_pin.update_state(not val_prev)


class XOR_Gate(BaseCircuitElement):
    def __init__(self, board) -> None:
        super().__init__(board, 2, 1)
    def operation(self):
        # if self.input_pins[0].signal is not None and self.input_pins[1].signal is not None:
        #     self.output_pins[0].change_signal(self.input_pins[0].father.signal ^ self.input_pins[1].father.signal)
        bools = tuple(i_pin.get_state() for i_pin in self.get_inputs())

        val_prev = bools[0]

        for val in bools[1:]:
            val_prev = val ^ val_prev
        for o_pin in self.get_outputs():
            o_pin.update_state(val_prev)


class XNOR_Gate(BaseCircuitElement):
    def __init__(self, board) -> None:
        super().__init__(board, 2, 1)
    def operation(self):
        # if self.input_pins[0].signal is not None and self.input_pins[1].signal is not None:
        #     self.output_pins[0].change_signal(not (self.input_pins[0].father.signal ^ self.input_pins[1].father.signal))
        bools = tuple(i_pin.get_state() for i_pin in self.get_inputs())

        val_prev = bools[0]

        for val in bools[1:]:
            val_prev = val ^ val_prev
        for o_pin in self.get_outputs():
            o_pin.update_state(not val_prev)


class NOT_Gate(BaseCircuitElement):
    def __init__(self, board) -> None:
        super().__init__(board, 2, 1) 
    def operation(self):
        bools = tuple(i_pin.get_state() for i_pin in self.get_inputs())

        val_prev = bools[0]

        for o_pin in self.get_outputs():
            o_pin.update_state(not val_prev)


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
        if sum([0 if i_pin.get_state() else 1 for i_pin in self.get_inputs()]) == 0: # is this ANDGate 2.0?
            print("shine")
        else:
            print('not shine')
