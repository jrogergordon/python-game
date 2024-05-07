import sys
sys.path.append('/mnt/c/Users/jroge/OneDrive/Desktop/python_game/') 

from mapNode.map_node import board_node
from character.character import Character

class GameBoard:
    def __init__(self, max=9, players=[], enemies=[], other=[], ally=[]):
        self.board = self.create_board()
        self.max = max
        self.players = players
        self.enemies = enemies
        self.others = other
        self.ally = ally

    def create_board(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                node = board_node(0, 0, None, j, i, 0)  # x is j, y is i
                row.append(node)
            board.append(row)
        return board

    def display_board(self):
        print('  1 2 3 4 5 6 7 8 9')
        for i, row in enumerate(self.board, start=1):
            row_show = []
            for node in row:
                if node.occupant != 0:
                    row_show.append(node.occupant.show)
                else:
                    row_show.append(node.show)
            print(f'{i} ' + ' '.join(row_show))

    def place_piece(self, piece, coordinate):
        if len(coordinate) != 2:
            raise ValueError("Coordinate must be a list of length 2")
        x, y = coordinate
        if x < 0 or y < 0:
            raise ValueError("Coordinate values must be non-negative")
        # Assuming self.board is a 2D list representing the game board
        if x >= len(self.board) or y >= len(self.board[0]):
            raise ValueError("Coordinate out of bounds")
        self.board[x][y] = piece

    def fight(self, character1, character2):
        # Check if either character has a weapon equipped
        weapon1 = character1.equipped
        weapon2 = character2.equipped

        # Calculate damage for each character
        damage1 = character1.strength - character2.defense
        damage2 = character2.strength - character1.defense

        # Add weapon strength to damage if applicable
        if weapon1 and not weapon1.broken:
            damage1 += weapon1.strength
        if weapon2 and not weapon2.broken:
            damage2 += weapon2.strength

        # Check if character 1 can attack twice
        if character1.speed >= character2.speed + 4:
            num_attacks1 = 2
        else:
            num_attacks1 = 1

        # Check if character 2 can attack twice
        if character2.speed >= character1.speed + 4:
            num_attacks2 = 2
        else:
            num_attacks2 = 1

        # Perform attacks
        for _ in range(num_attacks1):
            if weapon1 and weapon1.usage == 0:
                break
            if damage1 > 0:
                if damage1 > character2.health:
                    character2.health = 0
                else:
                    character2.change_health(-damage1)
            if weapon1:
                weapon1.usage -= 1
                if weapon1.usage < 0:
                    weapon1.usage = 0

        for _ in range(num_attacks2):
            if weapon2 and weapon2.usage == 0:
                break
            if damage2 > 0:
                if damage2 > character1.health:
                    character1.health = 0
                else:
                    character1.change_health(-damage2)
            if weapon2:
                weapon2.usage -= 1
                if weapon2.usage < 0:
                    weapon2.usage = 0

    def a_star(self, start, goal):
        moves = start.occupant.move
        open_list = [start]
        came_from = {}
        g_score = {node: float('inf') for row in self.board for node in row}
        g_score[start] = 0
        f_score = {node: float('inf') for row in self.board for node in row}
        f_score[start] = self.heuristic(start, goal)

        while open_list:
            current = min(open_list, key=lambda node: f_score[node])
            if current == goal:
                path = self.reconstruct_path(came_from, current)
                return path if len(path) <= moves else False

            open_list.remove(current)
            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    if neighbor not in open_list:
                        open_list.append(neighbor)

        return False

    def heuristic(self, node, goal):
        return abs(node.x - goal.x) + abs(node.y - goal.y)

    def get_neighbors(self, node):
        neighbors = []
        for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = node.x + x, node.y + y
            if 0 <= new_x < 9 and 0 <= new_y < 9:
                neighbor = self.board[new_y][new_x]
                if neighbor.occupant == 0:
                    neighbors.append(neighbor)
        return neighbors

    def reconstruct_path(self, came_from, current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.insert(0, current)
        return total_path

    def stop_move_open_menu(self, x, y):
        character = self.board[y][x].occupant
        menu_options = ["Wait"]

        if character.inventory or character.equipped:
            menu_options.append("Items")

        neighbor_nodes = [
            (x-1, y) if x > 0 else None,
            (x+1, y) if x < len(self.board[0]) - 1 else None,
            (x, y-1) if y > 0 else None,
            (x, y+1) if y < len(self.board) - 1 else None
        ]

        for node in neighbor_nodes:
            if node and self.board[node[1]][node[0]].occupant != 0:
                menu_options.extend(["Rescue", "Fight", "Shove"])
                break

        return menu_options

    def scan_area(self, location):
        x, y = location
        if not isinstance(self.board[y][x].occupant, Character):
            raise ValueError("Location is not a character")
        character = self.board[y][x].occupant
        move_distance = character.move

        min_x = max(0, x - move_distance)
        max_x = min(len(self.board) - 1, x + move_distance)
        min_y = max(0, y - move_distance)
        max_y = min(len(self.board[0]) - 1, y + move_distance)

        for j in range(min_x, max_x + 1):
            for i in range(min_y, max_y + 1):
                node = self.board[i][j]

                if isinstance(node.occupant, Character):
                    if node.occupant.team == "red":
                        node.show = ""
                    elif node.occupant.team == "blue":
                        node.show = ""
                    elif node.occupant.team == "yellow":
                        node.show = ""
                elif node.occupant == 0:
                    node.show = ""
                elif node.occupant == 1:
                    node.show = ""

    def find_targets(self, team):
        if team == "green":
            group = self.others
        elif team == "yellow":
            group = self.ally
        else:
            group = self.enemies

        scanned_nodes = {}
        
        for unit in group:
            unit_scanned = []
            for x in range(max(0, unit.x - unit.move), min(9, unit.x + unit.move + 1)):
                for y in range(max(0, unit.y - unit.move), min(9, unit.y + unit.move + 1)):
                    if x == 4 and y == 1: print("made it")
                    if abs(x - unit.x) + abs(y - unit.y) <= unit.move:
                        node = self.board[y][x]
                        if node.occupant and isinstance(node.occupant, Character) and ((team in ["yellow", "green"] and node.occupant.team == "red") or (team == "red" and node.occupant.team != team)):
                            adjacent_nodes = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                            reachable_nodes = []
                            for adj_x, adj_y in adjacent_nodes:
                                if 0 <= adj_x < 9 and 0 <= adj_y < 9:
                                    if self.a_star(self.board[unit.y][unit.x], self.board[adj_y][adj_x]):
                                        reachable_nodes.append((adj_y, adj_x))
                            if reachable_nodes:
                                unit_scanned.append([node.occupant, reachable_nodes])
            scanned_nodes[unit] = unit_scanned

        return scanned_nodes
    
# Test 1: Enemy in range
game = GameBoard()
game.enemies = [Character(name="Red Enemy", x=1, y=1, team="red", move=1)]
game.board[1][1].occupant = game.enemies[0]
game.others = [Character(name="Green Friend", x=2, y=2, team="green", move=2)]
game.board[2][2].occupant = game.others[0]
print("Test 1: Enemy in range")
targets = game.find_targets("green")
for key, values in targets.items():
    for value in values:
        print(f"{key.name}: {value[0].name}, {value[1]}")

# Test 2: Enemy out of range
game = GameBoard()
game.enemies = [Character(name="Red Enemy", x=1, y=1, team="red", move=1)]
game.board[1][1].occupant = game.enemies[0]
game.others = [Character(name="Green Friend", x=4, y=4, team="green", move=2)]
game.board[4][4].occupant = game.others[0]
print("Test 2: Enemy out of range")
targets = game.find_targets("green")
for key, values in targets.items():
    for value in values:
        print(f"{key.name}: {value[0].name}, {value[1]}")

# Test 3: Enemy on edge of range
game = GameBoard()
game.enemies = [Character(name="Red Enemy", x=4, y=1, team="red", move=1)]
game.board[1][4].occupant = game.enemies[0]
game.others = [Character(name="Green Friend", x=4, y=4, team="green", move=2)]
game.board[4][4].occupant = game.others[0]
print("Test 3: Enemy on edge of range")
targets = game.find_targets("green")
for key, values in targets.items():
    for value in values:
        print(f"{key.name}: {value[0].name}, {value[1]}")

# # Test 4: Enemy with only one reachable node
# game = GameBoard()
# game.enemies = [Character(name="Red Enemy", x=1, y=1, team="red", move=1)]
# game.board[1][1].occupant = game.enemies[0]
# game.others = [Character(name="Green Friend", x=3, y=1, team="green", move=2)]
# game.board[3][1].occupant = game.others[0]
# print("Test 4: Enemy with only one reachable node")
# targets = game.find_targets("green")
# for key, values in targets.items():
#     for value in values:
#         print(f"{key.name}: {value[0].name}, {value[1]}")



