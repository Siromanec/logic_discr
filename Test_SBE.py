from unittest import TestCase, main
from  Fundamentals import Board, BaseCircuitElement
from Simple_board_elements import *

class Test_SBE(TestCase):
    """

    """
    def setUp(self):
        """Set up for test functions"""
        self.board = Board()

    def set_board_0(self):
        self.src_A = self.board.create_element(ZERO_Generator)
        self.board.connect_pins(self.src_A.get_outputs()[0], self.element.get_inputs()[0])


    def set_board_1(self):
        self.src_A = self.board.create_element(ONE_Generator)
        self.board.connect_pins(self.src_A.get_outputs()[0], self.element.get_inputs()[0])


    def set_board_00(self):
        self.set_board_0()
        self.src_B = self.board.create_element(ZERO_Generator)
        self.board.connect_pins(self.src_B.get_outputs()[0], self.element.get_inputs()[1])

    def set_board_01(self):
        self.set_board_0()
        self.src_B = self.board.create_element(ONE_Generator)
        self.board.connect_pins(self.src_B.get_outputs()[0], self.element.get_inputs()[1])

    def set_board_10(self):

        self.set_board_1()
        self.src_B = self.board.create_element(ZERO_Generator)
        self.board.connect_pins(self.src_B.get_outputs()[0], self.element.get_inputs()[1])

    def set_board_11(self):

        self.set_board_1()
        self.src_B = self.board.create_element(ONE_Generator)
        self.board.connect_pins(self.src_B.get_outputs()[0], self.element.get_inputs()[1])

    def case_0(self):
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_0()
        self.board.update_board()
        return self.element.get_outputs()[0].get_state()

    def case_1(self):
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_1()
        self.board.update_board()
        return self.element.get_outputs()[0].get_state()

    def case_00(self):
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_00()
        self.board.update_board()
    
        return self.element.get_outputs()[0].get_state()

    def case_01(self):
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_01()
        self.board.update_board()
    
        return self.element.get_outputs()[0].get_state()

    def case_10(self):
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_10()
        self.board.update_board()
        return self.element.get_outputs()[0].get_state()

    def case_11(self):
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_11()
        self.board.update_board()
        return self.element.get_outputs()[0].get_state()

    def test_AND_Gate(self):
        self.el = AND_Gate
        assert [self.case_00(), self.case_01(), self.case_10(), self.case_11()] == [False, False, False, True]

    def test_NAND_Gate(self):
        self.el = NAND_Gate
        assert [self.case_00(), self.case_01(), self.case_10(), self.case_11()] == [True, True, True, False]

    def test_OR_Gate(self):
        self.el = OR_Gate
        assert [self.case_00(), self.case_01(), self.case_10(), self.case_11()] == [False, True, True, True]

    def test_NOR_Gate(self):
        self.el = NOR_Gate
        assert [self.case_00(), self.case_01(), self.case_10(), self.case_11()] == [True, False, False, False]

    def test_XOR_Gate(self):
        self.el = XOR_Gate
        assert [self.case_00(), self.case_01(), self.case_10(), self.case_11()] == [False, True, True, False]

    def test_XNOR_Gate(self):
        self.el = XNOR_Gate
        assert [self.case_00(), self.case_01(), self.case_10(), self.case_11()] == [True, False, False, True]

    def test_NOT_Gate(self):
        self.el = NOT_Gate
        assert [self.case_0(), self.case_1()] == [True, False]


['AND_Gate', 'NAND_Gate', 'OR_Gate', 'NOR_Gate',
 'XOR_Gate', 'XNOR_Gate', 'NOT_Gate',
 'ZERO_Generator', 'ONE_Generator', 'Lamp', 'Switch',
 'ClockGenerator']
if __name__ == "__main__":
    main()
