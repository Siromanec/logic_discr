from __future__ import annotations

from exceptions import *


class Pin:
    count = 0

    def __init__(self, circuit: BaseCircuitElement) -> None:
        if not isinstance(circuit, BaseCircuitElement):
            raise ValueError("Incorrect type of circuit!")
        self.id = Pin.count
        Pin.count += 1
        self._circuit = circuit
        self._state = False

    def __eq__(self, other: Pin) -> bool:
        """All pins are unique"""
        return id(self) == id(other)

    def __hash__(self):
        return hash(self.id)

    def get_state(self) -> bool:

        return self._state

    def set_state(self, new_state: bool):
        if not isinstance(new_state, bool):
            raise ValueError("Incorrect value for a pin state!")
        self._state = new_state

    def get_circuit(self) -> BaseCircuitElement:
        return self._circuit


class InputPin(Pin):
    def __init__(self, circuit: BaseCircuitElement) -> None:
        super().__init__(circuit)
        self._parent = None

    def __str__(self) -> str:
        return ' '.join((
            'type:',
            'InputPin',
            'id:',
            str(self.id),
            'gate:',
            repr(self.get_circuit()),
            'state:',
            str(self.get_state()),
            'parent:',
            repr(self.get_parent())))

    def __repr__(self):
        if self.get_parent():
            return "InputPin(id={}, parent={}, gate={}, state={})".format(str(self.id),
                                                                         str(self.get_parent().id),
                                                                         str(self.get_circuit()),
                                                                         str(self.get_state()))
        return "InputPin(id={}, noparent, gate={}, state={})".format(str(self.id),
                                                                      str(self.get_circuit()),
                                                                      str(self.get_state()))

    def update_state(self):
        if self._parent is not None and self._parent.get_state() is True:
            self.set_state(True)
        else:
            self.set_state(False)

    def set_parent(self, new_parent: OutputPin):
        if self._parent is not None:
            raise ParentAlreadyExistsError("Disconnect this pin from his current parent first!")
        if not isinstance(new_parent, OutputPin):
            raise ValueError("Incorrect pin type!")
        self._parent = new_parent

    def remove_parent(self):
        self._parent = None

    def get_parent(self):
        return self._parent


class OutputPin(Pin):
    def __init__(self, circuit: BaseCircuitElement) -> None:
        super().__init__(circuit)
        self._children = []

    def __str__(self) -> str:
        return ' '.join((
            'type:',
            'OutputPin',
            'id:',
            str(self.id),
            'gate:',
            repr(self.get_circuit()),
            'state:',
            str(self.get_state()),
            'children:',
            repr(self.get_children())))

    def __repr__(self):
        return "OutputPin(id={}, childrenId={}, gate={}, state={})".format(str(self.id),
                                                                           str([child.id for child in self.get_children()]),
                                                                           repr(self.get_circuit()),
                                                                           str(self.get_state()))

    def update_state(self, new_state: bool):
        self.set_state(new_state)

    def add_child(self, child: InputPin):
        if not isinstance(child, InputPin):
            raise ValueError("A child can only be an InputPin")
        self._children.append(child)

    def remove_child(self, child: InputPin):
        if not isinstance(child, InputPin):
            raise ValueError("A child can only be an InputPin")
        if child not in self.get_children():
            raise IndexError("The child doesn't exist!")
        self._children.remove(child)

    def get_children(self):
        return list(self._children)


class BaseCircuitElement:
    """
    Base circuit element
    Can work for gates and electronics
    """
    count = 0

    def __init__(self, board, input_pins_amount: int, output_pins_amount: int) -> None:
        self._input_pins = tuple(InputPin(self) for _ in range(input_pins_amount))
        self._output_pins = tuple(OutputPin(self) for _ in range(output_pins_amount))
        self._board = board
        self.id = BaseCircuitElement.count
        BaseCircuitElement.count += 1

    def __eq__(self, other: BaseCircuitElement) -> bool:
        """All circuit elements are unique"""
        return id(self) == id(other)

    def __str__(self) -> str:
        return ' '.join((repr(self), "inputs Id's:", str([pin.id for pin in self.get_inputs()]),
                         "outputs Id's:", str([pin.id for pin in self.get_outputs()])))

    def __repr__(self) -> str:
        return self.__class__.__name__ + "()"

    def __hash__(self) -> int:
        return hash(id(self))

    def get_inputs(self) -> tuple[InputPin]:
        return list(self._input_pins)

    def get_outputs(self) -> tuple[OutputPin]:
        return list(self._output_pins)

    def get_board(self):
        return self._board

    def get_dependent_circuits(self):
        output_pins = self.get_outputs()
        dependent_circuits = set()
        for pin in output_pins:
            for child in pin.get_children():
                dependent_circuits.add(child.get_circuit())
        return list(dependent_circuits)

    def get_parent_circuits(self) -> set[BaseCircuitElement]:
        input_pins = self.get_inputs()
        parent_circuits = set()
        for pin in input_pins:
            if pin.get_parent():
                parent_circuits.add(pin.get_parent().get_circuit())
        return list(parent_circuits)

    def is_fully_connected(self):
        for pin in self.get_inputs():
            if pin.get_parent() is None:
                return False
        return True

    def operation(self):
        """Depends on the element"""
        pass

    def update(self):
        if not self.is_fully_connected():
            for pin in self.get_outputs():
                pin.update_state(False)
            print("Not fully connected: " + str(self))
            return
            # raise NotConnectedCircuitError()
        for pin in self.get_inputs():
            pin.update_state()
        self.operation()

    def cycle_processing(self):
        """Maybe it should become red on the board or smth like that"""
        pass

    def destroy(self):
        pass  # some additional actions to destroy the circuit?


class Board:

    def __init__(self):
        self.circuits_list = []

    def connect_pins(self, parent_pin: OutputPin, child_pin: InputPin, update=True):
        """Connects a parent pin with a child pin"""
        parent_pin.add_child(child_pin)
        child_pin.set_parent(parent_pin)
        if update:
            self.update_board()

    def disconnect_pins(self, parent_pin: OutputPin, child_pin: InputPin, update=True):
        """Disconnects a parent pin and a child pin"""
        parent_pin.remove_child(child_pin)
        child_pin.remove_parent(parent_pin)
        if update:
            self.update_board()

    def remove_element(self, circuit: BaseCircuitElement):
        """Removes given circuit from a board and - deletes it"""
        for child in circuit.get_inputs():
            parent = child.get_parent()
            self.disconnect_pins(parent, child, update=False)
        for parent in circuit.get_outputs():
            children = parent.get_children()
            for child in children:
                self.disconnect_pins(parent, child, update=False)
        self.circuits_list.remove(circuit)
        circuit.destroy()
        self.update_board()

    def create_element(self, circuit_type, inputs=None, outputs=None):
        """Creates a circuit of a given type on the board"""
        try:
            if not issubclass(circuit_type, BaseCircuitElement):
                raise ValueError("Incorrect circuit type!")
        except TypeError as e:
            raise e

        if inputs is not None and outputs is not None:
            new_circuit = circuit_type(self, inputs, outputs)
        elif inputs is not None:
            new_circuit = circuit_type(self, inputs)
        elif outputs is not None:
            new_circuit = circuit_type(self, outputs)
        else:
            new_circuit = circuit_type(self)

        self.circuits_list.append(new_circuit)

        return new_circuit

    def get_circuits_list(self) -> list[BaseCircuitElement]:
        return list(self.circuits_list)

    def update_board(self):
        """Updates board status"""
        circuits = self.get_circuits_list()
        independent_circuits = []
        circuits_dependence = {}
        for circuit in circuits:
            circuits_dependence[circuit] = len(circuit.get_parent_circuits())
            if circuits_dependence[circuit] == 0:
                independent_circuits.append(circuit)

        while independent_circuits:
            circuit = independent_circuits.pop(0)
            circuit.update()
            for dependent_circuit in circuit.get_dependent_circuits():
                circuits_dependence[dependent_circuit] -= 1
                if circuits_dependence[dependent_circuit] == 0:
                    independent_circuits.append(dependent_circuit)
            circuits.remove(circuit)
        for circuit in circuits:
            circuit.cycle_processing()

    '''def update(self, structure=""):
        """Updates structure state, using topology sorting"""
        if not structure:
            structure = self
        circuits = self.get_circuits_list()
        independent_circuits = []
        circuits_dependence = {}
        for circuit in circuits:
            circuits_dependence[circuit] = len(circuit.get_parent_circuits())
            if circuits_dependence[circuit] == 0:
                independent_circuits.append(circuit)

        while independent_circuits:
            circuit = independent_circuits.pop(0)
            circuit.update()
            for dependent_circuit in circuit.get_dependent_circuits():
                circuits_dependence[dependent_circuit] -= 1
                if circuits_dependence[dependent_circuit] == 0:
                    independent_circuits.append(dependent_circuit)
            circuits.remove(circuit)
        for circuit in circuits:
            circuit.cycle_processing()'''
