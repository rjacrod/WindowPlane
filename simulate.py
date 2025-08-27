import requests, json, time
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
import numpy as np

WIDTH = 32
HEIGHT = 8
SCALE = 8

plt.ion()
fig, ax = plt.subplots()
im = None

def simulate_matrix(text, color=(255, 255, 255)):
    global im

    font = ImageFont.load_default()
    image = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font, fill=color)

    # Scale up for display
    large_image = image.resize((WIDTH * SCALE, HEIGHT * SCALE), Image.NEAREST)
    img_array = np.array(large_image)

    if im is None:
        im = ax.imshow(img_array)
        ax.axis('off')  # Hide axes
    else:
        im.set_data(img_array)
    
    fig.canvas.draw()
    fig.canvas.flush_events()

def get_planes():
    planes = {}
    try:
        with open("bbox.json") as f:
            bbox = json.load(f)

        response = requests.get("https://opensky-network.org/api/states/all", params=bbox, timeout=5)
        data = response.json()

        if not data['states']:
            print("No planes...")
            return {}
        
        uuid = 0
        for a in data['states']:
            callsign = a[1].strip() if a[1] else 'Unknown'
            icao24 = a[0]
            altitude = a[7]
            coords = (a[6], a[5])
            velocity = a[9]
            heading = a[10]

            planes[uuid] = {
                "callsign": callsign,
                "icao24": icao24,
                "altitude": altitude,
                "coords": coords,
                "velocity": velocity,
                "heading": heading
            }
            uuid += 1
        return planes

    except Exception as e:
        print("Error fetching planes:", e)
        return {}

# sim interface
while True:
    planes = get_planes()
    print(planes)
    callsigns = [p['callsign'] for p in planes.values() if p['callsign'] != 'Unknown']

    if not callsigns:
        simulate_matrix("No planes")
        time.sleep(5)
        continue

    print(f"Displaying {len(callsigns)} callsigns")

    start_time = time.time()
    i = 0
    while time.time() - start_time < 60:
        simulate_matrix(callsigns[i % len(callsigns)])
        time.sleep(1)  # small delay so display is readable
        i += 1
