from flask import Flask, jsonify
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/time', methods=['GET'])
def get_time():
    now = datetime.utcnow().isoformat() + 'Z'
    return jsonify({"current_time": now})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use PORT from environment or fallback
    app.run(host='0.0.0.0', port=port)
