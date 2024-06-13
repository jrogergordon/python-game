import sys
sys.path.append('/home/jrogergordon/python_game/') 

from character.character import Character

class AI:
    def __init__(self, team):
        self.team = team
        self.units = []
        self.boardValueBreakdown = {}
        self.currTargets = {}

    def populate_units(self, game_board):
        if self.team == "green":
            self.units = game_board.others
        elif self.team == "yellow":
            self.units = game_board.ally
        else:
            self.units = game_board.enemies

    def calculate_placement_value(self, unit, friendly_units, enemy_units, game_board):
        placement_value = 0
        for enemy_unit in enemy_units:
            if game_board.a_star(game_board.board[unit.y][unit.x], game_board.board[enemy_unit.y][enemy_unit.x]):
                if enemy_unit.value > unit.value:   
                    placement_value -= 10
                else:
                    placement_value += 5

        for friendly_unit in friendly_units:
            if friendly_unit != unit and game_board.a_star(game_board.board[unit.y][unit.x], game_board.board[friendly_unit.y][friendly_unit.x]):
                if friendly_unit.value > unit.value:
                    placement_value += 5
                else:
                    placement_value += 2
        return placement_value

    def best_move(self, game_board):
        best_move = None
        best_move_value = float('-inf')
        for unit in self.units:
            targets = self.currTargets[unit]
            for target in targets:
                enemy_unit = target[0]
                fight_value = target[1]
                # Use the enemy's position instead of the first reachable node
                node = (enemy_unit.x, enemy_unit.y)
                # Imitate the move happening
                old_x, old_y = unit.x, unit.y
                unit.x, unit.y = node
                # Calculate the expected fight value
                expected_fight_value = game_board.calculate_expected_fight_value(unit, enemy_unit)
                # Imitate the fight happening
                old_health1, old_health2 = unit.health, enemy_unit.health
                game_board.fight(unit, enemy_unit)
                health_change1 = unit.health - old_health1
                health_change2 = enemy_unit.health - old_health2
                # Calculate the value of the health change
                health_change_value = (health_change1 / unit.totalHealth) * unit.value + (health_change2 / enemy_unit.totalHealth) * enemy_unit.value
                # Calculate the placement value
                placement_value = self.calculate_placement_value(unit, self.units, game_board.enemies if self.team != "red" else game_board.player + game_board.ally + game_board.others, game_board)
                # Undo the move and the fight
                unit.x, unit.y = old_x, old_y
                unit.health, enemy_unit.health = old_health1, old_health2
                # Check if this move is the best so far
                if placement_value + expected_fight_value + health_change_value > best_move_value:
                    best_move_value = placement_value + expected_fight_value + health_change_value
                    best_move = (unit, node[0], node[1])
        return best_move
    
    def find_targets(self, game_board):
        if self.team == "green":
            group = game_board.others
        elif self.team == "yellow":
            group = game_board.ally
        else:
            group = game_board.enemies
        scanned_nodes = {}
    
        for unit in group:
            unit_scanned = []
            for x in range(max(0, unit.x - unit.move - 1), min(9, unit.x + unit.move + 1)):
                for y in range(max(0, unit.y - unit.move - 1), min(9, unit.y + unit.move + 1)):
                    if abs(x - unit.x) + abs(y - unit.y) <= unit.move + 1:
                        node = game_board.board[y][x]
                        if node.occupant and isinstance(node.occupant, Character) and ((self.team in ["yellow", "green"] and node.occupant.team == "red") 
                        or (self.team == "red" and node.occupant.team != self.team)):
                            expected_fight_value = game_board.calculate_expected_fight_value(unit, node.occupant)
                            adjacent_nodes = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                            reachable_nodes = []
                            for adj_x, adj_y in adjacent_nodes:
                                if 0 <= adj_x < 9 and 0 <= adj_y < 9: 
                                    if game_board.a_star(game_board.board[unit.y][unit.x], game_board.board[adj_y][adj_x]):                                      
                                        reachable_nodes.append((adj_x, adj_y))
                            if reachable_nodes:
                                unit_scanned.append([node.occupant, expected_fight_value, reachable_nodes])
            scanned_nodes[unit] = unit_scanned
    
        self.currTargets = scanned_nodes

    def calculate_board_value(self, game_board):
        if self.team == "green":
            current_units = game_board.others
        elif self.team == "yellow":
            current_units = game_board.ally
        else:
            current_units = game_board.enemies
        friendly_units = game_board.player + game_board.ally + game_board.others if self.team != "red" else game_board.enemies
        enemy_units = game_board.enemies if self.team != "red" else game_board.player + game_board.ally + game_board.others
        board_value = 0
        board_value_breakdown = {}
        for unit in current_units:
            board_value_breakdown[unit] = {}
            unit_value = unit.value * (unit.health / unit.totalHealth)
            board_value_breakdown[unit]["unit_value"] = unit_value
            board_value += unit_value
            placement_value = self.calculate_placement_value(unit, friendly_units, enemy_units, game_board)
            board_value_breakdown[unit]["placement_value"] = placement_value
            board_value += placement_value

            targets = game_board.currTargets[unit]
            total_fight_value = 0
            for target in targets:
                total_fight_value += target[1]  # expected fight value is stored in the second element of the target list
            average_fight_value = total_fight_value / len(targets) if targets else 0
            board_value_breakdown[unit]["fight_value"] = average_fight_value
            board_value += average_fight_value
        for enemy_unit in enemy_units:
            board_value_breakdown[enemy_unit] = {}
            unit_value = -enemy_unit.value * (enemy_unit.health / enemy_unit.totalHealth)
            board_value_breakdown[enemy_unit]["unit_value"] = unit_value
            board_value += unit_value

        game_board.boardValueBreakdown = board_value_breakdown

        return board_value


    def update_board_value_breakdown(self, unit, other_unit, board_value):
        # Update the board value breakdown based on the new health of the units
        old_unit_value = self.boardValueBreakdown[unit]["unit_value"]
        unit_value = unit.value * (unit.health / unit.totalHealth)
        self.boardValueBreakdown[unit]["unit_value"] = unit_value
        board_value += unit_value - old_unit_value

        # Update the placement value for the unit
        old_placement_value = self.boardValueBreakdown[unit]["placement_value"]
        self.boardValueBreakdown[unit]["placement_value"] = self.calculate_placement_value(unit, self.units, game_board.enemies if self.team != "red" else game_board.player + game_board.ally + game_board.others, game_board)
        new_placement_value = self.boardValueBreakdown[unit]["placement_value"]
        board_value += new_placement_value - old_placement_value

        # Update the unit value for the other unit
        if other_unit in self.boardValueBreakdown:
            old_other_unit_value = self.boardValueBreakdown[other_unit]["unit_value"]
            other_unit_value = other_unit.value * (other_unit.health / other_unit.totalHealth)
            self.boardValueBreakdown[other_unit]["unit_value"] = other_unit_value
            board_value += other_unit_value - old_other_unit_value

        return board_value
