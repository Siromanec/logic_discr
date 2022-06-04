import unittest
from  Fundamentals import Board
from Advanced_board_elements import ShiftLeft, ShiftRight
from Simple_board_elements import ONE_Generator, ZERO_Generator

from Test_SBE import Test_SBE
class Test_ABE(Test_SBE):
    """

    """
    def setUp(self):
        """Set up for test functions"""
        self.board = Board()

    def set_board_1010(self):

        self.set_board_10()
        self.board.connect_pins(self.src_A.get_outputs()[0], self.element.get_inputs()[2])
        self.board.connect_pins(self.src_B.get_outputs()[0], self.element.get_inputs()[3])

    # def set_shifters(self):
    
    #     self.board.clear()
    #     self.set_board_10()
    #     self.shifter = self.board.create_element(self.el)
    #     self.board.connect_pins(self.src_A.get_outputs()[0], self.shifter.get_inputs()[0])
    #     self.board.connect_pins(self.src_B.get_outputs()[0], self.shifter.get_inputs()[1])
    #     self.board.connect_pins(self.src_A.get_outputs()[0], self.shifter.get_inputs()[2])
    #     self.board.connect_pins(self.src_B.get_outputs()[0], self.shifter.get_inputs()[3])

    def test_ShiftLeft(self):

        self.el = ShiftLeft
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_1010()
        assert [self.element.get_outputs()[i].get_state() for i in range(len(self.element.get_outputs()))] == [False, True, False, False]

    def test_ShiftRight(self):
        """

        """
        self.el = ShiftRight
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_1010()
        assert [self.element.get_outputs()[i].get_state() for i in range(len(self.element.get_outputs()))] == [False, True, False, True]

    def test_2(self):
        """

        """
        pass

    def test_3(self):
        """

        """
        pass


if __name__ == "__main__":
    unittest.main()
