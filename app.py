from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    return "hello world"

@app.route('/assets/')
def send_assets(path):
    return send_from_directory('assets', path)

if __name__ == '__main__':
    app.run(debug=True)