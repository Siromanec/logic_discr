from Fundamentals import Board, BaseCircuitElement, InputPin, OutputPin
from Simple_board_elements import AND_Gate, XOR_Gate, ONEGenerator, ZEROGenerator, Lamp


class AdvancedCircuitElement(BaseCircuitElement):
    def __init__(self, board, i_number=1, o_number=1):
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

    def create_element(self, circuit_type):
        """Creates a circuit of a given type in this circuit"""
        try:
            if not issubclass(circuit_type, BaseCircuitElement):
                raise ValueError("Incorrect circuit type!")
        except TypeError as e:
            raise e
        new_circuit = circuit_type(self.get_board())
        self._elements.append(new_circuit)
        return new_circuit

    def get_elements(self):
        return list(self._elements)

    def operation(self):
        def topo_sorted_update():
            circuits = self.get_elements()
            independent_circuits = []
            circuits_dependence = {}
            for circuit in circuits:
                circuits_set = circuit.get_parent_circuits()
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
        1: carry"""

    def __init__(self, board, i_number=2, o_number=2):
        super().__init__(board, i_number, o_number)
        inputs = self.get_inputs()
        outputs = self.get_outputs()
        self.input_dict = {"A": inputs[0], "B": inputs[1]}
        self.output_dict = {"Sum": outputs[0], "Carry": outputs[1]}

        self.xor1 = self.create_element(XOR_Gate)
        self.and1 = self.create_element(AND_Gate)

        board.connect_pins(self.external_inner_convertor("A"), self.xor1.get_inputs()[0], update=False)
        board.connect_pins(self.external_inner_convertor("B"), self.xor1.get_inputs()[1], update=False)
        board.connect_pins(self.external_inner_convertor("A"), self.and1.get_inputs()[0], update=False)
        board.connect_pins(self.external_inner_convertor("B"), self.and1.get_inputs()[1], update=False)
        board.connect_pins(self.xor1.get_outputs()[0], self.inner_external_convertor("Sum"), update=False)
        board.connect_pins(self.and1.get_outputs()[0], self.inner_external_convertor("Carry"), update=False)

        self.get_board().update_board()


def main():
    board = Board()

    one1 = board.create_element(ONEGenerator)
    one2 = board.create_element(ONEGenerator)
    zero = board.create_element(ZEROGenerator)
    and_gate = board.create_element(AND_Gate)
    lamp = board.create_element(Lamp)
    half_adder1 = board.create_element(HalfAdder)

    board.connect_pins(one1.get_outputs()[0], and_gate.get_inputs()[0])
    board.connect_pins(one2.get_outputs()[0], and_gate.get_inputs()[1])
    board.connect_pins(one2.get_outputs()[0], half_adder1.input_dict["A"])
    board.connect_pins(one1.get_outputs()[0], half_adder1.input_dict["B"])

    board.connect_pins(and_gate.get_outputs()[0], lamp.get_inputs()[0])


    print("Final state: ")
    board.update_board()
    print(half_adder1.get_outputs())



if __name__ == '__main__':
    main()
