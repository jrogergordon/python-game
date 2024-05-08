from flask import Flask, jsonify
from flask import render_template

app = Flask(__name__, template_folder='templates')

# Initialize the game state
game_state = {
    "highlighted_cell": 0,
    "cell_colors": ["red", "blue"]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game-state', methods=['GET'])
def get_game_state():
    return jsonify(game_state)

@app.route('/change-highlighted-cell', methods=['POST'])
def change_highlighted_cell():
    global game_state
    game_state["highlighted_cell"] = (game_state["highlighted_cell"] + 1) % 2
    game_state["cell_colors"] = ["blue" if i == game_state["highlighted_cell"] else "red" for i in range(2)]
    return jsonify(game_state)

if __name__ == '__main__':
    app.run(debug=True)
