import os
import random


def generate_svg_stars(path="app/static/stars/stars.svg", count=250, width=1920,
                       height=2000):
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">\n')
            for _ in range(count):
                x = random.randint(0, width)
                y = random.randint(0, height)
                f.write(f'<circle cx="{x}" cy="{y}" r="1" fill="white" />\n')
            f.write('</svg>\n')

