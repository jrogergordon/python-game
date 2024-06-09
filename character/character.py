import random

class Character:
    def __init__(self, name="Joe", totalHealth=100, health=100, strength=10, speed=10, defense=10, skill=0, move=5, inventory=[], equipped="", show="\u265E", team="blue", x=0, y=0, value=0, used=0):
        self.name = name
        self.totalHealth = totalHealth
        self.health = health
        self.strength = strength
        self.speed = speed
        self.defense = defense
        self.skill = skill
        self.move = move
        self.inventory = inventory
        self.equipped = equipped
        self.show = show
        self.team = team
        self.x = x
        self.y = y
        self.value = value
        self.used = used

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
        
