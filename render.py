font_4x3 = {
    "A": [
        "111",
        "101",
        "111",
        "101",
    ],
    "B": [
        "110",
        "101",
        "110",
        "111",
    ],
    "C": [
        "111",
        "100",
        "100",
        "111",
    ],
    "D": [
        "110",
        "101",
        "101",
        "110",
    ],
    "E": [
        "111",
        "110",
        "100",
        "111",
    ],
    "F": [
        "111",
        "110",
        "100",
        "100",
    ],
    "G": [
        "111",
        "100",
        "101",
        "111",
    ],
    "H": [
        "101",
        "111",
        "101",
        "101",
    ],
    "I": [
        "111",
        "010",
        "010",
        "111",
    ],
    "J": [
        "001",
        "001",
        "101",
        "111",
    ],
    "K": [
        "101",
        "110",
        "110",
        "101",
    ],
    "L": [
        "100",
        "100",
        "100",
        "111",
    ],
    "M": [
        "1001",
        "1111",
        "1101",
        "1001",
    ],
    "N": [
        "1001",
        "1101",
        "1011",
        "1001",
    ],
    "O": [
        "111",
        "101",
        "101",
        "111",
    ],
    "P": [
        "111",
        "101",
        "111",
        "100",
    ],
    "Q": [
        "111",
        "101",
        "110",
        "001",
    ],
    "R": [
        "111",
        "101",
        "110",
        "101",
    ],
    "S": [
        "011",
        "100",
        "011",
        "110",
    ],
    "T": [
        "111",
        "010",
        "010",
        "010",
    ],
    "U": [
        "101",
        "101",
        "101",
        "111",
    ],
    "V": [
        "101",
        "101",
        "101",
        "010",
    ],
    "W": [
        "1001",
        "1101",
        "1111",
        "1001",
    ],
    "X": [
        "101",
        "010",
        "010",
        "101",
    ],
    "Y": [
        "101",
        "101",
        "111",
        "010",
    ],
    "Z": [
        "111",
        "001",
        "010",
        "111",
    ],
    "0": [
        "0110",
        "1101",
        "1011",
        "0110",
    ],
    "1": [
        "010",
        "110",
        "010",
        "111",
    ],
    "2": [
        "110",
        "001",
        "010",
        "111",
    ],
    "3": [
        "111",
        "001",
        "011",
        "110",
    ],
    "4": [
        "101",
        "111",
        "001",
        "001",
    ],
    "5": [
        "111",
        "100",
        "111",
        "001",
    ],
    "6": [
        "011",
        "100",
        "111",
        "111",
    ],
    "7": [
        "111",
        "001",
        "010",
        "100",
    ],
    "8": [
        "0111",
        "0101",
        "1010",
        "1110",
    ],
    "9": [
        "111",
        "101",
        "111",
        "001",
    ]
}

from PIL import Image

PIXEL_SCALE = 15

def render_char(char):
    pixels = font_4x3.get(char.upper(), ["000"]*4)
    height = len(pixels)
    width = len(pixels[0])
    img = Image.new("RGB", (width, height), (0, 0, 0))
    for y, row in enumerate(pixels):
        for x, c in enumerate(row):
            if c == "1":
                img.putpixel((x, y), (255, 255, 255))
    return img.resize((width * PIXEL_SCALE, height * PIXEL_SCALE), Image.NEAREST)

def render_text(text):
    chars = [render_char(c) for c in text if c.upper() in font_4x3]
    if not chars:
        return None
    height = chars[0].height
    spacing = PIXEL_SCALE
    width = sum(img.width for img in chars) + spacing * (len(chars) - 1)

    result = Image.new("RGB", (width, height), (0, 0, 0))
    x_offset = 0
    for i, img in enumerate(chars):
        result.paste(img, (x_offset, 0))
        x_offset += img.width
        if i < len(chars) - 1:
            x_offset += spacing
    return result

# Example usage:
img = render_text("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
img.show()

img = render_text("WUHF53  OISHY90  ZCCXY08")
img.show()
