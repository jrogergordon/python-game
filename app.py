from flask import Flask, render_template, jsonify, request
from functools import reduce  # Added for list intersection check
from board.test_match import test_board
from character.character import Character
from collections import deque
game_board = test_board
character_position = (0, 0)  # Global variable to track character position


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
    if not data or 'row' not in data or 'col' not in data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    row, col = int(data['row']), int(data['col'])
    character = game_board.board[row][col].occupant
    
    if not character or character.move <= 0:
        return jsonify({'reachable_cells': [], 'edge_cells': [], 'occupied_cells': []})

    # BFS to find all reachable cells
    queue = deque([(row, col, 0)])  # (row, col, distance)
    visited = set([(row, col)])
    reachable_cells = []  # This list will not include the starting position
    occupied_cells = []  # Initially empty, will include other characters, not the one moving
    edge_cells = set()  # For cells around reachable and occupied cells

    move_range = character.move

    while queue:
        r, c, dist = queue.popleft()
        if dist <= move_range:
            # Check if this cell is occupied by someone other than the moving character
            if game_board.board[r][c].occupant and (r, c) != (row, col):
                occupied_cells.append([r, c])
            elif (r, c) != (row, col):  # Avoid adding the character's current position to reachable cells
                reachable_cells.append([r, c])
            
            # Explore neighbors
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if (0 <= nr < len(game_board.board)) and (0 <= nc < len(game_board.board[0])) and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, dist + 1))

    # Determine edge cells now includes checking against occupied cells for accuracy
    for r, c in reachable_cells:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if (0 <= nr < len(game_board.board)) and (0 <= nc < len(game_board.board[0])):
                if [nr, nc] not in reachable_cells and [nr, nc] not in occupied_cells:
                    edge_cells.add((nr, nc))

    return jsonify({
        'reachable_cells': reachable_cells,
        'edge_cells': list(edge_cells),
        'occupied_cells': occupied_cells  # This now correctly does not include the moving character's cell
    })
    
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
            'defense': occupant.defense,
            'x': occupant.x,
            'y': occupant.y
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


@app.route('/collect_options', methods=['POST'])
def collect_options():  
    data = request.get_json()  
    if not data or 'row' not in data or 'col' not in data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    row = data.get('row')
    col = data.get('col')
    used = data.get('used')

    if row is None or col is None:
        return jsonify({'error': 'Row and col values are required'}), 400  # Adjust the error message as needed

    try:
        row = int(row)
        col = int(col)  
        character = game_board.board[row][col].occupant
    except (IndexError, KeyError, ValueError):
        return jsonify({'error': 'Character not found or invalid row/col'}), 404
    
    if used:
        return jsonify({'error': 'Character already used'})  
    
    options = ['move', 'wait']
    if character.equipped or character.inventory:
        options.append('items')  
    
    return jsonify({'options': options})   
    
@app.route('/get_highlighted_cell')
def get_highlighted_cell():
    global game_board
    return jsonify({'highlighted_cell': game_board.highlighted_cell})   

@app.route('/get_combat_preview', methods=['POST'])
def get_combat_preview():
    data = request.get_json()
    x1, y1 = data['character1']
    x2, y2 = data['character2']
    
    char1 = game_board.board[x1][y1].occupant if game_board.board[x1][y1].occupant else None
    char2 = game_board.board[x2][y2].occupant if game_board.board[x2][y2].occupant else None

    if not isinstance(char1, Character) or not isinstance(char2, Character):
        return jsonify({'error': 'One or both coordinates do not contain a character'}), 400

    # Calculate combat statistics
    damage1 = game_board.predict_fight(char1, char2)
    damage2 = game_board.predict_fight(char2, char1)
    hit_likelihood1, hit_likelihood2 = game_board.calculate_hit_likelihood(char1, char2)
    attacks_twice1 = char1.speed >= char2.speed + 4
    attacks_twice2 = char2.speed >= char1.speed + 4
    
    health_after_combat1 = max(0, char1.health - damage2 * hit_likelihood2 * (2 if attacks_twice2 else 1))
    health_after_combat2 = max(0, char2.health - damage1 * hit_likelihood1 * (2 if attacks_twice1 else 1))

    combat_data = {
        'character1': {
            'name': char1.name,
            'damage': damage1,
            'hit_likelihood': hit_likelihood1,
            'predicted_health': health_after_combat1,
            'attacks_twice': attacks_twice1
        },
        'character2': {
            'name': char2.name,
            'damage': damage2,
            'hit_likelihood': hit_likelihood2,
            'predicted_health': health_after_combat2,
            'attacks_twice': attacks_twice2
        }
    }

    return jsonify(combat_data)


if __name__ == '__main__':
    app.run()