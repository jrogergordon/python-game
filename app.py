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
        occupied_cells = []
        for i in range(len(game_board.board)):
            for j in range(len(game_board.board[0])):
                node = game_board.board[i][j]
                if node != game_board.board[row][col]:
                    result = game_board.a_star(game_board.board[row][col], node)
                    if result == -1:
                        occupied_cells.append([i, j])
                    elif result:
                        reachable_cells.append([i, j])
        for cell in reachable_cells:
            for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_row = cell[0] + i
                new_col = cell[1] + j
                if [new_row, new_col] not in reachable_cells and [new_row, new_col] not in edge_cells:
                    edge_cells.append([new_row, new_col])
        return jsonify({'reachable_cells': reachable_cells, 'edge_cells': edge_cells, 'occupied_cells': occupied_cells})
    else:
        return jsonify({'reachable_cells': [], 'edge_cells': [], 'occupied_cells': []})
    
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

@app.route('/move_character', methods=['POST'])
def move_character():
    data = request.get_json()
    character_name = data.get('character')
    new_x = data.get('new_x')
    new_y = data.get('new_y')

    # Find the character and move it to the new location
    for row in game_board.board:
        for node in row:
            if node.occupant and node.occupant.name == character_name:
                character = node.occupant
                node.occupant = 0
                game_board.board[new_x][new_y].occupant = character
                return jsonify({'success': True})

    return jsonify({'success': False})

@app.route('/get_characters')
def get_characters():
    characters = []
    for row in game_board.board:
        for node in row:
            if node.occupant:
                characters.append({'name': node.occupant.name})
    return jsonify({'characters': characters})

    
    

    

if __name__ == '__main__':
    app.run()