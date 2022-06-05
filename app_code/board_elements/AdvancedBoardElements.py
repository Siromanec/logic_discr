"""
[AdvancedCircuitElement, HalfAdder, Adder,
 Decoder, HalfSubstractor, Substractor, Encoder_4_to_2,
 Encoder_8_to_3, ShiftLeft, ShiftRight]
"""
from __future__ import annotations
import os
import sys
import time

root_folder = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(root_folder)

from board_elements.Fundamentals import Board, BaseCircuitElement, InputPin, OutputPin

from board_elements.SimpleBoardElements import (
    AND_Gate,
    OR_Gate,
    XOR_Gate,
    ONE_Generator,
    ZERO_Generator,
    Lamp,
    NOT_Gate,
    NOR_Gate,
    NAND_Gate,
    Switch,
    ClockGenerator,
)


class AdvancedCircuitElement(BaseCircuitElement):
    def __init__(self, board: Board, i_number=1, o_number=1):
        super().__init__(board, i_number, o_number)
        self._elements = []
        self.inner_inputs_dict = {}
        self.inner_outputs_dict = {}

        for o_pin in self.get_outputs():
            i_pin = InputPin(self)
            self.inner_outputs_dict[o_pin] = i_pin
        for i_pin in self.get_inputs():
            o_pin = OutputPin(self)
            self.inner_inputs_dict[i_pin] = o_pin

    def create_element(
        self, circuit_type, inputs=None, outputs=None
    ) -> AdvancedCircuitElement:
        """Creates a circuit of a given type in this circuit"""
        try:
            if not issubclass(circuit_type, BaseCircuitElement):
                raise ValueError("Incorrect circuit type!")
        except TypeError as e:
            raise e

        if inputs is not None and outputs is not None:
            new_circuit = circuit_type(self.get_board(), inputs, outputs)
        elif inputs is not None:
            new_circuit = circuit_type(self.get_board(), inputs)
        elif outputs is not None:
            new_circuit = circuit_type(self.get_board(), outputs)
        else:
            new_circuit = circuit_type(self.get_board())

        self._elements.append(new_circuit)
        return new_circuit

    def get_elements(self) -> list[BaseCircuitElement]:
        return list(self._elements)

    def operation(self):
        def topo_sorted_update():
            circuits = self.get_elements()
            independent_circuits = []
            circuits_dependence = {}
            for circuit in circuits:
                circuits_set = circuit.get_parent_circuits()
                if self in circuits_set:
                    circuits_set.remove(self)
                circuits_dependence[circuit] = len(circuits_set)
                if circuits_dependence[circuit] == 0:
                    independent_circuits.append(circuit)

            while independent_circuits:
                circuit = independent_circuits.pop(0)
                circuit.update()
                for dependent_circuit in circuit.get_dependent_circuits():
                    if dependent_circuit != self:
                        circuits_dependence[dependent_circuit] -= 1
                        if circuits_dependence[dependent_circuit] == 0:
                            independent_circuits.append(dependent_circuit)
                circuits.remove(circuit)
            if circuit:
                for circuit in circuits:
                    circuit.cycle_proccessing()
                self.cycle_processing()

        for i_pin in self.get_inputs():
            self.inner_inputs_dict[i_pin].update_state(i_pin.get_state())

        topo_sorted_update()

        for o_pin in self.get_outputs():
            pin = self.inner_outputs_dict[o_pin]
            pin.update_state()
            o_pin.set_state(pin.get_state())

    def external_inner_convertor(self, input_pin_name):
        return self.inner_inputs_dict[self.input_dict[input_pin_name]]

    def inner_external_convertor(self, output_pin_name):
        return self.inner_outputs_dict[self.output_dict[output_pin_name]]


class HalfAdder(AdvancedCircuitElement):
    """
    Input pins:
        0: A
        1: B
    Output pins:
        0: sum
        1: carry
    """

    def __init__(self, board: Board, i_number=2, o_number=2):
        super().__init__(board, i_number, o_number)
        inputs = self.get_inputs()
        outputs = self.get_outputs()
        self.input_dict = {"A": inputs[0], "B": inputs[1]}
        self.output_dict = {"Sum": outputs[0], "Carry": outputs[1]}

        self.xor1 = self.create_element(XOR_Gate)
        self.and1 = self.create_element(AND_Gate)

        board.connect_pins(
            self.external_inner_convertor("A"), self.xor1.get_inputs()[0], update=False
        )
        board.connect_pins(
            self.external_inner_convertor("B"), self.xor1.get_inputs()[1], update=False
        )
        board.connect_pins(
            self.external_inner_convertor("A"), self.and1.get_inputs()[0], update=False
        )
        board.connect_pins(
            self.external_inner_convertor("B"), self.and1.get_inputs()[1], update=False
        )
        board.connect_pins(
            self.xor1.get_outputs()[0],
            self.inner_external_convertor("Sum"),
            update=False,
        )
        board.connect_pins(
            self.and1.get_outputs()[0],
            self.inner_external_convertor("Carry"),
            update=False,
        )

        self.get_board().update_board()


class Adder(AdvancedCircuitElement):
    """
    Input pins:
        0: A
        1: B
        2: Carry in
    Output pins:
        0: sum
        1: carry out
    """

    def __init__(self, board: Board, i_number=3, o_number=2):
        super().__init__(board, i_number, o_number)
        inputs = self.get_inputs()
        outputs = self.get_outputs()
        self.input_dict = {"A": inputs[0], "B": inputs[1], "Carry in": inputs[2]}
        self.output_dict = {"Sum": outputs[0], "Carry out": outputs[1]}

        self.half_adder_1 = self.create_element(HalfAdder)
        self.half_adder_2 = self.create_element(HalfAdder)
        self.or_1 = self.create_element(OR_Gate)

        board.connect_pins(
            self.external_inner_convertor("A"),
            self.half_adder_1.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("B"),
            self.half_adder_1.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.half_adder_1.get_outputs()[1], self.or_1.get_inputs()[0], update=False
        )
        board.connect_pins(
            self.half_adder_1.get_outputs()[0],
            self.half_adder_2.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Carry in"),
            self.half_adder_2.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.half_adder_2.get_outputs()[1], self.or_1.get_inputs()[1], update=False
        )
        board.connect_pins(
            self.half_adder_2.get_outputs()[0],
            self.inner_external_convertor("Sum"),
            update=False,
        )
        board.connect_pins(
            self.or_1.get_outputs()[0],
            self.inner_external_convertor("Carry out"),
            update=False,
        )

        self.get_board().update_board()


class Decoder(AdvancedCircuitElement):
    """
    A class for Decoder.
    Input pins:
        0: A
        1: B
        2: C
    Output pins:
        0: 07
        1: 06
        2: 05
        3: 04
        4: 03
        5: 02
        6: 01
        7: 00
    """

    def __init__(self, board: Board, i_number=3, o_number=8):
        super().__init__(board, i_number, o_number)
        inputs = self.get_inputs()
        outputs = self.get_outputs()
        self.input_dict = {"A": inputs[0], "B": inputs[1], "C": inputs[2]}
        self.output_dict = {
            "O7": outputs[0],
            "O6": outputs[1],
            "O5": outputs[2],
            "O4": outputs[3],
            "O3": outputs[4],
            "O2": outputs[5],
            "O1": outputs[6],
            "O0": outputs[7],
        }
        self.not1 = self.create_element(NOT_Gate)
        self.not2 = self.create_element(NOT_Gate)
        self.not3 = self.create_element(NOT_Gate)
        self.and0 = self.create_element(AND_Gate, 3)
        self.and1 = self.create_element(AND_Gate, 3)
        self.and2 = self.create_element(AND_Gate, 3)
        self.and3 = self.create_element(AND_Gate, 3)
        self.and4 = self.create_element(AND_Gate, 3)
        self.and5 = self.create_element(AND_Gate, 3)
        self.and6 = self.create_element(AND_Gate, 3)
        self.and7 = self.create_element(AND_Gate, 3)

        board.connect_pins(
            self.external_inner_convertor("A"), self.not1.get_inputs()[0], update=False
        )
        board.connect_pins(
            self.not1.get_outputs()[0], self.and0.get_inputs()[0], update=False
        )
        board.connect_pins(
            self.not1.get_outputs()[0], self.and2.get_inputs()[0], update=False
        )
        board.connect_pins(
            self.not1.get_outputs()[0], self.and4.get_inputs()[0], update=False
        )
        board.connect_pins(
            self.not1.get_outputs()[0], self.and6.get_inputs()[0], update=False
        )

        board.connect_pins(
            self.external_inner_convertor("A"), self.and1.get_inputs()[0], update=False
        )
        board.connect_pins(
            self.external_inner_convertor("A"), self.and3.get_inputs()[0], update=False
        )
        board.connect_pins(
            self.external_inner_convertor("A"), self.and5.get_inputs()[0], update=False
        )
        board.connect_pins(
            self.external_inner_convertor("A"), self.and7.get_inputs()[0], update=False
        )

        board.connect_pins(
            self.external_inner_convertor("B"), self.not2.get_inputs()[0], update=False
        )
        board.connect_pins(
            self.not2.get_outputs()[0], self.and0.get_inputs()[1], update=False
        )
        board.connect_pins(
            self.not2.get_outputs()[0], self.and1.get_inputs()[1], update=False
        )
        board.connect_pins(
            self.not2.get_outputs()[0], self.and4.get_inputs()[1], update=False
        )
        board.connect_pins(
            self.not2.get_outputs()[0], self.and5.get_inputs()[1], update=False
        )

        board.connect_pins(
            self.external_inner_convertor("B"), self.and2.get_inputs()[1], update=False
        )
        board.connect_pins(
            self.external_inner_convertor("B"), self.and3.get_inputs()[1], update=False
        )
        board.connect_pins(
            self.external_inner_convertor("B"), self.and6.get_inputs()[1], update=False
        )
        board.connect_pins(
            self.external_inner_convertor("B"), self.and7.get_inputs()[1], update=False
        )

        board.connect_pins(
            self.external_inner_convertor("C"), self.not3.get_inputs()[0], update=False
        )
        board.connect_pins(
            self.not3.get_outputs()[0], self.and0.get_inputs()[2], update=False
        )
        board.connect_pins(
            self.not3.get_outputs()[0], self.and1.get_inputs()[2], update=False
        )
        board.connect_pins(
            self.not3.get_outputs()[0], self.and2.get_inputs()[2], update=False
        )
        board.connect_pins(
            self.not3.get_outputs()[0], self.and3.get_inputs()[2], update=False
        )

        board.connect_pins(
            self.external_inner_convertor("C"), self.and4.get_inputs()[2], update=False
        )
        board.connect_pins(
            self.external_inner_convertor("C"), self.and5.get_inputs()[2], update=False
        )
        board.connect_pins(
            self.external_inner_convertor("C"), self.and6.get_inputs()[2], update=False
        )
        board.connect_pins(
            self.external_inner_convertor("C"), self.and7.get_inputs()[2], update=False
        )

        board.connect_pins(
            self.and0.get_outputs()[0],
            self.inner_external_convertor("O0"),
            update=False,
        )
        board.connect_pins(
            self.and1.get_outputs()[0],
            self.inner_external_convertor("O1"),
            update=False,
        )
        board.connect_pins(
            self.and2.get_outputs()[0],
            self.inner_external_convertor("O2"),
            update=False,
        )
        board.connect_pins(
            self.and3.get_outputs()[0],
            self.inner_external_convertor("O3"),
            update=False,
        )
        board.connect_pins(
            self.and4.get_outputs()[0],
            self.inner_external_convertor("O4"),
            update=False,
        )
        board.connect_pins(
            self.and5.get_outputs()[0],
            self.inner_external_convertor("O5"),
            update=False,
        )
        board.connect_pins(
            self.and6.get_outputs()[0],
            self.inner_external_convertor("O6"),
            update=False,
        )
        board.connect_pins(
            self.and7.get_outputs()[0],
            self.inner_external_convertor("O7"),
            update=False,
        )

        self.get_board().update_board()
        
        
class Multiplexor(AdvancedCircuitElement):
    """ 
    A class for multiplexor.
    Input pins:
        0: s1
        1: s0
        2: i0
        3: i1
        4: i2
        5: i3
    Output pins:
        0: y
    """
    def __init__(self, board: Board, i_number=6, o_number=1):
        super().__init__(board, i_number, o_number)
        inputs = self.get_inputs()
        outputs = self.get_outputs()
        self.input_dict = {"s1": inputs[0], "s0": inputs[1],
                           "i0": inputs[2], "i1": inputs[3], "i2": inputs[4], "i3": inputs[5]}
        self.output_dict = {"y": outputs[0]}

        self.not1 = self.create_element(NOT_Gate)
        self.not2 = self.create_element(NOT_Gate)
        self.and3 = self.create_element(AND_Gate, 3)
        self.and2 = self.create_element(AND_Gate, 3)
        self.and1 = self.create_element(AND_Gate, 3)
        self.and0 = self.create_element(AND_Gate, 3)
        self.or1 = self.create_element(OR_Gate, 4)

        board.connect_pins(self.external_inner_convertor(
            "s1"), self.and3.get_inputs()[0], update=False)
        board.connect_pins(self.external_inner_convertor(
            "s1"), self.not1.get_inputs()[0], update=False)
        board.connect_pins(self.not1.get_outputs()[
                           0], self.and1.get_inputs()[0], update=False)
        board.connect_pins(self.not1.get_outputs()[
                           0], self.and0.get_inputs()[0], update=False)
        board.connect_pins(self.external_inner_convertor(
            "s1"), self.and2.get_inputs()[0], update=False)
        board.connect_pins(self.external_inner_convertor(
            "s0"), self.and3.get_inputs()[1], update=False)
        board.connect_pins(self.external_inner_convertor(
            "s0"), self.and1.get_inputs()[1], update=False)
        board.connect_pins(self.external_inner_convertor(
            "s0"), self.not2.get_inputs()[0], update=False)
        board.connect_pins(self.not2.get_outputs()[
                           0], self.and2.get_inputs()[1], update=False)
        board.connect_pins(self.not2.get_outputs()[
                           0], self.and0.get_inputs()[1], update=False)
        board.connect_pins(self.external_inner_convertor(
            "i3"), self.and3.get_inputs()[2], update=False)
        board.connect_pins(self.external_inner_convertor(
            "i2"), self.and2.get_inputs()[2], update=False)
        board.connect_pins(self.external_inner_convertor(
            "i1"), self.and1.get_inputs()[2], update=False)
        board.connect_pins(self.external_inner_convertor(
            "i0"), self.and0.get_inputs()[2], update=False)

        board.connect_pins(self.and3.get_outputs()[
                           0], self.or1.get_inputs()[0], update=False)
        board.connect_pins(self.and2.get_outputs()[
                           0], self.or1.get_inputs()[1], update=False)
        board.connect_pins(self.and1.get_outputs()[
                           0], self.or1.get_inputs()[2], update=False)
        board.connect_pins(self.and0.get_outputs()[
                           0], self.or1.get_inputs()[3], update=False)

        board.connect_pins(self.or1.get_outputs()[
                           0], self.inner_external_convertor("y"), update=False)

        self.get_board().update_board()



class HalfSubstractor(AdvancedCircuitElement):
    """
    Input pins:
        0: A
        1: B
    Output pins:
        0: difference
        1: borrow
    """

    def __init__(self, board: Board, i_number=2, o_number=2):
        super().__init__(board, i_number, o_number)
        inputs = self.get_inputs()
        outputs = self.get_outputs()
        self.input_dict = {"A": inputs[0], "B": inputs[1]}
        self.output_dict = {"Diff": outputs[0], "Borrow": outputs[1]}
        self.xor1 = self.create_element(XOR_Gate)
        self.and1 = self.create_element(AND_Gate)
        self.not1 = self.create_element(NOT_Gate)
        board.connect_pins(
            self.external_inner_convertor("A"), self.xor1.get_inputs()[0], update=False
        )
        board.connect_pins(
            self.external_inner_convertor("B"), self.xor1.get_inputs()[1], update=False
        )
        board.connect_pins(
            self.external_inner_convertor("A"), self.not1.get_inputs()[0], update=False
        )
        board.connect_pins(
            self.external_inner_convertor("B"), self.and1.get_inputs()[1], update=False
        )
        board.connect_pins(
            self.not1.get_outputs()[0], self.and1.get_inputs()[0], update=False
        )
        board.connect_pins(
            self.xor1.get_outputs()[0],
            self.inner_external_convertor("Diff"),
            update=False,
        )
        board.connect_pins(
            self.and1.get_outputs()[0],
            self.inner_external_convertor("Borrow"),
            update=False,
        )

        self.get_board().update_board()


class Substractor(AdvancedCircuitElement):
    """
    Input pins:
        0: A
        1: B
        2: borrow in
    Output pins:
        0: difference
        1: borrow out
    """

    def __init__(self, board: Board, i_number=3, o_number=2):
        super().__init__(board, i_number, o_number)
        inputs = self.get_inputs()
        outputs = self.get_outputs()
        self.input_dict = {"A": inputs[0], "B": inputs[1], "Borrow In": inputs[2]}
        self.output_dict = {"Diff": outputs[0], "Borrow Out": outputs[1]}
        self.half_sub1 = self.create_element(HalfSubstractor)
        self.half_sub2 = self.create_element(HalfSubstractor)
        self.or1 = self.create_element(OR_Gate)
        board.connect_pins(
            self.external_inner_convertor("A"),
            self.half_sub1.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("B"),
            self.half_sub1.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.half_sub1.get_outputs()[0],
            self.half_sub2.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Borrow In"),
            self.half_sub2.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.half_sub2.get_outputs()[1], self.or1.get_inputs()[0], update=False
        )
        board.connect_pins(
            self.half_sub1.get_outputs()[1], self.or1.get_inputs()[1], update=False
        )
        board.connect_pins(
            self.half_sub2.get_outputs()[0],
            self.inner_external_convertor("Diff"),
            update=False,
        )
        board.connect_pins(
            self.or1.get_outputs()[0],
            self.inner_external_convertor("Borrow Out"),
            update=False,
        )
        self.get_board().update_board()


class Encoder_4_to_2(AdvancedCircuitElement):
    """
    Priority Encoder 4-to-2 bits
    Input pins:
        0: I4
        1: I3
        2: I2
        3: I1
    Output pins:
        0: O1
        1: O2
        2: Valid
    ┌───────────┬───────┐
    |  inputs   |outputs|
    ├──┬──┬──┬──┼──┬──┬─┤
    |I4|I3|I2|I1|O2|O1|V|
    ├──┼──┼──┼──┼──┼──┼─┤
    |0 |0 |0 |0 |x |x |0|
    ├──┼──┼──┼──┼──┼──┼─┤
    |0 |0 |0 |1 |0 |0 |1|
    ├──┼──┼──┼──┼──┼──┼─┤
    |0 |0 |1 |x |0 |1 |1|
    ├──┼──┼──┼──┼──┼──┼─┤
    |0 |1 |x |x |1 |0 |1|
    ├──┼──┼──┼──┼──┼──┼─┤
    |1 |x |x |x |1 |1 |1|
    └──┴──┴──┴──┴──┴──┴─┘
    I4, I3, I2, I1 - input pins
    O2, O1 - output pins
    V - if encoding is valid
    x - any signal
    """

    def __init__(self, board: Board, i_number=4, o_number=3):

        super().__init__(board, i_number, o_number)
        inputs = self.get_inputs()
        outputs = self.get_outputs()
        self.input_dict = {
            "I4": inputs[0],
            "I3": inputs[1],
            "I2": inputs[2],
            "I1": inputs[3],
        }
        self.output_dict = {"O2": outputs[0], "O1": outputs[1], "Valid": outputs[2]}
        self.or_for_valid_1 = self.create_element(OR_Gate)
        self.or_for_valid_2 = self.create_element(OR_Gate)
        self.or_for_valid_3 = self.create_element(OR_Gate)
        self.or_for_encoder_1 = self.create_element(OR_Gate)
        self.or_for_encoder_2 = self.create_element(OR_Gate)
        self.not_gate = self.create_element(NOT_Gate)
        self.and_gate = self.create_element(AND_Gate)
        board.connect_pins(
            self.external_inner_convertor("I1"),
            self.or_for_valid_1.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I2"),
            self.or_for_valid_1.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I3"),
            self.or_for_valid_2.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.or_for_valid_1.get_outputs()[0],
            self.or_for_valid_2.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I4"),
            self.or_for_valid_3.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.or_for_valid_2.get_outputs()[0],
            self.or_for_valid_3.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.or_for_valid_3.get_outputs()[0],
            self.inner_external_convertor("Valid"),
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I2"),
            self.and_gate.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I3"),
            self.not_gate.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.not_gate.get_outputs()[0], self.and_gate.get_inputs()[1], update=False
        )
        board.connect_pins(
            self.and_gate.get_outputs()[0],
            self.or_for_encoder_1.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I4"),
            self.or_for_encoder_1.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.or_for_encoder_1.get_outputs()[0],
            self.inner_external_convertor("O1"),
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I4"),
            self.or_for_encoder_2.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I3"),
            self.or_for_encoder_2.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.or_for_encoder_2.get_outputs()[0], self.inner_external_convertor("O2")
        )
        self.get_board().update_board()


class Encoder_8_to_3(AdvancedCircuitElement):
    """
    Priority Encoder 8-to-3 bits
    Same logic as in previous encoder 4-to-2 bits
    Input pins:
        0: I8
        1: I7
        2: I6
        3: I5
        4: I4
        5: I3
        6: I2
        7: I1
    Output pins:
        0: O3
        1: O2
        2: O1
        3: Valid
    """

    def __init__(self, board: Board, i_number=8, o_number=4):

        super().__init__(board, i_number, o_number)
        inputs = self.get_inputs()
        outputs = self.get_outputs()
        self.input_dict = {
            "I8": inputs[0],
            "I7": inputs[1],
            "I6": inputs[2],
            "I5": inputs[3],
            "I4": inputs[4],
            "I3": inputs[5],
            "I2": inputs[6],
            "I1": inputs[7],
        }
        self.output_dict = {
            "O3": outputs[0],
            "O2": outputs[1],
            "O1": outputs[2],
            "Valid": outputs[3],
        }
        self.nand_gate_1 = self.create_element(NAND_Gate, 4, 1)
        self.nand_gate_2 = self.create_element(NAND_Gate, 4, 1)
        self.nand_gate_3 = self.create_element(NAND_Gate, 4, 1)
        self.nand_gate_4 = self.create_element(NAND_Gate, 4, 1)
        self.additional_nand_1 = self.create_element(NAND_Gate)
        self.additional_nand_2 = self.create_element(NAND_Gate)
        self.additional_nand_3 = self.create_element(NAND_Gate)
        self.not_gate_1 = self.create_element(NOT_Gate)
        self.not_gate_2 = self.create_element(NOT_Gate)
        self.not_gate_3 = self.create_element(NOT_Gate)
        self.not_gate_4 = self.create_element(NOT_Gate)
        self.not_gate_5 = self.create_element(NOT_Gate)
        self.or_gate_1 = self.create_element(OR_Gate, 3, 1)
        self.or_gate_2 = self.create_element(OR_Gate, 3, 1)
        self.nor_gate = self.create_element(NOR_Gate)
        board.connect_pins(
            self.external_inner_convertor("I1"),
            self.nor_gate.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I2"),
            self.not_gate_1.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.not_gate_1.get_outputs()[0],
            self.or_gate_1.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I3"),
            self.or_gate_1.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I3"),
            self.additional_nand_2.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I4"),
            self.additional_nand_1.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I5"),
            self.or_gate_2.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I5"),
            self.not_gate_3.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.not_gate_3.get_outputs()[0],
            self.nand_gate_4.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I6"),
            self.additional_nand_3.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I6"),
            self.or_gate_2.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I7"),
            self.or_gate_2.get_inputs()[2],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I7"),
            self.not_gate_4.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.not_gate_4.get_outputs()[0],
            self.additional_nand_3.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.not_gate_4.get_outputs()[0],
            self.nand_gate_4.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.not_gate_4.get_outputs()[0],
            self.nand_gate_3.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I8"),
            self.not_gate_5.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.not_gate_5.get_outputs()[0],
            self.nand_gate_4.get_inputs()[2],
            update=False,
        )
        board.connect_pins(
            self.not_gate_5.get_outputs()[0],
            self.nand_gate_3.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.not_gate_5.get_outputs()[0],
            self.nand_gate_2.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.or_gate_2.get_outputs()[0],
            self.or_gate_1.get_inputs()[2],
            update=False,
        )
        board.connect_pins(
            self.or_gate_2.get_outputs()[0],
            self.not_gate_2.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.not_gate_2.get_outputs()[0],
            self.additional_nand_1.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.not_gate_2.get_outputs()[0],
            self.additional_nand_2.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.additional_nand_3.get_outputs()[0],
            self.nand_gate_4.get_inputs()[3],
            update=False,
        )
        board.connect_pins(
            self.additional_nand_3.get_outputs()[0],
            self.nand_gate_2.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.or_gate_1.get_outputs()[0],
            self.nand_gate_1.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.or_gate_1.get_outputs()[0],
            self.nand_gate_2.get_inputs()[2],
            update=False,
        )
        board.connect_pins(
            self.additional_nand_1.get_outputs()[0],
            self.nand_gate_1.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.additional_nand_1.get_outputs()[0],
            self.nand_gate_2.get_inputs()[3],
            update=False,
        )
        board.connect_pins(
            self.additional_nand_1.get_outputs()[0],
            self.nand_gate_3.get_inputs()[2],
            update=False,
        )
        board.connect_pins(
            self.additional_nand_2.get_outputs()[0],
            self.nand_gate_1.get_inputs()[2],
            update=False,
        )
        board.connect_pins(
            self.additional_nand_2.get_outputs()[0],
            self.nand_gate_3.get_inputs()[3],
            update=False,
        )
        board.connect_pins(
            self.nand_gate_4.get_outputs()[0],
            self.nor_gate.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.nand_gate_4.get_outputs()[0],
            self.inner_external_convertor("O3"),
            update=False,
        )
        board.connect_pins(
            self.nor_gate.get_outputs()[0],
            self.nand_gate_1.get_inputs()[3],
            update=False,
        )
        board.connect_pins(
            self.nand_gate_1.get_outputs()[0],
            self.inner_external_convertor("Valid"),
            update=False,
        )
        board.connect_pins(
            self.nand_gate_2.get_outputs()[0],
            self.inner_external_convertor("O1"),
            update=False,
        )
        board.connect_pins(
            self.nand_gate_3.get_outputs()[0],
            self.inner_external_convertor("O2"),
            update=False,
        )
        self.get_board().update_board()


class ShiftLeft(AdvancedCircuitElement):
    """
    Moving a bit pattern to the left
        1      0      1     0
        ↓      ↓      ↓     ↓
     ┌────────────────────────┐
     |       Shift left       |
     └────────────────────────┘
        ↓      ↓      ↓     ↓
        0      1      0     0
    Input pins:
        0: I1
        1: I2
        2: I3
        3: I4
    Output pins:
        0: O1
        1: O2
        2: O3
        3: O4
    """

    def __init__(self, board: Board, i_number=4, o_number=4):
        super().__init__(board, i_number, o_number)
        inputs = self.get_inputs()
        outputs = self.get_outputs()
        self.input_dict = {
            "I1": inputs[0],
            "I2": inputs[1],
            "I3": inputs[2],
            "I4": inputs[3],
        }
        self.output_dict = {
            "O1": outputs[0],
            "O2": outputs[1],
            "O3": outputs[2],
            "O4": outputs[3],
        }
        self.controller = self.create_element(ZERO_Generator)
        self.not_gate = self.create_element(NOT_Gate)
        self.and_gate_1 = self.create_element(AND_Gate)
        self.and_gate_2 = self.create_element(AND_Gate)
        self.and_gate_3 = self.create_element(AND_Gate)
        self.and_gate_4 = self.create_element(AND_Gate)
        self.and_gate_5 = self.create_element(AND_Gate)
        self.and_gate_6 = self.create_element(AND_Gate)
        self.or_gate_1 = self.create_element(OR_Gate)
        self.or_gate_2 = self.create_element(OR_Gate)
        board.connect_pins(
            self.controller.get_outputs()[0],
            self.not_gate.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I1"),
            self.and_gate_1.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I2"),
            self.and_gate_2.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I2"),
            self.and_gate_3.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I3"),
            self.and_gate_4.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I3"),
            self.and_gate_5.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I4"),
            self.and_gate_6.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.controller.get_outputs()[0],
            self.and_gate_1.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.controller.get_outputs()[0],
            self.and_gate_3.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.controller.get_outputs()[0],
            self.and_gate_5.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.not_gate.get_outputs()[0],
            self.and_gate_2.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.not_gate.get_outputs()[0],
            self.and_gate_4.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.not_gate.get_outputs()[0],
            self.and_gate_6.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.and_gate_1.get_outputs()[0],
            self.or_gate_1.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.and_gate_4.get_outputs()[0],
            self.or_gate_1.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.and_gate_3.get_outputs()[0],
            self.or_gate_2.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.and_gate_6.get_outputs()[0],
            self.or_gate_2.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.and_gate_2.get_outputs()[0],
            self.inner_external_convertor("O1"),
            update=False,
        )
        board.connect_pins(
            self.or_gate_1.get_outputs()[0],
            self.inner_external_convertor("O2"),
            update=False,
        )
        board.connect_pins(
            self.or_gate_2.get_outputs()[0],
            self.inner_external_convertor("O3"),
            update=False,
        )
        board.connect_pins(
            self.and_gate_5.get_outputs()[0],
            self.inner_external_convertor("O4"),
            update=False,
        )
        self.get_board().update_board()


class ShiftRight(AdvancedCircuitElement):
    """
    Moving a bit pattern to the right
        1      0      1     0
        ↓      ↓      ↓     ↓
     ┌────────────────────────┐
     |      Shift right       |
     └────────────────────────┘
        ↓      ↓      ↓     ↓
        0      1      0     1
        Input pins:
        0: I1
        1: I2
        2: I3
        3: I4
    Output pins:
        0: O1
        1: O2
        2: O3
        3: O4
    """

    def __init__(self, board: Board, i_number=4, o_number=4):
        super().__init__(board, i_number, o_number)
        inputs = self.get_inputs()
        outputs = self.get_outputs()
        self.input_dict = {
            "I1": inputs[0],
            "I2": inputs[1],
            "I3": inputs[2],
            "I4": inputs[3],
        }
        self.output_dict = {
            "O1": outputs[0],
            "O2": outputs[1],
            "O3": outputs[2],
            "O4": outputs[3],
        }
        self.controller = self.create_element(ONE_Generator)
        self.not_gate = self.create_element(NOT_Gate)
        self.and_gate_1 = self.create_element(AND_Gate)
        self.and_gate_2 = self.create_element(AND_Gate)
        self.and_gate_3 = self.create_element(AND_Gate)
        self.and_gate_4 = self.create_element(AND_Gate)
        self.and_gate_5 = self.create_element(AND_Gate)
        self.and_gate_6 = self.create_element(AND_Gate)
        self.or_gate_1 = self.create_element(OR_Gate)
        self.or_gate_2 = self.create_element(OR_Gate)
        board.connect_pins(
            self.controller.get_outputs()[0],
            self.not_gate.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I1"),
            self.and_gate_1.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I2"),
            self.and_gate_2.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I2"),
            self.and_gate_3.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I3"),
            self.and_gate_4.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I3"),
            self.and_gate_5.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("I4"),
            self.and_gate_6.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.controller.get_outputs()[0],
            self.and_gate_1.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.controller.get_outputs()[0],
            self.and_gate_3.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.controller.get_outputs()[0],
            self.and_gate_5.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.not_gate.get_outputs()[0],
            self.and_gate_2.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.not_gate.get_outputs()[0],
            self.and_gate_4.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.not_gate.get_outputs()[0],
            self.and_gate_6.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.and_gate_1.get_outputs()[0],
            self.or_gate_1.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.and_gate_4.get_outputs()[0],
            self.or_gate_1.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.and_gate_3.get_outputs()[0],
            self.or_gate_2.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.and_gate_6.get_outputs()[0],
            self.or_gate_2.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.and_gate_2.get_outputs()[0],
            self.inner_external_convertor("O1"),
            update=False,
        )
        board.connect_pins(
            self.or_gate_1.get_outputs()[0],
            self.inner_external_convertor("O2"),
            update=False,
        )
        board.connect_pins(
            self.or_gate_2.get_outputs()[0],
            self.inner_external_convertor("O3"),
            update=False,
        )
        board.connect_pins(
            self.and_gate_5.get_outputs()[0],
            self.inner_external_convertor("O4"),
            update=False,
        )
        self.get_board().update_board()


class ALU_1_bit(AdvancedCircuitElement):
    """
    Input pins:
        0: Input A
        1: Input B
        2: Carry In
        3: Borrow In
        4: Select S1
        5: Select S2
    Output pins:
        0: Result
        1: Carry Out
        2: Borrow Out
    """

    def __init__(self, board: Board, i_number=6, o_number=3):
        super().__init__(board, i_number, o_number)
        inputs = self.get_inputs()
        outputs = self.get_outputs()
        self.input_dict = {
            "Input A": inputs[0],
            "Input B": inputs[1],
            "Carry In": inputs[2],
            "Borrow In": inputs[3],
            "Select S1": inputs[4],
            "Select S0": inputs[5],
        }
        self.output_dict = {
            "Result": outputs[0],
            "Carry Out": outputs[1],
            "Borrow Out": outputs[2],
        }
        self.adder = self.create_element(Adder)
        self.substractor = self.create_element(Substractor)
        self.and_gate = self.create_element(AND_Gate)
        self.or_gate = self.create_element(OR_Gate)
        self.mux = self.create_element(Multiplexor)
        board.connect_pins(
            self.external_inner_convertor("Input A"),
            self.adder.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Input B"),
            self.adder.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Carry In"),
            self.adder.get_inputs()[2],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Input A"),
            self.substractor.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Input B"),
            self.substractor.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Borrow In"),
            self.substractor.get_inputs()[2],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Input A"),
            self.and_gate.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Input B"),
            self.and_gate.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Input A"),
            self.or_gate.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Input B"),
            self.or_gate.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Select S1"),
            self.mux.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Select S0"),
            self.mux.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.adder.get_outputs()[0], self.mux.get_inputs()[2], update=False
        )
        board.connect_pins(
            self.substractor.get_outputs()[0], self.mux.get_inputs()[3], update=False
        )
        board.connect_pins(
            self.and_gate.get_outputs()[0], self.mux.get_inputs()[4], update=False
        )
        board.connect_pins(
            self.or_gate.get_outputs()[0], self.mux.get_inputs()[5], update=False
        )
        board.connect_pins(
            self.substractor.get_outputs()[1],
            self.inner_external_convertor("Borrow Out"),
            update=False,
        )
        board.connect_pins(
            self.adder.get_outputs()[1],
            self.inner_external_convertor("Carry Out"),
            update=False,
        )
        board.connect_pins(
            self.mux.get_outputs()[0], self.inner_external_convertor("Result")
        )
        self.get_board().update_board()


class ALU_4_bit(AdvancedCircuitElement):
    """
    Input pins:
        0: A3
        1: A2
        2: A1
        3: A0
        4: B3
        5: B2
        6: B1
        7: B0
        8: Carry In
        9: Borrow In
        10: Select S1
        11: Select S2
    Output pins:
        0: O3
        1: O2
        2: O1
        3: O0
        1: Select S1
        2: Select S0
    """
    def __init__(self, board: Board, i_number=12, o_number=6):
        super().__init__(board, i_number, o_number)
        inputs = self.get_inputs()
        outputs = self.get_outputs()
        self.input_dict = {
            "A3": inputs[0],
            "A2": inputs[1],
            "A1": inputs[2],
            "A0": inputs[3],
            "B3": inputs[4],
            "B2": inputs[5],
            "B1": inputs[6],
            "B0": inputs[7],
            "Carry In": inputs[8],
            "Borrow In": inputs[9],
            "Select S1": inputs[10],
            "Select S0": inputs[11],
        }
        self.output_dict = {
            "O3": outputs[0],
            "O2": outputs[1],
            "O1": outputs[2],
            "O0": outputs[3],
            "Overflow Adder": outputs[4],
            "Overflow Substractor": outputs[5],
        }
        self.alu_1 = self.create_element(ALU_1_bit)
        self.alu_2 = self.create_element(ALU_1_bit)
        self.alu_3 = self.create_element(ALU_1_bit)
        self.alu_4 = self.create_element(ALU_1_bit)
        board.connect_pins(
            self.external_inner_convertor("A0"),
            self.alu_1.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("B0"),
            self.alu_1.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Carry In"),
            self.alu_1.get_inputs()[2],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Borrow In"),
            self.alu_1.get_inputs()[3],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Select S1"),
            self.alu_1.get_inputs()[4],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Select S0"),
            self.alu_1.get_inputs()[5],
            update=False,
        )
        board.connect_pins(
            self.alu_1.get_outputs()[0],
            self.inner_external_convertor("O0"),
            update=False,
        )
        board.connect_pins(
            self.alu_1.get_outputs()[1], self.alu_2.get_inputs()[2], update=False
        )
        board.connect_pins(
            self.alu_1.get_outputs()[2], self.alu_2.get_inputs()[3], update=False
        )
        board.connect_pins(
            self.external_inner_convertor("A1"),
            self.alu_2.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("B1"),
            self.alu_2.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Select S1"),
            self.alu_2.get_inputs()[4],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Select S0"),
            self.alu_2.get_inputs()[5],
            update=False,
        )
        board.connect_pins(
            self.alu_2.get_outputs()[0],
            self.inner_external_convertor("O1"),
            update=False,
        )
        board.connect_pins(
            self.alu_2.get_outputs()[1], self.alu_3.get_inputs()[2], update=False
        )
        board.connect_pins(
            self.alu_2.get_outputs()[2], self.alu_3.get_inputs()[3], update=False
        )
        board.connect_pins(
            self.external_inner_convertor("A2"),
            self.alu_3.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("B2"),
            self.alu_3.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Select S1"),
            self.alu_3.get_inputs()[4],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Select S0"),
            self.alu_3.get_inputs()[5],
            update=False,
        )
        board.connect_pins(
            self.alu_3.get_outputs()[0],
            self.inner_external_convertor("O2"),
            update=False,
        )
        board.connect_pins(
            self.alu_3.get_outputs()[1], self.alu_4.get_inputs()[2], update=False
        )
        board.connect_pins(
            self.alu_3.get_outputs()[2], self.alu_4.get_inputs()[3], update=False
        )
        board.connect_pins(
            self.external_inner_convertor("A3"),
            self.alu_4.get_inputs()[0],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("B3"),
            self.alu_4.get_inputs()[1],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Select S1"),
            self.alu_4.get_inputs()[4],
            update=False,
        )
        board.connect_pins(
            self.external_inner_convertor("Select S0"),
            self.alu_4.get_inputs()[5],
            update=False,
        )
        board.connect_pins(
            self.alu_4.get_outputs()[0],
            self.inner_external_convertor("O3"),
            update=False,
        )
        board.connect_pins(
            self.alu_4.get_outputs()[1],
            self.inner_external_convertor("Overflow Adder"),
            update=False,
        )
        board.connect_pins(
            self.alu_4.get_outputs()[2],
            self.inner_external_convertor("Overflow Substractor"),
            update=False,
        )


def main():
    board = Board()

    one1 = board.create_element(ZERO_Generator)
    one2 = board.create_element(ONE_Generator)
    one3 = board.create_element(ZERO_Generator)
    one4 = board.create_element(ONE_Generator)
    one5 = board.create_element(ZERO_Generator)
    one6 = board.create_element(ZERO_Generator)
    one7 = board.create_element(ONE_Generator)
    one8 = board.create_element(ONE_Generator)
    one9 = board.create_element(ZERO_Generator)
    one10 = board.create_element(ZERO_Generator)
    one11 = board.create_element(ZERO_Generator)
    one12 = board.create_element(ONE_Generator)

    lamp = board.create_element(Lamp)
    lamp_2 = board.create_element(Lamp)
    lamp_3 = board.create_element(Lamp)
    lamp_4 = board.create_element(Lamp)
    lamp_5 = board.create_element(Lamp)
    lamp_6 = board.create_element(Lamp)

    alu = board.create_element(ALU_4_bit)
    board.connect_pins(one1.get_outputs()[0], alu.get_inputs()[0])
    board.connect_pins(one2.get_outputs()[0], alu.get_inputs()[1])
    board.connect_pins(one3.get_outputs()[0], alu.get_inputs()[2])
    board.connect_pins(one4.get_outputs()[0], alu.get_inputs()[3])
    board.connect_pins(one5.get_outputs()[0], alu.get_inputs()[4])
    board.connect_pins(one6.get_outputs()[0], alu.get_inputs()[5])
    board.connect_pins(one7.get_outputs()[0], alu.get_inputs()[6])
    board.connect_pins(one8.get_outputs()[0], alu.get_inputs()[7])
    board.connect_pins(one9.get_outputs()[0], alu.get_inputs()[8])
    board.connect_pins(one10.get_outputs()[0], alu.get_inputs()[9])
    board.connect_pins(one11.get_outputs()[0], alu.get_inputs()[10])
    board.connect_pins(one12.get_outputs()[0], alu.get_inputs()[11])

    board.connect_pins(alu.get_outputs()[0], lamp.get_inputs()[0])
    board.connect_pins(alu.get_outputs()[1], lamp_2.get_inputs()[0])
    board.connect_pins(alu.get_outputs()[2], lamp_3.get_inputs()[0])
    board.connect_pins(alu.get_outputs()[3], lamp_4.get_inputs()[0])
    board.connect_pins(alu.get_outputs()[4], lamp_5.get_inputs()[0])
    board.connect_pins(alu.get_outputs()[5], lamp_6.get_inputs()[0])

    print("Final state: ")
    board.update_board()
    print(alu.get_outputs())

    """g = board.create_element(ClockGenerator)
    time.sleep(2)
    print("-----")
    time.sleep(2)
    board.remove_element(g)
    print("Killed?")
    time.sleep(3)
    print("Killed.")"""


if __name__ == "__main__":
    main()
