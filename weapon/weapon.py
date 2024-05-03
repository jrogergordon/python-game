class Weapon:
    def __init__(self, name="sword", usage=50, speed=5, strength=10, broken=0):
        self.name = name
        self.usage = usage
        self.speed = speed
        self.strength = strength
        self.broken = broken

    def check_condition(self):
        if self.usage == 0:
            self.broken = 1
            self.speed = 0
            self.strength = 0