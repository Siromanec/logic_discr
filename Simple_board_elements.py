"""
these are simple board elements
['AND_Gate', 'NAND_Gate', 'OR_Gate', 'NOR_Gate',
 'XOR_Gate', 'XNOR_Gate', 'NOT_Gate',
 'ZERO_Generator', 'ONE_Generator', 'Lamp', 'Switch',
 'ClockGenerator']

"""
from Fundamentals import BaseCircuitElement
from PIL import Image, ImageTk
import time
import threading


class AND_Gate(BaseCircuitElement):
    """
    The AND logic gate
    """

    def __init__(self, board, i_number=2, o_number=1) -> None:
        super().__init__(board, i_number, o_number)
        # self.img = ImageTk.PhotoImage(Image.open("visuals/and.png").resize((100, 50)))

    def operation(self):
        """
        Performs AND operation on all inputs
        ┌─┬─┬───────┐
        |x|y|x and y|
        ├─┼─┼───────┤
        |0|0|   0   |
        ├─┼─┼───────┤
        |0|1|   0   |
        ├─┼─┼───────┤
        |1|0|   0   |
        ├─┼─┼───────┤
        |1|1|   1   |
        └─┴─┴───────┘
        """
        bools = tuple(i_pin.get_state() for i_pin in self.get_inputs())

        val_prev = bools[0]

        for val in bools[1:]:
            val_prev = val and val_prev
        for o_pin in self.get_outputs():
            o_pin.update_state(val_prev)


class NAND_Gate(BaseCircuitElement):
    """
    The NAND logic gate
    """

    def __init__(self, board, i_number=2, o_number=1) -> None:
        super().__init__(board, i_number, o_number)
        # self.img = ImageTk.PhotoImage(Image.open("visuals/nand.png").resize((100, 50)))

    def operation(self):
        """
        Performs NAND operation on all inputs
        ┌─┬─┬────────┐
        |x|y|x nand y|
        ├─┼─┼────────┤
        |0|0|   1    |
        ├─┼─┼────────┤
        |0|1|   1    |
        ├─┼─┼────────┤
        |1|0|   1    |
        ├─┼─┼────────┤
        |1|1|   0    |
        └─┴─┴────────┘
        """
        bools = tuple(i_pin.get_state() for i_pin in self.get_inputs())

        val_prev = bools[0]

        for val in bools[1:]:
            val_prev = val and val_prev
        for o_pin in self.get_outputs():
            o_pin.update_state(not val_prev)


class OR_Gate(BaseCircuitElement):
    """
    The OR logic gate
    """

    def __init__(self, board, i_number=2, o_number=1) -> None:
        super().__init__(board, i_number, o_number)
        # self.img = ImageTk.PhotoImage(Image.open("visuals/or.png").resize((100, 50)))

    def operation(self):
        bools = tuple(i_pin.get_state() for i_pin in self.get_inputs())
        """
        Performs OR operation on all inputs
        ┌─┬─┬──────┐
        |x|y|x or y|
        ├─┼─┼──────┤
        |0|0|  0   |
        ├─┼─┼──────┤
        |0|1|  1   |
        ├─┼─┼──────┤
        |1|0|  1   |
        ├─┼─┼──────┤
        |1|1|  1   |
        └─┴─┴──────┘
        """
        val_prev = bools[0]

        for val in bools[1:]:
            val_prev = val or val_prev
        for o_pin in self.get_outputs():
            o_pin.update_state(val_prev)


class NOR_Gate(BaseCircuitElement):
    """
    The NOR logic gate
    """

    def __init__(self, board, i_number=2, o_number=1) -> None:
        super().__init__(board, i_number, o_number)
        # self.img = ImageTk.PhotoImage(Image.open("visuals/nor.png").resize((100, 50)))

    def operation(self):
        """
        Performs NOR operation on all inputs
        ┌─┬─┬───────┐
        |x|y|x nor y|
        ├─┼─┼───────┤
        |0|0|   1   |
        ├─┼─┼───────┤
        |0|1|   0   |
        ├─┼─┼───────┤
        |1|0|   0   |
        ├─┼─┼───────┤
        |1|1|   0   |
        └─┴─┴───────┘
        """
        bools = tuple(i_pin.get_state() for i_pin in self.get_inputs())

        val_prev = bools[0]

        for val in bools[1:]:
            val_prev = val or val_prev
        for o_pin in self.get_outputs():
            o_pin.update_state(not val_prev)


class XOR_Gate(BaseCircuitElement):
    """
    The XOR logic gate
    """

    def __init__(self, board) -> None:
        super().__init__(board, 2, 1)
        # self.img = ImageTk.PhotoImage(Image.open("visuals/xor.png").resize((100, 50)))

    def operation(self):
        """
        Performs XOR operation on all inputs
        ┌─┬─┬───────┐
        |x|y|x xor y|
        ├─┼─┼───────┤
        |0|0|   0   |
        ├─┼─┼───────┤
        |0|1|   1   |
        ├─┼─┼───────┤
        |1|0|   1   |
        ├─┼─┼───────┤
        |1|1|   0   |
        └─┴─┴───────┘
        """
        # if self.input_pins[0].signal is not None and self.input_pins[1].signal is not None:
        #     self.output_pins[0].change_signal(self.input_pins[0].father.signal ^ self.input_pins[1].father.signal)
        bools = tuple(i_pin.get_state() for i_pin in self.get_inputs())

        val_prev = bools[0]

        for val in bools[1:]:
            val_prev = val ^ val_prev
        for o_pin in self.get_outputs():
            o_pin.update_state(val_prev)


class XNOR_Gate(BaseCircuitElement):
    """
    The XNOR logic gate
    """

    def __init__(self, board) -> None:
        super().__init__(board, 2, 1)
        # self.img = ImageTk.PhotoImage(Image.open("visuals/xnor.png").resize((100, 50)))

    def operation(self):
        """
        Performs XNOR operation on all inputs
        ┌─┬─┬────────┐
        |x|y|x xnor y|
        ├─┼─┼────────┤
        |0|0|   1    |
        ├─┼─┼────────┤
        |0|1|   0    |
        ├─┼─┼────────┤
        |1|0|   0    |
        ├─┼─┼────────┤
        |1|1|   1    |
        └─┴─┴────────┘
        """
        bools = tuple(i_pin.get_state() for i_pin in self.get_inputs())

        val_prev = bools[0]

        for val in bools[1:]:
            val_prev = val ^ val_prev
        for o_pin in self.get_outputs():
            o_pin.update_state(not val_prev)


class NOT_Gate(BaseCircuitElement):
    """
    The NOT logic gate
    """

    def __init__(self, board) -> None:
        super().__init__(board, 1, 1)
        # self.img = ImageTk.PhotoImage(Image.open("not.png").resize((100, 50)))
        self.set_reaction_areas_for_pins()

    def operation(self):
        """
        Performs NOT operation on input
        ┌─┬─────┐
        |x|not x|
        ├─┼─────┤
        |0|  1  |
        ├─┼─────┤
        |1|  0  |
        └─┴─────┘
        """
        bools = tuple(i_pin.get_state() for i_pin in self.get_inputs())

        val_prev = bools[0]

        for o_pin in self.get_outputs():
            o_pin.update_state(not val_prev)

    def set_reaction_areas_for_pins(self):
        """Set reaction areas for all pins"""
        self.get_inputs()[0].set_reaction_area(-48, -5, -40, 5)
        self.get_outputs()[0].set_reaction_area(40, -5, 48, 5)


class ZERO_Generator(BaseCircuitElement):
    """
    The ZERO signal generator
    """

    def __init__(self, board, o_number=1) -> None:
        super().__init__(board, 0, o_number)
        # self.img = ImageTk.PhotoImage(Image.open("visuals/low_constant.png").resize((100, 50)))

    def operation(self):
        """
        Sends zero on all pins
        """
        for o_pin in self.get_outputs():
            o_pin.update_state(False)


class ONE_Generator(BaseCircuitElement):
    """
    The ONE signal generator
    """

    def __init__(self, board, o_number=1) -> None:
        super().__init__(board, 0, o_number)
        # self.img = ImageTk.PhotoImage(Image.open("visuals/high_constant.png").resize((100, 50)))

    def operation(self):
        """
        Sends one on all pins
        """
        for o_pin in self.get_outputs():
            o_pin.update_state(True)


class Lamp(BaseCircuitElement):
    """Toy implementation of a lamp"""
    all_lamp_images = []

    def __init__(self, board) -> None:
        super().__init__(board, 1, 0)
        # self.img = ImageTk.PhotoImage(Image.open("visuals/light_bulb.png").resize((50, 100)))
        self.set_reaction_areas_for_pins()

    def operation(self):
        """
        shines if the signal is 1 (True)
        """
        bools = tuple(i_pin.get_state() for i_pin in self.get_inputs())

        val_prev = bools[0]

        if val_prev:
            print("shine")
        else:
            print("not shine")
    
    def set_reaction_areas_for_pins(self):
        """Set reaction areas for all pins"""
        self.get_inputs()[0].set_reaction_area(-4, 26, 4, 35)


class Switch(BaseCircuitElement):
    """The Switch - can change generated signal"""
    def __init__(self, board, o_number=1) -> None:
        super().__init__(board, 0, o_number)
        self.state = False
        img1 = "image 1"
        img2 = "image 2"
        self.images = {True: img1, False: img2}
        # self.img = self.images[self.state]

    def operation(self):
        """Generates either ZERO or ONE, depending on the state"""
        for o_pin in self.get_outputs():
            o_pin.update_state(self.state)

    def switch(self):
        """Activates by the click on the Switch element area"""
        self.state = not self.state
        # self.img = self.images[self.state]
        self.get_board().update_board()


class ClockGenerator(BaseCircuitElement):
    """The clock generator - generates clock pulses of a defined frequency"""

    def __init__(self, board, o_number=1, frequency=1) -> None:
        super().__init__(board, 0, o_number)
        self.time_interval = 1 / frequency
        self.state = True
        self.exists = True
        # # self.img =
        gen = threading.Thread(target=self.generation, args=())
        gen.start()

    def generation(self):
        """Generates either ZERO or ONE each time period, depending on the state"""
        while self.exists:
            time.sleep(self.time_interval)
            print(self.state)
            for o_pin in self.get_outputs():
                o_pin.update_state(self.state)
            self.get_board().update_board()
            self.state = not self.state

    def destroy(self):
        """Activates by the click on the Switch element area"""
        self.exists = False
