from __future__ import annotations

from exceptions import *
class Pin():
    def __init__(self, circuit: BaseCircuitElement,
                 father: Pin or None=None, children: list[Pin]=[],
                 input_pin: bool=True, signal: bool=None) -> None:
        self.circuit = circuit
        self.father = father
        self.children = children
        self.input_pin = input_pin
        self.signal = signal
    def change_signal(self, val: bool):
        self.signal = val
        #does not work properly so use self.father.signal
        if not self.input_pin:
            for child in self.children:
                child.signal = val
    def add_father(self, father: Pin):
        self.father = father
        father.children.append(self)

    def add_son(self, son: Pin):
        son.add_father(self)

    def del_son(self, son: Pin):
        self.children.remove(son)
        son.father = None

    def del_father(self):
        self.father.del_son(self)

    def __str__(self) -> str:
        return ' '.join(('gate:',
                         repr(self.circuit),
                         'father:',
                         repr(self.father),
                         'children:',
                         repr(self.children)))
    def __repr__(self):
        return repr(self.circuit)

    def __eq__(self, __o: Pin) -> bool:
        """all pins are unique"""
        return id(self) == id(__o)





class BaseCircuitElement():
    """
    base circuit element
    can work for gates and electronics
    """

    def __init__(self, input_pins_amount: int, output_pins_amount: int=1) -> None:
        self.input_pins = tuple(Pin(self) for i in range(input_pins_amount))
        self.output_pins = tuple(Pin(self, input_pin=False) for i in range(output_pins_amount))


    def connect(self, pin_self: Pin, pin___o: Pin):
        """
        use:
        self.connect(self.input_pins[x], other.output_pins[y])
        self.input_pins[x] # desired input pin at position x of self gate
        other.output_pins[y] # desired output pin at position y [default is 0] of the other gate
        |works the other way around too|
        """
        if pin_self.input_pin and not pin___o.input_pin:
            pin_self.add_father(pin___o)
        elif not pin_self.input_pin and pin___o.input_pin:
            pin_self.add_son(pin___o)
        else:
            raise ImpossibleToJoin("Can't join out/out or in/in")
    def disconnect(self, pin_self: Pin, pin___o: Pin):
        # i don't remember if it works
        if pin_self.input_pin and not pin___o.input_pin:
            pin_self.del_father()
        elif not pin_self.input_pin and pin___o.input_pin:
            pin_self.del_son(pin___o)
        else:
            raise ImpossibleToDisconnect("Can't disconnect out/out or in/in")


    def __str__(self) -> str:
        return ' '.join((repr(self), 'input:', repr(self.input_pins), 'output:', repr(self.output_pins)))

    def __repr__(self) -> str:
        return self.__class__.__name__
#if we want to send signal from gates we either build multiple trees of order of operations or make the gates send signals by themselves
class AND_Gate(BaseCircuitElement):
    def __init__(self) -> None:
        super().__init__(2, 1)
    def operation(self):
        if self.input_pins[0].signal is not None and self.input_pins[1].signal is not None:
            self.output_pins[0].change_signal(self.input_pins[0].father.signal and self.input_pins[1].father.signal)

class NAND_Gate(BaseCircuitElement):
    def __init__(self) -> None:
        super().__init__(2, 1)
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

class ZERO_Generator(BaseCircuitElement):
    def __init__(self) -> None:
        super().__init__(0, 1)
    def operation(self):
        self.output_pins[0].change_signal(False)

class ONE_Generator(BaseCircuitElement):
    def __init__(self) -> None:
        super().__init__(0, 1)
    def operation(self):
        self.output_pins[0].change_signal(True)

class Lamp(BaseCircuitElement):
    def __init__(self) -> None:
        super().__init__(1, 0)
    def operation(self):
        if self.input_pins[0].signal:
            print("shine")
        else:
            print('not shine')

def main():
    one1  = ONE_Generator()
    one2  = ONE_Generator()

    zero = ZERO_Generator()

    and_gate = AND_Gate()

    lamp = Lamp()

    one1.connect(one1.output_pins[0], and_gate.input_pins[0])
    one2.connect(one2.output_pins[0], and_gate.input_pins[1])


    and_gate.connect(and_gate.output_pins[0], lamp.input_pins[0])

    one1.operation()
    one2.operation()


    and_gate.operation()

    lamp.operation()

if __name__ == '__main__':
    main()