from tkinter import Canvas
from unittest import TestCase, main
import os
import sys

root_folder = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
sys.path.append(root_folder)

from board_elements.Fundamentals import Board, BaseCircuitElement
from board_elements.SimpleBoardElements import *


class Test_SBE(TestCase):
    """
    tests for SBE
    """

    def setUp(self):
        """Set up for test functions"""
        self.board = Board(Canvas())
        self.src_A = None
        self.src_B = None
        self.el = None

    def set_board_0(self):
        """x:0"""
        self.src_A = self.board.create_element(ZERO_Generator)
        self.board.connect_pins(
            self.src_A.get_outputs()[0], self.element.get_inputs()[0]
        )

    def set_board_1(self):
        """x:1"""
        self.src_A = self.board.create_element(ONE_Generator)
        self.board.connect_pins(
            self.src_A.get_outputs()[0], self.element.get_inputs()[0]
        )

    def set_board_00(self):
        """xy:00"""
        self.set_board_0()
        self.src_B = self.board.create_element(ZERO_Generator)
        self.board.connect_pins(
            self.src_B.get_outputs()[0], self.element.get_inputs()[1]
        )

    def set_board_01(self):
        """xy:01"""
        self.set_board_0()
        self.src_B = self.board.create_element(ONE_Generator)
        self.board.connect_pins(
            self.src_B.get_outputs()[0], self.element.get_inputs()[1]
        )

    def set_board_10(self):
        """xy:10"""
        self.set_board_1()
        self.src_B = self.board.create_element(ZERO_Generator)
        self.board.connect_pins(
            self.src_B.get_outputs()[0], self.element.get_inputs()[1]
        )

    def set_board_11(self):
        """xy:11"""
        self.set_board_1()
        self.src_B = self.board.create_element(ONE_Generator)
        self.board.connect_pins(
            self.src_B.get_outputs()[0], self.element.get_inputs()[1]
        )

    def case_0(self):
        """case:0"""
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_0()
        self.board.update_board()
        return self.element.get_outputs()[0].get_state()

    def case_1(self):
        """case:1"""
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_1()
        self.board.update_board()
        return self.element.get_outputs()[0].get_state()

    def case_00(self):
        """case:00"""
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_00()
        self.board.update_board()

        return self.element.get_outputs()[0].get_state()

    def case_01(self):
        """case:01"""
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_01()
        self.board.update_board()
        return self.element.get_outputs()[0].get_state()

    def case_10(self):
        """case:10"""
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_10()
        self.board.update_board()
        return self.element.get_outputs()[0].get_state()

    def case_11(self):
        """case:11"""
        self.board.clear()
        self.element = self.board.create_element(self.el)
        self.set_board_11()
        self.board.update_board()
        return self.element.get_outputs()[0].get_state()

    def test_AND_Gate(self):
        """tests AND_Gate"""
        self.el = AND_Gate
        assert [self.case_00(), self.case_01(), self.case_10(), self.case_11()] == [
            False,
            False,
            False,
            True,
        ]

    def test_NAND_Gate(self):
        """tests NAND_Gate"""
        self.el = NAND_Gate
        assert [self.case_00(), self.case_01(), self.case_10(), self.case_11()] == [
            True,
            True,
            True,
            False,
        ]

    def test_OR_Gate(self):
        """tests OR_Gate"""
        self.el = OR_Gate
        assert [self.case_00(), self.case_01(), self.case_10(), self.case_11()] == [
            False,
            True,
            True,
            True,
        ]

    def test_NOR_Gate(self):
        """tests NOR_Gate"""
        self.el = NOR_Gate
        assert [self.case_00(), self.case_01(), self.case_10(), self.case_11()] == [
            True,
            False,
            False,
            False,
        ]

    def test_XOR_Gate(self):
        """tests XOR_Gate"""
        self.el = XOR_Gate
        assert [self.case_00(), self.case_01(), self.case_10(), self.case_11()] == [
            False,
            True,
            True,
            False,
        ]

    def test_XNOR_Gate(self):
        """tests XNOR_Gate"""
        self.el = XNOR_Gate
        assert [self.case_00(), self.case_01(), self.case_10(), self.case_11()] == [
            True,
            False,
            False,
            True,
        ]

    def test_NOT_Gate(self):
        """tests NOT_Gate"""
        self.el = NOT_Gate
        assert [self.case_0(), self.case_1()] == [True, False]


[
    "AND_Gate",
    "NAND_Gate",
    "OR_Gate",
    "NOR_Gate",
    "XOR_Gate",
    "XNOR_Gate",
    "NOT_Gate",
    "ZERO_Generator",
    "ONE_Generator",
    "Lamp",
    "Switch",
    "ClockGenerator",
]
if __name__ == "__main__":
    main()
