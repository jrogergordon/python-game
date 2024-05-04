import sys
sys.path.append('/mnt/c/Users/jroge/OneDrive/Desktop/python_game/') 

import unittest
from board import GameBoard
from character.character import Character
from mapNode.map_node import board_node
from weapon.weapon import Weapon

class TestGameBoard(unittest.TestCase):

    def setUp(self):
        self.game_board = GameBoard()

    def test_board_size(self):
        self.assertEqual(len(self.game_board.board), 9)
        self.assertEqual(len(self.game_board.board[0]), 9)

    # def test_board_contents(self):
    #     for row in self.game_board.board:
    #         for cell in row:
    #             self.assertIsInstance(cell, map_node)

    def test_place_piece(self):
        # Test 1: Placing a piece at a valid coordinate
        self.game_board.place_piece(u'\u254F', [1, 1])
        self.assertEqual(self.game_board.board[1][1], u'\u254F')

        # Test 2: Placing a piece at an invalid coordinate (negative value)
        with self.assertRaises(ValueError):
            self.game_board.place_piece(u'\u25A0', [-1, 1])

        # Test 3: Placing a piece at an invalid coordinate (out of bounds)
        with self.assertRaises(ValueError):
            self.game_board.place_piece(u'\u25B2', [9, 9])

        # Test 4: Placing a piece with an invalid coordinate (not a list of length 2)
        with self.assertRaises(ValueError):
            self.game_board.place_piece(u'\u25C6', [1, 1, 1])

        # Test 5: Placing multiple pieces
        self.game_board.place_piece(u'\u25CF', [0, 0])
        self.game_board.place_piece(u'\u25CB', [1, 1])
        self.game_board.place_piece(u'\u25CA', [2, 2])
        self.assertEqual(self.game_board.board[0][0], u'\u25CF')
        self.assertEqual(self.game_board.board[1][1], u'\u25CB')
        self.assertEqual(self.game_board.board[2][2], u'\u25CA')

    def test_fight_damage(self):
        char1 = Character(strength=20)
        char2 = Character()
        self.game_board.fight(char1, char2)
        self.assertEqual(char2.health, 90)

    def test_fight_no_damage(self):
        char1 = Character(strength=5)
        char2 = Character(defense=5)
        self.game_board.fight(char1, char2)
        self.assertEqual(char2.health, 100)

    def test_fight_zero_health(self):
        char1 = Character(strength=1000)
        char2 = Character()
        self.game_board.fight(char1, char2)
        self.assertEqual(char2.health, 0)

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

    def test_impossible_path_obstacles(self):
        character = Character(move=10)
        self.game_board.board[4][4].occupant = character
        start = self.game_board.board[4][4]
        goal = self.game_board.board[8][8]
        for i in range(3, 6):
            for j in range(3, 6):
                if (i, j) != (4, 4):
                    self.game_board.board[i][j].occupant = 1
        self.assertFalse(self.game_board.a_star(start, goal))

    def test_impossible_path_distance(self):
        start = self.game_board.board[0][0]
        character = Character(move=5)
        start.occupant = character
        goal = self.game_board.board[8][8]
        self.assertFalse(self.game_board.a_star(start, goal))

    def test_possible_path_1(self):
        character = Character(move=10)
        start = self.game_board.board[0][0]
        start.occupant = character
        goal = self.game_board.board[2][2]
        path = self.game_board.a_star(start, goal)
        expected_path = [self.game_board.board[0][0], self.game_board.board[1][0], self.game_board.board[2][0], self.game_board.board[2][1], self.game_board.board[2][2]]
        self.assertEqual(path, expected_path)

    def test_possible_path_2(self):
        character = Character(move=10)
        start = self.game_board.board[0][0]
        start.occupant = character
        goal = self.game_board.board[0][8]
        path = self.game_board.a_star(start, goal)
        expected_path = [self.game_board.board[0][0], self.game_board.board[0][1], self.game_board.board[0][2], self.game_board.board[0][3], self.game_board.board[0][4], self.game_board.board[0][5], self.game_board.board[0][6], self.game_board.board[0][7], self.game_board.board[0][8]]
        self.assertEqual(path, expected_path)

    def test_path_length_obstacles(self):
        character = Character(move=10)
        self.game_board.board[4][4].occupant = character
        start = self.game_board.board[4][4]
        goal = self.game_board.board[8][8]
        for i in range(5, 8):
            self.game_board.board[i][4].occupant = 1
        for i in range(3, 6):
            self.game_board.board[6][i].occupant = 1
        for i in range(7, 9):
            self.game_board.board[i][7].occupant = 1
        path = self.game_board.a_star(start, goal)
        self.assertTrue(len(path) <= character.move)

    def test_stop_move_open_menu_empty_inventory(self):
        character = Character()
        self.game_board.board[4][4].occupant = character
        menu_options = self.game_board.stop_move_open_menu(4, 4)
        self.assertEqual(menu_options, ["Wait"])

    def test_stop_move_open_menu_non_empty_inventory(self):
        character = Character(inventory=["item1"])
        self.game_board.board[4][4].occupant = character
        menu_options = self.game_board.stop_move_open_menu(4, 4)
        self.assertEqual(menu_options, ["Wait", "Items"])

    def test_stop_move_open_menu_equipped_item(self):
        character = Character(equipped="item1")
        self.game_board.board[4][4].occupant = character
        menu_options = self.game_board.stop_move_open_menu(4, 4)
        self.assertEqual(menu_options, ["Wait", "Items"])

    def test_stop_move_open_menu_neighbor_occupant(self):
        character = Character()
        self.game_board.board[4][4].occupant = character
        self.game_board.board[4][5].occupant = 1
        menu_options = self.game_board.stop_move_open_menu(4, 4)
        self.assertEqual(menu_options, ["Wait", "Rescue", "Fight", "Shove"])

    def test_scan_area_valid_location(self):
        # Set up a character at location (2, 2) with move distance 1
        self.game_board.board[2][2].occupant = Character(move=1, team="red")
        self.game_board.scan_area((2, 2))
        # Check that nodes within move distance have been updated
        self.assertEqual(self.game_board.board[2][1].show, "")
        self.assertEqual(self.game_board.board[2][3].show, "")
        self.assertEqual(self.game_board.board[1][2].show, "")
        self.assertEqual(self.game_board.board[3][2].show, "")

        # Check that other nodes have not been updated
        self.assertEqual(self.game_board.board[0][0].show, "\u265E")

    def test_scan_area_invalid_location(self):
        # Try scanning an area outside the board
        with self.assertRaises(ValueError):
            self.game_board.scan_area((-1, -1))

    def test_scan_area_no_character(self):
        # Try scanning an area with no character
        with self.assertRaises(ValueError):
            self.game_board.scan_area((2, 2))

    def test_scan_area_different_teams(self):
        # Set up characters of different teams
        self.game_board.board[2][2].occupant = Character(move=1, team="red")
        self.game_board.board[2][1].occupant = Character(team="blue")
        self.game_board.board[2][3].occupant = Character(team="yellow")
        self.game_board.scan_area((2, 2))
        # Check that nodes have been updated correctly
        self.assertEqual(self.game_board.board[2][1].show, "")
        self.assertEqual(self.game_board.board[2][3].show, "")

    def test_scan_area_occupant_types(self):
        # Set up different occupant types
        self.game_board.board[2][2].occupant = Character(move=1, team="red")
        self.game_board.board[2][1].occupant = 0
        self.game_board.board[2][3].occupant = 1
        self.game_board.scan_area((2, 2))
        # Check that nodes have been updated correctly
        self.assertEqual(self.game_board.board[2][1].show, "")
        self.assertEqual(self.game_board.board[2][3].show, "")

    def test_fight_no_weapons(self):
        character1 = Character(strength=10, defense=5, health=100)
        character2 = Character(strength=8, defense=3, health=100)
        self.game_board.fight(character1, character2)
        self.assertEqual(character1.health, 97)  # 100 - (8 - 5)
        self.assertEqual(character2.health, 93)  # 100 - (10 - 3)

    def test_fight_with_weapon(self):
        character1 = Character(strength=10, defense=5, health=100)
        character2 = Character(strength=8, defense=3, health=100)
        weapon = Weapon(strength=5, usage=2, broken=False)
        character1.equipped = weapon
        self.game_board.fight(character1, character2)
        self.assertEqual(character1.health, 97)  # 100 - (8 - 5)
        self.assertEqual(character2.health, 88)  # 100 - (10 + 5 - 3)

    def test_fight_with_broken_weapon(self):
        character1 = Character(strength=10, defense=5, health=100)
        character2 = Character(strength=8, defense=3, health=100)
        weapon = Weapon(strength=5, usage=2, broken=True)
        character1.equipped = weapon
        self.game_board.fight(character1, character2)
        self.assertEqual(character1.health, 97)  # 100 - (8 - 5)
        self.assertEqual(character2.health, 93)  # 100 - (10 - 3)

    def test_fight_with_weapon_usage_0(self):
        character1 = Character(strength=10, defense=5, health=100)
        character2 = Character(strength=8, defense=3, health=100)
        weapon = Weapon(strength=5, usage=0, broken=False)
        character1.equipped = weapon
        self.game_board.fight(character1, character2)
        self.assertEqual(character1.health, 97)  # 100 - (8 - 5)
        self.assertEqual(character2.health, 100)  # No attack due to weapon usage 0

    def test_fight_speed_difference(self):
        character1 = Character(strength=10, defense=5, speed=10, health=100)
        character2 = Character(strength=8, defense=3, speed=6, health=100)
        self.game_board.fight(character1, character2)
        self.assertEqual(character1.health, 97)  # 100 - (8 - 5)
        self.assertEqual(character2.health, 86)  # 100 - (10 - 3) * 2

if __name__ == '__main__':
    unittest.main()