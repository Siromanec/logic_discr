import unittest
from  Fundamentals import Board
from Advanced_board_elements import ShiftLeft
from Simple_board_elements import ONE_Generator, ZERO_Generator


class Test_ABE(unittest.TestCase):
    """

    """
    def setUp(self):
        """Set up for test functions"""
        self.board = Board()
        self.one = self.board.create_element(ONE_Generator)
        self.zero = self.board.create_element(ZERO_Generator)
        self.shifter = self.board.create_element(ShiftLeft)

    def test_1(self):
        """

        """
        self.board.connect_pins(self.one.get_outputs()[0], self.shifter.get_inputs()[0])
        self.board.connect_pins(self.zero.get_outputs()[0], self.shifter.get_inputs()[1])
        self.board.connect_pins(self.one.get_outputs()[0], self.shifter.get_inputs()[2])
        self.board.connect_pins(self.zero.get_outputs()[0], self.shifter.get_inputs()[3])
        self.assertEqual(self.shifter.get_outputs() == ["Correct answer here"])

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
