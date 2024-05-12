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
        self.highlighted_cell = [0, 0]

    def update_highlighted_cell(self, row, col):
        self.highlighted_cell = [row, col]

    def move_up(self):
        if self.highlighted_cell[0] > 0:
            self.highlighted_cell[0] -= 1

    def move_down(self):
        if self.highlighted_cell[0] < 8:
            self.highlighted_cell[0] += 1

    def move_left(self):
        if self.highlighted_cell[1] > 0:
            self.highlighted_cell[1] -= 1

    def move_right(self):
        if self.highlighted_cell[1] < 8:
            self.highlighted_cell[1] += 1

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
                return path if len(path) <= moves + 1 else False

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
            for x in range(max(0, unit.x - unit.move - 1), min(9, unit.x + unit.move + 1)):
                for y in range(max(0, unit.y - unit.move - 1), min(9, unit.y + unit.move + 1)):
                    if abs(x - unit.x) + abs(y - unit.y) <= unit.move + 1:
                        node = self.board[y][x]
                        if node.occupant and isinstance(node.occupant, Character) and ((team in ["yellow", "green"] and node.occupant.team == "red") 
                        or (team == "red" and node.occupant.team != team)):
                            predicted_damage = self.predict_fight(unit, node.occupant)
                            adjacent_nodes = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                            reachable_nodes = []
                            for adj_x, adj_y in adjacent_nodes:
                                if 0 <= adj_x < 9 and 0 <= adj_y < 9:
                                    if self.a_star(self.board[unit.y][unit.x], self.board[adj_y][adj_x]):                                      
                                        reachable_nodes.append((adj_x, adj_y))
                            if reachable_nodes:
                                unit_scanned.append([node.occupant, predicted_damage, reachable_nodes])
            scanned_nodes[unit] = unit_scanned

        return scanned_nodes

    
    def predict_fight(self, character1, character2):
        # Check if either character has a weapon equipped
        weapon1 = character1.equipped

        # Calculate damage for character1
        damage1 = character1.strength - character2.defense

        # Add weapon strength to damage if applicable
        if weapon1 and not weapon1.broken:
            damage1 += weapon1.strength

        # Check if character 1 can attack twice
        if character1.speed >= character2.speed + 4:
            num_attacks1 = 2
        else:
            num_attacks1 = 1

        # Predict damage
        predicted_damage = damage1 * num_attacks1

        return predicted_damage
    
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

    def calculate_hit_likelihood(self, character1, character2):
        weapon1 = character1.equipped
        weapon2 = character2.equipped

        # Calculate hit likelihood for character 1
        char1_skill_factor = character1.skill * 0.04  # Weigh character skill heavily
        char1_speed_factor = character1.speed * 0.0225  # Weigh character speed moderately
        weapon1_weight_factor = weapon1.weight * -0.0075 if weapon1 else 0  # Weigh weapon weight lightly negatively
        char2_dodge_factor = character2.speed * -0.015  # Higher character2 speed reduces character1 hit chance
        char1_hit_likelihood = char1_skill_factor + char1_speed_factor + weapon1_weight_factor + char2_dodge_factor
        char1_hit_likelihood = max(0, min(1, char1_hit_likelihood))  # Ensure value is between 0 and 1

        # Calculate hit likelihood for character 2
        char2_skill_factor = character2.skill * 0.04
        char2_speed_factor = character2.speed * 0.0225
        weapon2_weight_factor = weapon2.weight * -0.0075 if weapon2 else 0
        char1_dodge_factor = character1.speed * -0.015
        char2_hit_likelihood = char2_skill_factor + char2_speed_factor + weapon2_weight_factor + char1_dodge_factor
        char2_hit_likelihood = max(0, min(1, char2_hit_likelihood))  # Ensure value is between 0 and 1

        return char1_hit_likelihood, char2_hit_likelihood
    



