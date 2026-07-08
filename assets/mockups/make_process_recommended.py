from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path("assets/mockups/process-block-recommended.png")
W, H = 1600, 920
S = 2

NAVY = "#0b315f"
NAVY_2 = "#173f73"
GOLD = "#dc9332"
GOLD_LIGHT = "#f4c985"
INK = "#2d4665"
MUTED = "#647891"
LINE = "#dce6f0"
PAPER = "#ffffff"
CREAM = "#faf6ef"
MIST = "#eef4f8"

FONT_SERIF = "C:/Windows/Fonts/georgia.ttf"
FONT_SERIF_BOLD = "C:/Windows/Fonts/georgiab.ttf"
FONT_SANS = "C:/Windows/Fonts/arial.ttf"
FONT_SANS_BOLD = "C:/Windows/Fonts/arialbd.ttf"


def font(path, size):
    return ImageFont.truetype(path, size * S)


img = Image.new("RGB", (W * S, H * S), PAPER)
d = ImageDraw.Draw(img)


def xy(values):
    return tuple(int(v * S) for v in values)


def rect(box, fill, outline=None, width=1, radius=0):
    if radius:
        d.rounded_rectangle(
            xy(box),
            radius=radius * S,
            fill=fill,
            outline=outline,
            width=width * S if outline else 1,
        )
    else:
        d.rectangle(xy(box), fill=fill, outline=outline, width=width * S if outline else 1)


def line(points, fill, width=1):
    d.line([xy(p) for p in points], fill=fill, width=width * S, joint="curve")


def circle(cx, cy, r, fill, outline=None, width=1):
    d.ellipse(xy((cx - r, cy - r, cx + r, cy + r)), fill=fill, outline=outline, width=width * S if outline else 1)


def text(pos, value, text_font, fill=INK, anchor=None, align="left"):
    d.text(xy(pos), value, font=text_font, fill=fill, anchor=anchor, align=align)


def center_text(cx, cy, value, text_font, fill=INK):
    text((cx, cy), value, text_font, fill, anchor="mm")


def wrap(value, text_font, max_width):
    words = value.split()
    lines = []
    current = ""
    for word in words:
        candidate = (current + " " + word).strip()
        if d.textbbox((0, 0), candidate, font=text_font)[2] <= max_width * S or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paragraph(x, y, value, text_font, fill, max_width, line_height):
    yy = y
    for row in wrap(value, text_font, max_width):
        text((x, yy), row, text_font, fill)
        yy += line_height
    return yy


def icon(cx, cy, kind, color=GOLD):
    if kind == "target":
        circle(cx, cy, 18, None, color, 4)
        circle(cx, cy, 7, color)
    elif kind == "plan":
        rect((cx - 15, cy - 20, cx + 15, cy + 20), None, color, 4, 4)
        line([(cx - 7, cy - 8), (cx + 8, cy - 8)], color, 3)
        line([(cx - 7, cy + 2), (cx + 8, cy + 2)], color, 3)
        line([(cx - 7, cy + 12), (cx + 5, cy + 12)], color, 3)
    elif kind == "work":
        points = [(cx, cy - 22), (cx + 19, cy - 10), (cx + 13, cy + 16), (cx, cy + 24), (cx - 13, cy + 16), (cx - 19, cy - 10), (cx, cy - 22)]
        d.line([xy(p) for p in points], fill=color, width=4 * S, joint="curve")
        line([(cx - 7, cy + 1), (cx - 1, cy + 8), (cx + 10, cy - 8)], color, 4)
    elif kind == "check":
        line([(cx - 16, cy), (cx - 5, cy + 13), (cx + 18, cy - 18)], color, 5)


def pill(x, y, w, h, label, fill=GOLD_LIGHT, color=NAVY):
    rect((x, y, x + w, y + h), fill, radius=h // 2)
    center_text(x + w / 2, y + h / 2 - 1, label, font(FONT_SANS_BOLD, 18), color)


# subtle section background
rect((0, 0, W, H), PAPER)
rect((48, 48, W - 48, H - 54), "#fbfcfd", "#edf2f7", 1, 26)
rect((82, 250, W - 82, H - 112), CREAM, "#efe2cf", 1, 24)

# heading
center_text(W / 2, 96, "ЯК МИ ПРАЦЮЄМО", font(FONT_SANS_BOLD, 18), NAVY)
center_text(W / 2, 160, "Від першої консультації до результату", font(FONT_SERIF_BOLD, 54), NAVY)
center_text(W / 2, 218, "Прозорий процес без зайвого стресу: ви розумієте кожен крок і бачите, що відбувається далі.", font(FONT_SANS, 22), MUTED)

# left promise block
text((132, 318), "Починаємо\nз вашої ситуації", font(FONT_SERIF_BOLD, 38), NAVY)
paragraph(
    132,
    428,
    "Спочатку розбираємо задачу, потім пропонуємо план дій і беремо супровід на себе. Без хаосу, без прихованих умов.",
    font(FONT_SANS, 22),
    INK,
    415,
    34,
)
pill(132, 568, 250, 56, "Отримати план дій")

chips = [("01", "перша консультація"), ("10+", "років досвіду"), ("UA/CZ", "зручна комунікація")]
for i, (big, small) in enumerate(chips):
    x = 132 + i * 146
    y = 666
    rect((x, y, x + 124, y + 104), PAPER, "#e3ebf3", 1, 14)
    center_text(x + 62, y + 34, big, font(FONT_SERIF_BOLD, 26), GOLD)
    center_text(x + 62, y + 72, small, font(FONT_SANS_BOLD, 13), NAVY)

# roadmap card
road_x = 680
road_y = 316
road_w = 760
road_h = 420
rect((road_x, road_y, road_x + road_w, road_y + road_h), PAPER, "#e1e9f2", 1, 20)

steps = [
    ("01", "Консультація", "Вивчаємо ситуацію та фіксуємо завдання.", "target"),
    ("02", "План дій", "Пояснюємо оптимальний шлях і строки.", "plan"),
    ("03", "Реалізація", "Готуємо документи та супроводжуємо процес.", "work"),
    ("04", "Результат", "Передаємо готове рішення або послугу.", "check"),
]

row_y = [384, 474, 564, 654]
for idx, ((num, title, desc, kind), cy) in enumerate(zip(steps, row_y)):
    if idx < 3:
        line([(road_x + 72, cy + 38), (road_x + 72, row_y[idx + 1] - 38)], LINE, 4)
    circle(road_x + 72, cy, 36, "#fffaf2", "#f1c681", 2)
    icon(road_x + 72, cy, kind)
    text((road_x + 132, cy - 30), num, font(FONT_SERIF_BOLD, 24), GOLD)
    text((road_x + 184, cy - 31), title, font(FONT_SANS_BOLD, 25), NAVY)
    text((road_x + 184, cy + 7), desc, font(FONT_SANS, 19), INK)

# decorative route curve
curve = [(92, 790), (310, 840), (585, 810), (835, 814), (1110, 856), (1508, 796)]
for offset, color, width in [(0, "#e8eef5", 6), (-10, "#f4c985", 2)]:
    shifted = [(x, y + offset) for x, y in curve]
    for a, b in zip(shifted, shifted[1:]):
        line([a, b], color, width)

img = img.resize((W, H), Image.Resampling.LANCZOS)
OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, quality=95)
print(OUT, img.size)
