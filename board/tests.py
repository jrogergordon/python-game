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

    def test_find_targets_enemy_in_range(self):
        self.game_board.enemies = [Character(name="Red Enemy", x=1, y=1, team="red", move=1, health=100, strength=50, defense=10)]
        self.game_board.board[1][1].occupant = self.game_board.enemies[0]
        self.game_board.others = [Character(name="Green Friend", x=2, y=2, team="green", move=2, health=100, strength=50, defense=10)]
        self.game_board.board[2][2].occupant = self.game_board.others[0]
        targets = self.game_board.find_targets("green")
        for key, values in targets.items():
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
        targets = self.game_board.find_targets("green")
        for key, values in targets.items():
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
        targets = self.game_board.find_targets("green")
        for key, values in targets.items():
            for value in values:
                self.assertEqual(key.name, "Green Friend")
                self.assertEqual(value[0].name, "Red Enemy")
                self.assertEqual(value[1], 40)
                self.assertEqual(value[2], [(4, 2)])

    def test_find_targets_enemy_with_only_one_reachable_node(self):
        self.game_board.enemies = [Character(name="Red Enemy", x=1, y=1, team="red", move=1, health=100, strength=50, defense=10)]
        self.game_board.board[1][1].occupant = self.game_board.enemies[0]
        self.game_board.others = [Character(name="Green Friend", x=3, y=1, team="green", move=2, health=100, strength=50, defense=10)]
        self.game_board.board[1][3].occupant = self.game_board.others[0]
        targets = self.game_board.find_targets("green")
        for key, values in targets.items():
            for value in values:
                self.assertEqual(key.name, "Green Friend")
                self.assertEqual(value[0].name, "Red Enemy")
                self.assertEqual(value[1], 40)
                self.assertEqual(value[2], [(2, 1)])

    def test_equal_characters(self):
        character1 = Character()
        character2 = Character()
        weapon1 = Weapon()
        weapon2 = Weapon()
        character1.equipped = weapon1
        character2.equipped = weapon2
        likelihood1, likelihood2 = self.game_board.calculate_hit_likelihood(character1, character2)
        self.assertAlmostEqual(likelihood1, 0.0675)
        self.assertAlmostEqual(likelihood2, 0.0675)

    def test_character_with_higher_skill(self):
        character1 = Character(skill=20)
        character2 = Character()
        weapon1 = Weapon()
        weapon2 = Weapon()
        character1.equipped = weapon1
        character2.equipped = weapon2
        likelihood1, likelihood2 = self.game_board.calculate_hit_likelihood(character1, character2)
        self.assertGreater(likelihood1, likelihood2)

    def test_character_with_higher_speed(self):
        character1 = Character(speed=20)
        character2 = Character()
        weapon1 = Weapon()
        weapon2 = Weapon()
        character1.equipped = weapon1
        character2.equipped = weapon2
        likelihood1, likelihood2 = self.game_board.calculate_hit_likelihood(character1, character2)
        self.assertGreater(likelihood1, likelihood2)

    def test_weapon_with_higher_speed(self):
        character1 = Character()
        character2 = Character()
        weapon1 = Weapon(speed=10)
        weapon2 = Weapon()
        character1.equipped = weapon1
        character2.equipped = weapon2
        likelihood1, likelihood2 = self.game_board.calculate_hit_likelihood(character1, character2)
        self.assertEqual(likelihood1, likelihood2)  # Corrected: weapon speed is not considered in hit likelihood

    def test_character_with_lower_weight_weapon(self):
        character1 = Character()
        character2 = Character()
        weapon1 = Weapon(weight=0)
        weapon2 = Weapon(weight=5)
        character1.equipped = weapon1
        character2.equipped = weapon2
        likelihood1, likelihood2 = self.game_board.calculate_hit_likelihood(character1, character2)
        self.assertGreater(likelihood1, likelihood2)


if __name__ == '__main__':
    unittest.main()