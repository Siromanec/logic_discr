"""
Fundamentals.py
[Pin, InputPin, OutputPin,
 BaseCircuitElement, Board]
"""
from __future__ import annotations
import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from exceptions.exceptions import *


class Pin:
    """
    class Pin
    represents connections of elements
    """
    count = 0

    def __init__(self, circuit: BaseCircuitElement) -> None:
        if not isinstance(circuit, BaseCircuitElement):
            raise ValueError("Incorrect type of circuit!")
        self.id = Pin.count
        Pin.count += 1
        self._circuit = circuit
        self._state = False
        self._reaction_area = None
        self._connected_line_tag = None

    def __eq__(self, other: Pin) -> bool:
        """All pins are unique"""
        return id(self) == id(other)

    def __hash__(self):
        return hash(self.id)

    def get_state(self) -> bool:
        """
        returns the state of the pin
        """
        return self._state

    def set_state(self, new_state: bool):
        """
        sets the state of the pin
        """
        if not isinstance(new_state, bool):
            raise ValueError("Incorrect value for a pin state!")
        self._state = new_state

    def get_circuit(self) -> BaseCircuitElement:
        """
        returns the element that this pin is on
        """
        return self._circuit

    def set_reaction_area(self, x1, y1, x2, y2):
        """Set reaction area for the pin"""
        self._reaction_area = (x1, y1, x2, y2)

    def get_reaction_area(self):
        """Get reaction area of the pin"""
        return self._reaction_area

    def set_connected_line_tag(self, line_tag):
        self._connected_line_tag = line_tag

    def get_connected_line_tag(self):
        return self._connected_line_tag

    def remove_connected_line_tag(self):
        self._connected_line_tag = None


    def check_dot(self, x_coord, y_coord):
        """Check if dot is in the reaction area"""
        area = self.get_reaction_area()
        return area[0] <= x_coord <= area[2] and area[1] <= y_coord <= area[3]

    def is_connected(self):
        """used to check connections"""


class InputPin(Pin):
    """
    class InputPin
    used to represent the input pins of an element
    """
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
                                                                          str(self.get_parent(
                                                                          ).id),
                                                                          str(self.get_circuit(
                                                                          )),
                                                                          str(self.get_state()))
        return "InputPin(id={}, noparent, gate={}, state={})".format(str(self.id),
                                                                     str(self.get_circuit(
                                                                     )),
                                                                     str(self.get_state()))

    def update_state(self):
        """
        copies the state of parent pin
        """
        self.set_state(self._parent.is_connected() and self.get_parent().get_state())

    def set_parent(self, new_parent: OutputPin):
        """
        sets parent
        """
        if  self.is_connected():
            raise ParentAlreadyExistsError(
                "Disconnect this pin from his current parent first!")
        if not isinstance(new_parent, OutputPin):
            raise ValueError("Incorrect pin type!")
        self._parent = new_parent

    def remove_parent(self):
        """
        removes parent
        """
        self._parent = None

    def get_parent(self) -> OutputPin:
        """
        returns parent of the pin
        """
        return self._parent

    def is_connected(self) -> bool:
        """
        checks if self has connections
        """
        return bool(self.get_parent())


class OutputPin(Pin):
    """
    class OutputPin
    used to represent the output pins of an element
    """
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

    def __repr__(self) -> str:
        return "OutputPin(id={}, childrenId={}, gate={}, state={})".format(str(self.id),
                                                                           str([
                                                                               child.id for child in self.get_children()]),
                                                                           repr(
                                                                               self.get_circuit()),
                                                                           str(self.get_state()))

    def update_state(self, new_state: bool):
        """
        updates the state of the pin
        """
        self.set_state(new_state)

    def add_child(self, child: InputPin):
        """
        adds a child
        """
        if not isinstance(child, InputPin):
            raise ValueError("A child can only be an InputPin")
        self._children.append(child)

    def remove_child(self, child: InputPin):
        """
        removes the given child
        """
        if not isinstance(child, InputPin):
            raise ValueError("A child can only be an InputPin")
        if child not in self.get_children():
            raise IndexError("The child doesn't exist!")
        self._children.remove(child)

    def get_children(self) -> list[InputPin]:
        """
        return s list of input pins
        """
        return list(self._children)

    def is_connected(self) -> bool:
        """
        checks if has any children
        """

        return bool(self.get_children())


class BaseCircuitElement:
    """
    Base circuit element
    Can work for gates and electronics
    """
    count = 0

    def __init__(self, board: Board,
                 input_pins_amount: int,
                 output_pins_amount: int) -> None:
        self._input_pins = tuple(InputPin(self)
                                 for _ in range(input_pins_amount))
        self._output_pins = tuple(OutputPin(self)
                                  for _ in range(output_pins_amount))
        self._board = board
        self.id = BaseCircuitElement.count
        BaseCircuitElement.count += 1
        self.img_object = None
        self.img_path = None
        self._img_coords = None
        self._img_width = 100
        self._img_height = 50

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
        """
        retuns a list of all input pins
        """
        return list(self._input_pins)

    def get_outputs(self) -> tuple[OutputPin]:
        """
        retuns a list of all output pins
        """
        return list(self._output_pins)

    def get_board(self) -> Board:
        """
        returns the board that the element is on
        """
        return self._board


    def set_img_coords(self, x_coord, y_coord):
        self._img_coords = (x_coord, y_coord)

    def get_img_coords(self):
        return self._img_coords

    def set_img_width(self, width):
        self._img_width = width

    def get_img_width(self):
        return self._img_width

    def set_img_height(self, height):
        self._img_height = height

    def get_img_height(self):
        return self._img_height

    def get_dependent_circuits(self) -> list[BaseCircuitElement]:
        """
        returns a list of all circuits that are connected to output pins
        """
        output_pins = self.get_outputs()
        dependent_circuits = set()
        for pin in output_pins:
            for child in pin.get_children():
                dependent_circuits.add(child.get_circuit())
        return list(dependent_circuits)

    def get_parent_circuits(self) -> list[BaseCircuitElement]:
        """
        returns a list of all circuits that are connected to input pins
        """
        input_pins = self.get_inputs()
        parent_circuits = set()
        for pin in input_pins:
            if pin.get_parent():
                parent_circuits.add(pin.get_parent().get_circuit())
        return list(parent_circuits)

    def is_fully_connected(self):
        """
        checks if all elements are connected
        """
        for pin in self.get_inputs():
            if pin.get_parent() is None:
                return False
        return True

    def operation(self):
        """Depends on the element"""

    def set_reaction_areas_for_pins(self):
        """Depends on the element"""

    def update_reaction_areas(self, x_coord, y_coord):
        """Update reaction areas of pins depending on the position of the image"""
        for input_pin in self.get_inputs():
            old_area = input_pin.get_reaction_area()
            if old_area:
                input_pin.set_reaction_area(
                    old_area[0] + x_coord,
                    old_area[1] + y_coord,
                    old_area[2] + x_coord,
                    old_area[3] + y_coord
                    )

        for output_pin in self.get_outputs():
            old_area = output_pin.get_reaction_area()
            if old_area:
                output_pin.set_reaction_area(
                    old_area[0] + x_coord,
                    old_area[1] + y_coord,
                    old_area[2] + x_coord,
                    old_area[3] + y_coord
                    )

    def check_dot_in_img(self, x_coord, y_coord):
        """Check if dot is in the image's area"""
        center = self.get_img_coords()
        center_x, center_y = center[0], center[1]
        x_shift, y_shift = self.get_img_width()/2, self.get_img_height()/2
        return ((center_x - x_shift <= x_coord <= center_x + x_shift) and
                (center_y - y_shift <= y_coord <= center_y + y_shift))


    def update(self):
        """updates the BCE"""
        if not self.is_fully_connected():
            for pin in self.get_outputs():
                pin.update_state(False)
            print("Not fully connected: " + str(self))
            return
        for pin in self.get_inputs():
            pin.update_state()
        self.operation()

    def cycle_processing(self):
        """Maybe it should become red on the board or smth like that"""

    def destroy(self):
        """additional actions to destroy the circuit, if running out of refferences isn't enough"""


class Board:

    def __init__(self):
        #self.clear()
        self._circuits_list: list[BaseCircuitElement] = []
        self._images_list = []
    
    def add_to_img_list(self, img):
        self._images_list.append(img)

    def clear(self):
        # for el in self._circuits_list:
        #     self.remove_element(el)
        self._circuits_list: list[BaseCircuitElement] = []

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
        self._circuits_list.remove(circuit)
        circuit.destroy()
        self.update_board()

    def create_element(self, circuit_type, inputs=None, outputs=None) -> BaseCircuitElement:
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

        self._circuits_list.append(new_circuit)
        self.update_board()

        return new_circuit

    def get_circuits_list(self) -> list[BaseCircuitElement]:
        return list(self._circuits_list)

    def get_all_pins(self) -> list[Pin]:
        pins_list = []
        for element in self.get_circuits_list():
            for input_pin in element.get_inputs():
                pins_list.append(input_pin)
            for output_pin in element.get_outputs():
                pins_list.append(output_pin)
        return pins_list

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
