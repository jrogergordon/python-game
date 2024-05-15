import unittest
from character import Character

class TestCharacter(unittest.TestCase):
    def test_default_attributes(self):
        character = Character('John')
        self.assertEqual(character.health, 100)
        self.assertEqual(character.strength, 10)
        self.assertEqual(character.speed, 10)
        self.assertEqual(character.defense, 10)

    def test_custom_attributes(self):
        character = Character('John', 150, 20, 15, 12)
        self.assertEqual(character.health, 150)
        self.assertEqual(character.strength, 20)
        self.assertEqual(character.speed, 15)
        self.assertEqual(character.defense, 12)

    def test_partial_custom_attributes(self):
        character = Character('John', health=120, strength=15)
        self.assertEqual(character.health, 120)
        self.assertEqual(character.strength, 15)
        self.assertEqual(character.speed, 10)
        self.assertEqual(character.defense, 10)

    def test_change_attributes(self):
        character = Character('John')
        character.change_health(10)
        character.change_strength(5)
        character.change_speed(-3)
        character.change_defense(2)
        self.assertEqual(character.health, 110)
        self.assertEqual(character.strength, 15)
        self.assertEqual(character.speed, 7)
        self.assertEqual(character.defense, 12)

    def test_level_up(self):
        character = Character('John')
        character.level_up()
        # Since level_up is random, we can't assert specific values.
        # Instead, we'll just check that two attributes have increased.
        increased_attributes = 0
        if character.health > 100:
            increased_attributes += 1
        if character.strength > 10:
            increased_attributes += 1
        if character.speed > 10:
            increased_attributes += 1
        if character.defense > 10:
            increased_attributes += 1
        self.assertEqual(increased_attributes, 2)

if __name__ == '__main__':
    unittest.main()