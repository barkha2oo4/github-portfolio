import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from action_logic import handle_query
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json(force=True)
    user_input = data.get("input", "")
    response = handle_query(user_input)
    return jsonify({"response": response})

@app.route('/backend/image/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(app.root_path, 'image'), filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
