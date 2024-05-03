import unittest
from weapon import Weapon  # assuming the Weapon class is in a file named weapon.py

class TestWeapon(unittest.TestCase):

    def test_default_values(self):
        weapon = Weapon()
        self.assertEqual(weapon.name, "sword")
        self.assertEqual(weapon.usage, 50)
        self.assertEqual(weapon.speed, 5)
        self.assertEqual(weapon.strength, 10)
        self.assertEqual(weapon.broken, 0)

    def test_custom_values(self):
        weapon = Weapon("axe", 100, 10, 20)
        self.assertEqual(weapon.name, "axe")
        self.assertEqual(weapon.usage, 100)
        self.assertEqual(weapon.speed, 10)
        self.assertEqual(weapon.strength, 20)
        self.assertEqual(weapon.broken, 0)

    def test_check_condition(self):
        weapon = Weapon()
        weapon.usage = 0
        weapon.check_condition()
        self.assertEqual(weapon.broken, 1)
        self.assertEqual(weapon.speed, 0)
        self.assertEqual(weapon.strength, 0)

    def test_check_condition_no_change(self):
        weapon = Weapon()
        weapon.check_condition()
        self.assertEqual(weapon.broken, 0)
        self.assertEqual(weapon.speed, 5)
        self.assertEqual(weapon.strength, 10)

if __name__ == "__main__":
    unittest.main()