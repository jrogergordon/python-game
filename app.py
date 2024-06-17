from flask import Flask, render_template, jsonify, request
from board.test_match import test_board
from character.character import Character
game_board = test_board

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', board_size=len(game_board.board), game_board=game_board)

@app.route('/update_highlighted_cell', methods=['POST'])
def update_highlighted_cell():
    global game_board
    data = request.get_json()
    if 'direction' in data:
        direction = data['direction']
        if direction == 'up' and game_board.highlighted_cell[0] > 0:
            game_board.move_up()
        elif direction == 'down' and game_board.highlighted_cell[0] < len(game_board.board) - 1:
            game_board.move_down()
        elif direction == 'left' and game_board.highlighted_cell[1] > 0:
            game_board.move_left()
        elif direction == 'right' and game_board.highlighted_cell[1] < len(game_board.board[0]) - 1:
            game_board.move_right()
    elif 'highlighted_cell' in data:
        game_board.update_highlighted_cell(data['highlighted_cell'][0], data['highlighted_cell'][1])
    return jsonify({'highlighted_cell': game_board.highlighted_cell})

@app.route('/get_reachable_cells', methods=['POST'])
def get_reachable_cells():
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Invalid request'}), 400
    row = data.get('row')
    col = data.get('col')
    if row is None or col is None:
        return jsonify({'error': 'Missing row or col data'}), 400
    try:
        row = int(row)
        col = int(col)
    except ValueError:
        return jsonify({'error': 'Invalid row or col data'}), 400
    character = game_board.board[row][col].occupant
    if character and character.move > 0:
        reachable_cells = []
        edge_cells = []
        for i in range(-character.move, character.move + 1):
            for j in range(-character.move, character.move + 1):
                if abs(i) + abs(j) <= character.move:
                    new_row = row + i
                    new_col = col + j
                    if new_row >= 0 and new_row < len(game_board.board) and new_col >= 0 and new_col < len(game_board.board[0]):
                        reachable_cells.append([new_row, new_col])
                    else:
                        edge_cells.append([new_row, new_col])
        for cell in reachable_cells:
            for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_row = cell[0] + i
                new_col = cell[1] + j
                if [new_row, new_col] not in reachable_cells and [new_row, new_col] not in edge_cells:
                    edge_cells.append([new_row, new_col])
        return jsonify({'reachable_cells': reachable_cells, 'edge_cells': edge_cells})
    else:
        return jsonify({'reachable_cells': [], 'edge_cells': []})
    
@app.route('/get_occupant', methods=['POST'])
def get_occupant():
    data = request.get_json()
    row = data.get('row')
    col = data.get('col')
    occupant = game_board.board[row][col].occupant
    if isinstance(occupant, Character):
        return jsonify({
            'type': 'character',
            'name': occupant.name,
            'health': occupant.health,
            'strength': occupant.strength,
            'speed': occupant.speed,
            'skill': occupant.skill,
            'defense': occupant.defense
        })
    else:
        return jsonify({'type': 'node', 'show': game_board.board[row][col].show})
    
@app.route('/get_board')
def get_board():
    board_data = []
    for row in game_board.board:
        row_data = []
        for node in row:
            node_data = {
                'occupant': node.occupant.show if node.occupant else None,
                'show': node.show
            }
            row_data.append(node_data)
        board_data.append(row_data)
    return jsonify({'board': board_data})
    
    

    

if __name__ == '__main__':
    app.run()