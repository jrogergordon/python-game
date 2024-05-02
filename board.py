import heapq
from map_node import board_node

class GameBoard:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                node = board_node(0, 0, None, j, i)  # x is j, y is i
                row.append(node)
            board.append(row)
        return board

    def display_board(self):
        print('  1 2 3 4 5 6 7 8 9')
        for i, row in enumerate(self.board, start=1):
            print(f'{i} ' + ' '.join(row))

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
        damage = character1.strength - character2.defense
        if damage > 0:
            if damage > character2.health:
                character2.health = 0
            else:    
                character2.change_health(-damage)

    def a_star(self, start, goal):
        open_list = [start]
        came_from = {}
        g_score = {node: float('inf') for row in self.board for node in row}
        g_score[start] = 0
        f_score = {node: float('inf') for row in self.board for node in row}
        f_score[start] = self.heuristic(start, goal)

        while open_list:
            current = min(open_list, key=lambda node: f_score[node])
            if current == goal:
                return self.reconstruct_path(came_from, current)

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

# Create and display the game board
# game_board = GameBoard()
# game_board.display_board()