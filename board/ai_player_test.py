import sys
sys.path.append('/home/jrogergordon/python_game/')

import unittest
from board import GameBoard
from character.character import Character

class TestAI(unittest.TestCase):
    def setUp(self):
        self.game_board = GameBoard()
        self.ai = self.game_board.ai_green

    def test_populate_units(self):
        self.game_board.others = [Character(team="green")]
        self.ai.populate_units(self.game_board)
        self.assertEqual(self.ai.units, self.game_board.others)

    def test_find_targets_enemy_in_range(self):
        self.game_board.enemies = [Character(name="Red Enemy", x=1, y=1, team="red", move=1, health=100, strength=50, defense=10)]
        self.game_board.board[1][1].occupant = self.game_board.enemies[0]
        self.game_board.others = [Character(name="Green Friend", x=2, y=2, team="green", move=2, health=100, strength=50, defense=10)]
        self.game_board.board[2][2].occupant = self.game_board.others[0]
        self.ai.find_targets(self.game_board)
        for key, values in self.ai.currTargets.items():
            for value in values:
                self.assertEqual(key.name, "Green Friend")
                self.assertEqual(value[0].name, "Red Enemy")
                self.assertEqual(value[1], 40)
                self.assertEqual(value[2], [(2, 1), (1, 2)])

    def test_find_targets_enemy_out_of_range(self):
        self.game_board.enemies = [Character(name="Red Enemy", x=1, y=1, team="red", move=1, health=100, strength=50, defense=10)]
        self.game_board.board[1][1].occupant = self.game_board.enemies[0]
        self.game_board.others = [Character(name="Green Friend", x=4, y=4, team="green", move=2, health=100, strength=50, defense=10)]
        self.game_board.board[4][4].occupant = self.game_board.others[0]
        self.ai.find_targets(self.game_board)
        for key, values in self.ai.currTargets.items():
            for value in values:
                self.assertEqual(key.name, "Green Friend")
                self.assertEqual(value[0].name, "Red Enemy")
                self.assertEqual(value[1], 40)
                self.assertEqual(value[2], [])

    def test_find_targets_enemy_on_edge_of_range(self):
        self.game_board.enemies = [Character(name="Red Enemy", x=4, y=1, team="red", move=1, health=100, strength=50, defense=10)]
        self.game_board.board[1][4].occupant = self.game_board.enemies[0]
        self.game_board.others = [Character(name="Green Friend", x=4, y=4, team="green", move=2, health=100, strength=50, defense=10)]
        self.game_board.board[4][4].occupant = self.game_board.others[0]
        self.ai.find_targets(self.game_board)
        for key, values in self.ai.currTargets.items():
            for value in values:
                self.assertEqual(key.name, "Green Friend")
                self.assertEqual(value[0].name, "Red Enemy")
                self.assertEqual(value[1], 40)
                self.assertEqual(value[2], [(4, 2)])

if __name__ == '__main__':
    unittest.main()