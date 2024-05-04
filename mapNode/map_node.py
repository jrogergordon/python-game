class board_node:
    def __init__(self, h, g, parent, x, y, obstacle=0, show='\u265E'):
        self.h = h
        self.g = g
        self.parent = parent
        self.x = x
        self.y = y
        self.occupant = obstacle
        self.show = show