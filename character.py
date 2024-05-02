import random

class Character:
    def __init__(self, name="Joe", health=100, strength=10, speed=10, defense=10, move=5, equip="stick"):
        self.name = name
        self.health = health
        self.strength = strength
        self.speed = speed
        self.defense = defense
        self.move = 5
        self.inventory = []
        self.equipped = equip

    def change_health(self, amount):
        self.health += amount

    def change_strength(self, amount):
        self.strength += amount

    def change_speed(self, amount):
        self.speed += amount

    def change_defense(self, amount):
        self.defense += amount

    def level_up(self):
        skills = ['health', 'strength', 'speed', 'defense']
        random_skills = random.sample(skills, 2)
        for skill in random_skills:
            if skill == 'health':
                self.change_health(10)
            elif skill == 'strength':
                self.change_strength(5)
            elif skill == 'speed':
                self.change_speed(5)
            elif skill == 'defense':
                self.change_defense(5)
        
