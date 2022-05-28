from unittest import TestCase, main
from Fundamentals import Pin, InputPin, OutputPin
from Fundamentals import Board
from Fundamentals import BaseCircuitElement
from exceptions import *
class TestFund(TestCase):
    def test_BCE(self):

        self.board = Board()

        self.circuitA = BaseCircuitElement(self.board, 2, 1)
        self.circuitB = BaseCircuitElement(self.board, 2, 1)
        self.board.circuits_list.append(self.circuitA)
        self.board.circuits_list.append(self.circuitB)

        self.assertNotEqual(self.circuitA, self.circuitB)


        self.assertEqual("BaseCircuitElement() inputs Id's: [0, 1] outputs Id's: [2]", str(self.circuitA))
        self.assertEqual(self.circuitA.get_board(), self.board)
        self.board.connect_pins(self.circuitA._output_pins[0], self.circuitB._input_pins[0])
        self.assertEqual(self.circuitA.get_dependent_circuits()[0], self.circuitB)
        self.assertEqual(self.circuitB.get_parent_circuits()[0], self.circuitA)

        self.assertFalse(self.circuitA.is_fully_connected())
        #self.board.remove_element(self.circuitA)

    def test_pins(self):
        self.board = Board()
        self.circuitA = BaseCircuitElement(self.board, 2, 1)
        self.circuitB = BaseCircuitElement(self.board, 2, 1)

        self.pinA  = InputPin(self.circuitA)
        self.pinB  = OutputPin(self.circuitB)

        with self.assertRaises(ValueError) as context:
            self.pinA.set_parent(self.pinA)
        self.assertTrue("Incorrect pin type!" in str(context.exception))

        with self.assertRaises(ValueError) as context:
            self.pinB.add_child(self.pinB)
        self.assertTrue("A child can only be an InputPin" in str(context.exception))

        self.pinA.set_parent(self.pinB)
        
        self.pinB.add_child(self.pinA)

        self.assertEqual(self.pinA._parent, self.pinB)
        self.assertEqual(self.pinB._children[0], self.pinA)

        self.assertFalse(self.pinB.get_state())

        with self.assertRaises(ValueError) as  context:
            self.pinB.set_state(1322)
        self.assertTrue("Incorrect value for a pin state!" in str(context.exception))
        
        self.pinB.update_state(True)
        self.pinA.update_state()
        self.assertTrue(self.pinB.get_state())
        self.assertTrue(self.pinA.get_state())
        self.assertEqual(("type: OutputPin id: 13 gate: BaseCircuitElement() " +
                          "state: True children: [InputPin(id=12, parent=13, gate=BaseCircuitElement() "+
                          "inputs Id's: [6, 7] outputs Id's: [8], state=True)]"), str(self.pinB))
        self.assertEqual(("type: InputPin id: 12 gate: BaseCircuitElement() " +
                          "state: True parent: OutputPin(id=13, childrenId=[12], " +
                          "gate=BaseCircuitElement(), state=True)"), str(self.pinA))

        self.assertEqual(self.pinB.get_children(), [self.pinA])
        self.pinB.remove_child(self.pinA)
        self.pinA.remove_parent()
        self.assertIsNone(self.pinA._parent)
        self.assertEqual(self.pinB.get_children(), [])
        self.assertNotEqual(self.pinA, self.pinB)
        self.assertEqual(hash(self.pinA), 12)
        del self.pinB
        del self.pinA



        pass
if __name__ == '__main__':
    main()