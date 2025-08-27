import requests, json

# setup planes dict
planes = {}

# query flights
with open("bbox.json") as f:
    bbox = json.load(f)
response = requests.get("https://opensky-network.org/api/states/all", params=bbox)
data = response.json()

if data['states'] == None:
    # no flights
    print("No planes...")
else:
    # format flights
    print(f"\nPlanes closeby: {len(data.get('states', []))}\n")

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

    print(planes)        
