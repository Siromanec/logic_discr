"""custom exceptions"""
class NotEmptyPin(Exception):
    """The pin is allready connected that way"""
class NoSuchPin(Exception):
    """The pin does not exist on the circuit"""
class NoSuchPinInput(NoSuchPin):
    """The input pin does not exist on the circuit"""
class NoSuchPinOutput(NoSuchPin):
    """The output pin does not exist on the circuit"""
class ImpossibleToJoin(Exception):
    """Can't join out/out or in/in"""
class ImpossibleToDisconnect(Exception):
    """Can't disconnect out/out or in/in"""

class ParentAlreadyExistsError(Exception):
    """ParentAlreadyExistsError"""


class NotConnectedCircuitError(Exception):
    """NotConnectedCircuitError"""
