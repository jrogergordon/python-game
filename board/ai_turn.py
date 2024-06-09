class AI:
    def __init__(self, team):
        self.team = team

    def calculate_placement_value(self, unit, friendly_units, enemy_units, game_board):
        placement_value = 0
        for enemy_unit in enemy_units:
            if game_board.can_reach(enemy_unit, unit):
                if enemy_unit.value > unit.value:   
                    placement_value -= 10
                else:
                    placement_value += 5

        for friendly_unit in friendly_units:
            if friendly_unit != unit and game_board.can_reach(friendly_unit, unit):
                if friendly_unit.value > unit.value:
                    placement_value += 5
                else:
                    placement_value += 2
        return placement_value

    def can_reach(self, unit1, unit2):
        return abs(unit1.x - unit2.x) + abs(unit1.y - unit2.y) <= unit1.move + 1

    def best_move(self, game_board):
        best_move = None
        best_move_value = float('-inf')
        if self.team == "green":
            units = game_board.others
        elif self.team == "yellow":
            units = game_board.ally
        else:
            units = game_board.enemies
        for unit in units:
            targets = game_board.currTargets[unit]
            for target in targets:
                enemy_unit = target[0]
                fight_value = target[1]
                reachable_nodes = target[2]
                for node in reachable_nodes:
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
                    placement_value = self.calculate_placement_value(unit, units, game_board.enemies if self.team != "red" else game_board.player + game_board.ally + game_board.others, game_board)
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
    
        game_board.currTargets = scanned_nodes

    def update_board_value_breakdown(self, unit, other_unit, board_value):
        # Update the board value breakdown based on the new health of the units
        old_unit_value = self.boardValueBreakdown[unit]["unit_value"]
        unit_value = unit.value * (unit.health / unit.totalHealth)
        self.boardValueBreakdown[unit]["unit_value"] = unit_value
        board_value += unit_value - old_unit_value

        # Update the placement value for the unit
        old_placement_value = self.boardValueBreakdown[unit]["placement_value"]
        self.boardValueBreakdown[unit]["placement_value"] = self.calculate_placement_value(unit, self.units, self.game_board.enemies if self.team != "red" else self.game_board.player + self.game_board.ally + self.game_board.others, self.game_board)
        new_placement_value = self.boardValueBreakdown[unit]["placement_value"]
        board_value += new_placement_value - old_placement_value

        # Update the unit value for the other unit
        if other_unit in self.boardValueBreakdown:
            old_other_unit_value = self.boardValueBreakdown[other_unit]["unit_value"]
            other_unit_value = other_unit.value * (other_unit.health / other_unit.totalHealth)
            self.boardValueBreakdown[other_unit]["unit_value"] = other_unit_value
            board_value += other_unit_value - old_other_unit_value

        return board_value

