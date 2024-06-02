def calculate_board_value(self, team):
    if team == "green":
        friendly_units = self.others
    elif team == "yellow":
        friendly_units = self.ally
    else:
        friendly_units = self.enemies

    board_value = 0
    board_value_breakdown = {}

    for friendly_unit in friendly_units:
        board_value_breakdown[friendly_unit] = {}
        unit_value = friendly_unit.value * (friendly_unit.health / friendly_unit.totalHealth)
        board_value_breakdown[friendly_unit]["unit_value"] = unit_value
        board_value += unit_value

        placement_value = self.calculate_placement_value(friendly_unit, board_value_breakdown)
        board_value += placement_value

        targets = self.currTargets[friendly_unit]
        total_fight_value = 0
        for target in targets:
            enemy_unit = target[0]
            expected_fight_value = self.calculate_expected_fight_value(friendly_unit, enemy_unit)
            total_fight_value += expected_fight_value
        average_fight_value = total_fight_value / len(targets) if targets else 0
        board_value_breakdown[friendly_unit]["fight_value"] = average_fight_value
        board_value += average_fight_value

    for enemy_unit in self.enemies if team != "red" else self.others + self.ally:
        board_value_breakdown[enemy_unit] = {}
        unit_value = -enemy_unit.value * (enemy_unit.health / enemy_unit.totalHealth)
        board_value_breakdown[enemy_unit]["unit_value"] = unit_value
        board_value += unit_value

        placement_value = self.calculate_placement_value(enemy_unit, board_value_breakdown)
        board_value += placement_value

    if team == "green":
        self.boardValueOther = board_value_breakdown
    elif team == "yellow":
        self.boardValueAlly = board_value_breakdown
    else:
        self.boardValueEnemies = board_value_breakdown

    return board_value

def calculate_placement_value(self, unit, board_value_breakdown):
    placement_value = 0
    friendly_units = self.others + self.ally if unit.team != "red" else self.enemies
    enemy_units = self.enemies if unit.team != "red" else self.others + self.ally

    for enemy_unit in enemy_units:
        if self.can_reach(enemy_unit, unit):
            if enemy_unit.value > unit.value:
                placement_value -= 10 
                board_value_breakdown[unit][f"placement_value_strong_enemy_{enemy_unit.name}"] = -10
            else:
                placement_value += 5
                board_value_breakdown[unit][f"placement_value_weak_enemy_{enemy_unit.name}"] = 5

    for friendly_unit in friendly_units:
        if friendly_unit != unit and self.can_reach(friendly_unit, unit):
            if friendly_unit.value > unit.value:
                placement_value += 5
                board_value_breakdown[unit][f"placement_value_strong_friend_{friendly_unit.name}"] = 5
            else:
                placement_value += 2
                board_value_breakdown[unit][f"placement_value_weak_friend_{friendly_unit.name}"] = 2

    return placement_value

def can_reach(self, unit1, unit2):
    return abs(unit1.x - unit2.x) + abs(unit1.y - unit2.y) <= unit1.move + 1