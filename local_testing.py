from flask import Flask, jsonify, render_template
import requests, json
app = Flask(__name__)

(h_lat, h_lon) = (39.00950594490651, -77.51869347001733)

def get_planes():
    # setup planes dict
    planes = {}

    # query flights
    with open("bbox.json") as f:
        bbox = json.load(f)
    response = requests.get("https://opensky-network.org/api/states/all", params=bbox)
    data = response.json()

    if data['states'] == None:
        # no flights
        return planes, bbox
    else:
        # format flights
        uuid = 0
        for a in data.get("states", []):
            callsign = a[1].strip() if a[1] else 'Unknown'
            icao24 = a[0]
            altitude = a[7] # m
            coords = (a[6], a[5])
            velocity = a[9] # m/s
            heading = a[10] # deg

            planes[uuid] = {
                "callsign": callsign,
                "icao24": icao24,
                "altitude": altitude,
                "coords": coords,
                "velocity": velocity,
                "heading": heading
            }
            uuid += 1

        return planes, bbox

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/planes')
def api_planes():
    planes, bbox = get_planes()
    return jsonify({
        'planes': planes,
        'bbox': bbox,
        'home': {'lat': h_lat, 'lon': h_lon}
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)