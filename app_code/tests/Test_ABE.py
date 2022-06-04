import unittest
import os
import sys


root_folder = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(root_folder)
from board_elements.Fundamentals import Board
from board_elements.AdvancedBoardElements import *
from board_elements.SimpleBoardElements import ONE_Generator, ZERO_Generator

from Test_SBE import Test_SBE


class Test_ABE(Test_SBE):
    """testind advanced circuit elements"""

    def setUp(self):
        """Set up for test functions"""
        self.board = Board()

    def set_board_1010(self):

        self.set_board_10()
        self.board.connect_pins(
            self.src_A.get_outputs()[0], self.element.get_inputs()[2]
        )
        self.board.connect_pins(
            self.src_B.get_outputs()[0], self.element.get_inputs()[3]
        )

    def set_board_10101010(self):

        self.set_board_10()
        self.board.connect_pins(
            self.src_A.get_outputs()[0], self.element.get_inputs()[2]
        )
        self.board.connect_pins(
            self.src_B.get_outputs()[0], self.element.get_inputs()[3]
        )
        self.board.connect_pins(
            self.src_A.get_outputs()[0], self.element.get_inputs()[4]
        )
        self.board.connect_pins(
            self.src_B.get_outputs()[0], self.element.get_inputs()[5]
        )
        self.board.connect_pins(
            self.src_A.get_outputs()[0], self.element.get_inputs()[6]
        )
        self.board.connect_pins(
            self.src_B.get_outputs()[0], self.element.get_inputs()[7]
        )

    def set_board_01010101(self):
        self.set_board_01()
        self.board.connect_pins(
            self.src_A.get_outputs()[0], self.element.get_inputs()[2]
        )
        self.board.connect_pins(
            self.src_B.get_outputs()[0], self.element.get_inputs()[3]
        )
        self.board.connect_pins(
            self.src_A.get_outputs()[0], self.element.get_inputs()[4]
        )
        self.board.connect_pins(
            self.src_B.get_outputs()[0], self.element.get_inputs()[5]
        )
        self.board.connect_pins(
            self.src_A.get_outputs()[0], self.element.get_inputs()[6]
        )
        self.board.connect_pins(
            self.src_B.get_outputs()[0], self.element.get_inputs()[7]
        )

    def set_board_010(self):

        self.set_board_01()
        self.board.connect_pins(
            self.src_A.get_outputs()[0], self.element.get_inputs()[2]
        )

    # def set_shifters(self):

    #     self.board.clear()
    #     self.set_board_10()
    #     self.shifter = self.board.create_element(self.el)
    #     self.board.connect_pins(self.src_A.get_outputs()[0], self.shifter.get_inputs()[0])
    #     self.board.connect_pins(self.src_B.get_outputs()[0], self.shifter.get_inputs()[1])
    #     self.board.connect_pins(self.src_A.get_outputs()[0], self.shifter.get_inputs()[2])
    #     self.board.connect_pins(self.src_B.get_outputs()[0], self.shifter.get_inputs()[3])

    def test_ShiftLeft(self):
        """Testing left shifter"""
        self.el = ShiftLeft
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_1010()
        self.assertEqual(
            [
                self.element.get_outputs()[i].get_state()
                for i in range(len(self.element.get_outputs()))
            ],
            [False, True, False, False],
        )

    def test_ShiftRight(self):
        """Testing left shifter"""
        self.el = ShiftRight
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_1010()
        self.assertEqual(
            [
                self.element.get_outputs()[i].get_state()
                for i in range(len(self.element.get_outputs()))
            ],
            [False, True, False, True],
        )

    def test_HalfAdder(self):
        """Testing half adder"""
        self.el = HalfAdder
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_11()
        self.assertEqual(
            [
                self.element.get_outputs()[i].get_state()
                for i in range(len(self.element.get_outputs()))
            ],
            [False, True],
        )

    def test_Adder(self):
        """Testing adder"""
        self.el = Adder
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_010()
        self.assertEqual(
            [
                self.element.get_outputs()[i].get_state()
                for i in range(len(self.element.get_outputs()))
            ],
            [True, False],
        )

    def test_HalfSubstractor(self):
        """Testing half substractor"""
        self.el = HalfSubstractor
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_10()
        self.assertEqual(
            [
                self.element.get_outputs()[i].get_state()
                for i in range(len(self.element.get_outputs()))
            ],
            [True, False],
        )

    def test_Substractor(self):
        """Testing substractor"""
        self.el = Substractor
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_010()
        self.assertEqual(
            [
                self.element.get_outputs()[i].get_state()
                for i in range(len(self.element.get_outputs()))
            ],
            [True, True],
        )

    def test_Decoder(self):
        """Testing decoder"""
        self.el = Decoder
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_010()
        self.assertEqual(
            [
                self.element.get_outputs()[i].get_state()
                for i in range(len(self.element.get_outputs()))
            ],
            [False, False, False, False, False, True, False, False],
        )

    def test_Encoder_4_to_2(self):
        """Testing 4-to-2 encoder"""
        self.el = Encoder_4_to_2
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_1010()
        self.assertEqual(
            [
                self.element.get_outputs()[i].get_state()
                for i in range(len(self.element.get_outputs()))
            ],
            [True, True, True],
        )

    def test_Encoder_8_to_3(self):
        """Testing 4-to-2 encoder"""
        self.el = Encoder_8_to_3
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_01010101()
        self.assertEqual(
            [
                self.element.get_outputs()[i].get_state()
                for i in range(len(self.element.get_outputs()))
            ],
            [True, True, False, True],
        )


if __name__ == "__main__":
    unittest.main()

