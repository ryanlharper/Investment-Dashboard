from flask import Flask, send_from_directory
import os
from src import create_app

app = create_app()

@app.route('/')
def index():
    return send_from_directory(os.path.join(app.root_path, 'public'), 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(os.path.join(app.root_path, 'public'), path)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

