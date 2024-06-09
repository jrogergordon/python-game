import sys
sys.path.append('/home/jrogergordon/python_game/')

import unittest
from board import GameBoard
from character.character import Character
from mapNode.map_node import board_node
from weapon.weapon import Weapon

class TestGameBoard(unittest.TestCase):

    def setUp(self):
        self.game_board = GameBoard()

    def test_calculate_board_value_empty_board(self):
        self.assertEqual(self.game_board.calculate_board_value("green"), 0)

    def test_calculate_board_value_single_friendly_unit(self):
        friendly_unit = Character(team="green", value=10, health=100, totalHealth=100, x=0, y=0, move=1)
        self.game_board.board[0][0].occupant = friendly_unit
        self.game_board.others = [friendly_unit]
        self.game_board.currTargets = {friendly_unit: []}
        # board value = friendly_unit.value * (friendly_unit.health / friendly_unit.totalHealth) = 10 * (100 / 100) = 10
        self.assertEqual(self.game_board.calculate_board_value("green"), 10)

    def test_calculate_board_value_single_enemy_unit(self):
        enemy_unit = Character(team="red", value=10, health=100, totalHealth=100, x=0, y=0, move=1)
        self.game_board.board[0][0].occupant = enemy_unit
        self.game_board.enemies = [enemy_unit]
        self.game_board.currTargets = {}
        # board value = -enemy_unit.value * (enemy_unit.health / enemy_unit.totalHealth) = -10 * (100 / 100) = -10
        self.assertEqual(self.game_board.calculate_board_value("green"), -10)

    def test_calculate_board_value_multiple_friendly_units(self):
        friendly_unit1 = Character(team="green", value=10, health=100, totalHealth=100, x=0, y=0, move=1)
        friendly_unit2 = Character(team="green", value=20, health=50, totalHealth=100, x=1, y=0, move=1)
        self.game_board.board[0][0].occupant = friendly_unit1
        self.game_board.board[0][1].occupant = friendly_unit2
        self.game_board.others = [friendly_unit1, friendly_unit2]
        self.game_board.currTargets = {friendly_unit1: [], friendly_unit2: []}
        # board value = friendly_unit1.value * (friendly_unit1.health / friendly_unit1.totalHealth) + friendly_unit2.value * (friendly_unit2.health / friendly_unit2.totalHealth) = 10 * (100 / 100) + 20 * (50 / 100) = 10 + 10 = 20
        # placement value for friendly_unit1 = 5 (since friendly_unit2 is within range)
        # placement value for friendly_unit2 = 5 (since friendly_unit1 is within range)
        # total board value = 20 + 5 + 5 = 30
        self.assertEqual(self.game_board.calculate_board_value("green"), 30)

    def test_calculate_board_value_multiple_enemy_units(self):
        enemy_unit1 = Character(team="red", value=10, health=100, totalHealth=100, x=0, y=0, move=1)
        enemy_unit2 = Character(team="red", value=20, health=50, totalHealth=100, x=1, y=0, move=1)
        self.game_board.board[0][0].occupant = enemy_unit1
        self.game_board.board[0][1].occupant = enemy_unit2
        self.game_board.enemies = [enemy_unit1, enemy_unit2]
        self.game_board.currTargets = {}
        # board value = -enemy_unit1.value * (enemy_unit1.health / enemy_unit1.totalHealth) - enemy_unit2.value * (enemy_unit2.health / enemy_unit2.totalHealth) = -10 * (100 / 100) - 20 * (50 / 100) = -10 - 10 = -20
        # placement value for enemy_unit1 = -10 (since enemy_unit2 is within range)
        # placement value for enemy_unit2 = -10 (since enemy_unit1 is within range)
        # total board value = -20 - 10 - 10 = -40
        self.assertEqual(self.game_board.calculate_board_value("green"), -40)

    def test_calculate_board_value_friendly_unit_with_placement_value(self):
        friendly_unit = Character(team="green", value=10, health=100, totalHealth=100, x=0, y=0, move=5)
        enemy_unit = Character(team="red", value=20, health=100, totalHealth=100, x=1, y=0, move=1)
        self.game_board.board[0][0].occupant = friendly_unit
        self.game_board.board[0][1].occupant = enemy_unit
        self.game_board.others = [friendly_unit]
        self.game_board.enemies = [enemy_unit]
        self.game_board.currTargets = {friendly_unit: [[enemy_unit, 0, []]]}
        # board value = friendly_unit.value * (friendly_unit.health / friendly_unit.totalHealth) = 10 * (100 / 100) = 10
        # placement value for friendly_unit = 5 (since enemy_unit is within range)
        # total board value = 10 + 5 = 15
        self.assertEqual(self.game_board.calculate_board_value("green"), 15)

    def test_calculate_board_value_friendly_unit_with_fight_value(self):
        friendly_unit = Character(team="green", value=10, health=100, totalHealth=100, strength=20, x=0, y=0, move=1)
        enemy_unit = Character(team="red", value=20, health=100, totalHealth=100, defense=10, x=1, y=0, move=1)
        self.game_board.board[0][0].occupant = friendly_unit
        self.game_board.board[0][1].occupant = enemy_unit
        self.game_board.others = [friendly_unit]
        self.game_board.enemies = [enemy_unit]
        self.game_board.currTargets = {friendly_unit: [[enemy_unit, 10, []]]}
        # board value = friendly_unit.value * (friendly_unit.health / friendly_unit.totalHealth) = 10 * (100 / 100) = 10
        # fight value for friendly_unit = 10 (since enemy_unit is within range and has a defense of 10)
        # placement value for friendly_unit = 5 (since enemy_unit is within range)
        # total board value = 10 + 10 + 5 = 25
        self.assertEqual(self.game_board.calculate_board_value("green"), 25)

    def test_best_move_no_targets(self):
        game_board = GameBoard()
        game_board.currTargets = {Character(name="Green Friend", team="green"): []}
        best_move = game_board.best_move("green")
        self.assertIsNone(best_move)

    def test_best_move_one_target(self):
        game_board = GameBoard()
        character = Character(name="Green Friend", team="green")
        enemy = Character(name="Red Enemy", team="red")
        game_board.currTargets = {character: [[enemy, 40, [(1, 1)]]]}
        best_move = game_board.best_move("green")
        self.assertIsNotNone(best_move)
        self.assertEqual(best_move[0].name, "Green Friend")
        self.assertEqual(best_move[1], 1)
        self.assertEqual(best_move[2], 1)

    def test_best_move_multiple_targets(self):
        game_board = GameBoard()
        character = Character(name="Green Friend", team="green")
        enemy1 = Character(name="Red Enemy 1", team="red")
        enemy2 = Character(name="Red Enemy 2", team="red")
        game_board.currTargets = {character: [[enemy1, 40, [(1, 1)]], [enemy2, 40, [(3, 3)]]]}
        best_move = game_board.best_move("green")
        self.assertIsNotNone(best_move)
        self.assertEqual(best_move[0].name, "Green Friend")
        self.assertIn(best_move[1], [1, 3])
        self.assertIn(best_move[2], [1, 3])

    def test_best_move_target_out_of_range(self):
        game_board = GameBoard()
        character = Character(name="Green Friend", team="green")
        enemy = Character(name="Red Enemy", team="red")
        game_board.currTargets = {character: [[enemy, 40, []]]}
        best_move = game_board.best_move("green")
        self.assertIsNone(best_move)

    def test_best_move_target_with_higher_value(self):
        game_board = GameBoard()
        character = Character(name="Green Friend", team="green")
        enemy1 = Character(name="Red Enemy 1", team="red", value=10)
        enemy2 = Character(name="Red Enemy 2", team="red", value=20)
        game_board.currTargets = {character: [[enemy1, 40, [(1, 1)]], [enemy2, 40, [(3, 3)]]]}
        best_move = game_board.best_move("green")
        self.assertIsNotNone(best_move)
        self.assertEqual(best_move[0].name, "Green Friend")
        self.assertEqual(best_move[1], 3)
        self.assertEqual(best_move[2], 3)

if __name__ == '__main__':
    unittest.main()