import unittest
from board import GameBoard
from character import Character
from map_node import board_node

class TestGameBoard(unittest.TestCase):

    def setUp(self):
        self.game_board = GameBoard()

    # def test_board_size(self):
    #     self.assertEqual(len(self.game_board.board), 9)
    #     self.assertEqual(len(self.game_board.board[0]), 9)

    # def test_board_contents(self):
    #     for row in self.game_board.board:
    #         for cell in row:
    #             self.assertIsInstance(cell, str)

    # def test_place_piece(self):
    #     # Test 1: Placing a piece at a valid coordinate
    #     self.game_board.place_piece(u'\u254F', [1, 1])
    #     self.assertEqual(self.game_board.board[1][1], u'\u254F')

    #     # Test 2: Placing a piece at an invalid coordinate (negative value)
    #     with self.assertRaises(ValueError):
    #         self.game_board.place_piece(u'\u25A0', [-1, 1])

    #     # Test 3: Placing a piece at an invalid coordinate (out of bounds)
    #     with self.assertRaises(ValueError):
    #         self.game_board.place_piece(u'\u25B2', [9, 9])

    #     # Test 4: Placing a piece with an invalid coordinate (not a list of length 2)
    #     with self.assertRaises(ValueError):
    #         self.game_board.place_piece(u'\u25C6', [1, 1, 1])

    #     # Test 5: Placing multiple pieces
    #     self.game_board.place_piece(u'\u25CF', [0, 0])
    #     self.game_board.place_piece(u'\u25CB', [1, 1])
    #     self.game_board.place_piece(u'\u25CA', [2, 2])
    #     self.assertEqual(self.game_board.board[0][0], u'\u25CF')
    #     self.assertEqual(self.game_board.board[1][1], u'\u25CB')
    #     self.assertEqual(self.game_board.board[2][2], u'\u25CA')

    # def test_fight_damage(self):
    #     char1 = Character(strength=20)
    #     char2 = Character()
    #     self.game_board.fight(char1, char2)
    #     self.assertEqual(char2.health, 90)

    # def test_fight_no_damage(self):
    #     char1 = Character(strength=5)
    #     char2 = Character(defense=5)
    #     self.game_board.fight(char1, char2)
    #     self.assertEqual(char2.health, 100)

    # def test_fight_zero_health(self):
    #     char1 = Character(strength=1000)
    #     char2 = Character()
    #     self.game_board.fight(char1, char2)
    #     self.assertEqual(char2.health, 0)
    def test_board_size(self):
        self.assertEqual(len(self.game_board.board), 9)
        for row in self.game_board.board:
            self.assertEqual(len(row), 9)

    def test_node_type(self):
        for row in self.game_board.board:
            for node in row:
                self.assertIsInstance(node, board_node)

    def test_node_coordinates(self):
        random_nodes = [self.game_board.board[2][3], self.game_board.board[5][1], self.game_board.board[8][8]]
        expected_coordinates = [(3, 2), (1, 5), (8, 8)]
        for node, coordinates in zip(random_nodes, expected_coordinates):
            self.assertEqual((node.x, node.y), coordinates)

if __name__ == '__main__':
    unittest.main()