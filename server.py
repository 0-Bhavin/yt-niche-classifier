from flask import Flask, request, jsonify
import json
from pathlib import Path
from datetime import datetime

app = Flask(__name__)

# Path to save video data
DATA_DIR = Path(__file__).parent / "data"
DATA_FILE = DATA_DIR / "extension_videos.json"

@app.route('/save-videos', methods=['POST'])
def save_videos():
    try:
        data = request.json
        videos = data.get('videos', [])
        
        # Create data with timestamp
        output = {
            'videos': videos,
            'count': len(videos),
            'timestamp': datetime.now().isoformat()
        }
        
        # Save to JSON file
        with open(DATA_FILE, 'w') as f:
            json.dump(output, f, indent=2)
        
        return jsonify({
            'status': 'success',
            'message': f'Saved {len(videos)} videos',
            'path': str(DATA_FILE)
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'Server is running'}), 200

if __name__ == '__main__':
    print(f"Starting server... Data will be saved to: {DATA_FILE}")
    app.run(host='localhost', port=5000, debug=True)
