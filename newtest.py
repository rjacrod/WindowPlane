from flask import Flask, jsonify, send_file
from flask_cors import CORS
import requests
import json
import time

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configuration
HOME_LAT = 39.00950594490651
HOME_LON = -77.51869347001733

BBOX = {
    'lamin': 38.5,
    'lomin': -78.0,
    'lamax': 39.5,
    'lomax': -77.0
}

OPENSKY_CLIENT_ID = 'rjacr-api-client'
OPENSKY_CLIENT_SECRET = 'Ya0OeETWCxXcu1k053glAgaebhoBQSc5'

def get_planes():
    """Fetch plane data from OpenSky Network API"""
    planes = {}
    
    try:
        # Prepare API request
        api_url = "https://opensky-network.org/api/states/all"
        
        # Try Basic Authentication (username:password format)
        print("Making authenticated request with Basic Auth")
        auth = (OPENSKY_CLIENT_ID, OPENSKY_CLIENT_SECRET)
        
        # Make API request
        print(f"Fetching planes in bbox: {BBOX}")
        response = requests.get(api_url, params=BBOX, auth=auth, timeout=15)
        
        print(f"API Response: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('states'):
                print(f"Found {len(data['states'])} aircraft")
                for idx, state in enumerate(data['states']):
                    planes[idx] = {
                        'callsign': state[1].strip() if state[1] else 'Unknown',
                        'icao24': state[0],
                        'altitude': state[7],
                        'coords': [state[6], state[5]],
                        'velocity': state[9],
                        'heading': state[10]
                    }
            else:
                print("No aircraft in area")
                
        elif response.status_code == 401:
            print("✗ Authentication failed - check credentials")
        elif response.status_code == 429:
            print("✗ Rate limited by OpenSky")
        else:
            print(f"✗ API error: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            
    except requests.exceptions.Timeout:
        print("✗ Request timed out")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    return planes, BBOX

@app.route('/')
def index():
    """Serve the HTML file"""
    return send_file('templates/index.html')

@app.route('/api/planes')
def api_planes():
    """API endpoint for fetching plane data"""
    print("\n=== API Request Received ===")
    planes, bbox = get_planes()
    
    response_data = {
        'planes': planes,
        'bbox': bbox,
        'home': {'lat': HOME_LAT, 'lon': HOME_LON}
    }
    
    print(f"Returning {len(planes)} planes\n")
    return jsonify(response_data)

@app.route('/health')
def health():
    return jsonify({'status': 'ok', 'timestamp': time.time()})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')