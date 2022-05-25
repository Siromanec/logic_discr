from __future__ import annotations

from exceptions import NoSuchPin, NoSuchPinInput, NoSuchPinOutput, NotEmptyPin

class Pin(object):
    """Represents a singly linked node."""
    def __init__(self, name: str,
                 circuit_self: BaseCircuitElement,
                 circuit_master: BaseCircuitElement=None,
                 circuit_slave: BaseCircuitElement=None,
                 father = None, son = None):
        self.circuit_self = circuit_self
        self.circuit_master = circuit_master
        self.circuit_slave = circuit_slave

        self.name = name
        self.son = son
        self.father = father
    def __str__(self) -> str:
        return f'circuit: {repr(self.circuit_self)}, ' +\
               f'master: {repr(self.circuit_master)}, ' +\
               f'slave: {repr(self.circuit_slave)}; ' +\
               f'name: {repr(self.name)}, ' +\
               f'father: {repr(self.father)}, ' +\
               f'son: {repr(self.son)} '
    def __repr__(self) -> str:
        return repr(self.name)

    def __eq__(self, __o: Pin):
        return self.name == __o.name

    def add_son(self, circuit_slave: BaseCircuitElement, son: Pin):
        if self.son is not None:
            raise NotEmptyPin("The pin is already connected")
        elif not isinstance(son, Pin):
            raise TypeError("You can only connect pins to other pins")
        self.son = son
        self.circuit_slave = circuit_slave
        son.father = self
        son.circuit_master = self.circuit_self
    def add_father(self, circuit_master: BaseCircuitElement, father: Pin):
        if self.father is not None:
            raise NotEmptyPin("The pin is already connected")
        elif not isinstance(father, Pin):
            raise TypeError("You can only connect pins to other pins")
        self.father = father
        self.circuit_master = circuit_master
        father.son = self
        father.circuit_slave = self.circuit_self


    def disconnect(self):
        self.son = None
        self.father = None
        if self.circuit_master:
            self.circuit_master._disconnect_outputs()
        self.circuit_master = None
        if self.circuit_slave:
            self.circuit_slave._disconnect_inputs()
        self.circuit_slave = None



class BaseCircuitElement():
    """
    base circuit element
    can work for gates and electronics
    """
    count = 0

    def __init__(self, name: str, input_pins: tuple[str], output_pins: tuple[str]) -> None:
        self.name = name
        self.input_pins = tuple(Pin(name, self) for name in input_pins)
        self.output_pins = tuple(Pin(name, self) for name in output_pins)

    def __str__(self) -> str:
        connected_circuits_to_inputs = self._connected_circuits_to_inputs()
        connected_circuits_to_outputs = self._connected_circuits_to_outputs()

        info = ''
        info += 'inputs: '
        info += f'{(repr(self.input_pins))}; '
        info += 'connected to: '
        info += f'{(repr(connected_circuits_to_inputs))}. '
        info += 'outputs: '
        info += f'{(repr(self.output_pins))}; '
        info += 'connected to: '
        info += f'{(repr(connected_circuits_to_outputs))}.'




        return info

    def __repr__(self) -> str:
        return self.name


    def _connected_circuits_to_inputs(self) -> list[BaseCircuitElement, None]:
        return list(pin.circuit_master for pin in self.input_pins)


    def _connected_circuits_to_outputs(self) -> list[BaseCircuitElement, None]:
        return list(pin.circuit_slave for pin in self.output_pins)


    def find_input_pin(self, pin_name: str) -> Pin:
        try:
            return next(i for i in self.input_pins if i.name == pin_name) #finds first inctance of pin
        except StopIteration:
            raise NoSuchPinInput('The input pin does not exist on the circuit')


    def find_output_pin(self, pin_name: str) -> Pin:
        try:
            return next(i for i in self.output_pins if i.name == pin_name) #finds first inctance of pin
        except StopIteration:
            raise NoSuchPinOutput('The output pin does not exist on the circuit')


    def connect(self, __o: BaseCircuitElement, pin_self_name: Pin, pin___o_name: Pin):
        """
        :param BaseCircuitElement __o: second element
        :param Pin pin_self_name: name of pin in [self].connect(__o, pin_self_name, pin___o_name)
        :param Pin pin___o_name: name of pin in self.connect([__o], pin_self_name, pin___o_name)

        """
        try:
            pin_self = self.find_input_pin(pin_self_name)
            pin___o = __o.find_output_pin(pin___o_name)
            pin_self.add_father(__o, pin___o)

        except NoSuchPinInput or NoSuchPinOutput:
            pin_self = self.find_output_pin(pin_self_name)
            pin___o = __o.find_input_pin(pin___o_name)
            pin_self.add_son(__o, pin___o)
        except NoSuchPin:
            raise NoSuchPin('The pin does not exist on the circuit')
    def _disconnect_inputs(self):
        for pin in self.input_pins: pin.disconnect()
    def _disconnect_outputs(self):
        for pin in self.output_pins: pin.disconnect(); print(pin)

    def disconnect_all(self):
        """
        DISCONNECT ABSOLUTELY DOESN`T WORK
        needs fixing
        dont't even bother using it
        """
        self._disconnect_inputs()
        self._disconnect_outputs()
    # def disconnect(self):
    #     pass
    @classmethod
    def counter(cls):
        cls.count += 1



class Ground(BaseCircuitElement):

    #count = 0
    def __init__(self) -> None:
        """
        :name [ground{count}]
        :in [0V]
        :out []
        """
        super().__init__(f'ground{self.count}', ('0V', ), ())
        self.counter()
#class Intersection(BaseCircuitElement):
    #def
class Source5V(BaseCircuitElement):

    #count = 0
    def __init__(self) -> None:
        """
        :name [source5V{count}]
        :in []
        :out [5V]
        """
        super().__init__(f'source5V{self.count}', (), ("5V", ))
        self.counter()


class Transistor(BaseCircuitElement):
    r"""
               c|
              / |
          | /
    b_____|
          |_\|
              \ |
               e|
    """
    def __init__(self) -> None:
        """
        transistor
        """
        super.__init__(self, ('base', ), ('emitor', 'collector'))

class GateAND(BaseCircuitElement):
    
    pass
def main():
    grd = Ground()
    s5V = Source5V()
    print(grd)

    grd.connect(s5V, '0V', '5V')
    # circuit1 = BaseCircuitElement('element1',('in','a0'), ('out',))
    # circuit2 = BaseCircuitElement('element2',(), ('out',))
    print(grd)
    #grd.disconnect_all()
    #s5V.disconnect_all()
    print(grd)
    print(s5V)

    # #fix no the same output/output or input/input

    # circuit1.connect(circuit2, "in", "out")

if __name__ == '__main__':
    main()