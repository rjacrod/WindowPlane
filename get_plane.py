import requests, json, time
import board
import neopixel
from PIL import Image, ImageDraw, ImageFont

# === LED MATRIX CONFIG ===
WIDTH = 32
HEIGHT = 8
NUM_PIXELS = WIDTH * HEIGHT
BRIGHTNESS = 0.2

pixels = neopixel.NeoPixel(
    board.D18, NUM_PIXELS, brightness=BRIGHTNESS, auto_write=False, pixel_order=neopixel.GRB
)

def xy_to_index(x, y):
    if y % 2 == 0:
        return y * WIDTH + x
    else:
        return y * WIDTH + (WIDTH - 1 - x)

def display_text(text, color=(255, 255, 255)):
    font = ImageFont.load_default()
    image = Image.new("RGB", (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, font=font, fill=color)

    for y in range(HEIGHT):
        for x in range(WIDTH):
            r, g, b = image.getpixel((x, y))
            pixels[xy_to_index(x, y)] = (r, g, b)
    pixels.show()

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

while True:
    planes = get_planes()
    callsigns = [p['callsign'] for p in planes.values() if p['callsign'] != 'Unknown']

    if not callsigns:
        display_text("No planes")
        time.sleep(5)
        continue

    print(f"Displaying {len(callsigns)} callsigns")
    
    start_time = time.time()
    i = 0
    while time.time() - start_time < 60:
        display_text(callsigns[i % len(callsigns)])
        time.sleep(5)
        i += 1