from flask import Flask, send_from_directory

app = Flask(__name__, static_url_path='', static_folder='public')

@app.route('/')
def serve_index():
    return send_from_directory('public', 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
