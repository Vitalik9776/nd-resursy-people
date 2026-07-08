from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path("assets/mockups/process-block-variants.png")
W, H = 1800, 1900
S = 2

NAVY = "#0b315f"
GOLD = "#dc9332"
GOLD_LIGHT = "#f3c987"
INK = "#243d5d"
MUTED = "#637791"
MIST = "#edf2f7"
LINE = "#d9e3ee"
PAPER = "#ffffff"
CREAM = "#faf7f1"
GREENISH = "#eef5f1"

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
    for line_text in wrap(value, text_font, max_width):
        text((x, yy), line_text, text_font, fill)
        yy += line_height
    return yy


def pill(x, y, w, h, label, fill=GOLD_LIGHT, color=NAVY):
    rect((x, y, x + w, y + h), fill, radius=h // 2)
    center_text(x + w / 2, y + h / 2 - 1, label, font(FONT_SANS_BOLD, 18), color)


def icon(cx, cy, kind, color=GOLD):
    if kind == "target":
        circle(cx, cy, 18, None, color, 4)
        circle(cx, cy, 7, color)
    elif kind == "doc":
        rect((cx - 15, cy - 19, cx + 15, cy + 19), None, color, 4, 4)
        line([(cx - 8, cy - 7), (cx + 8, cy - 7)], color, 3)
        line([(cx - 8, cy + 3), (cx + 8, cy + 3)], color, 3)
    elif kind == "shield":
        points = [(cx, cy - 20), (cx + 17, cy - 10), (cx + 12, cy + 15), (cx, cy + 24), (cx - 12, cy + 15), (cx - 17, cy - 10), (cx, cy - 20)]
        d.line([xy(p) for p in points], fill=color, width=4 * S, joint="curve")
        line([(cx - 7, cy + 1), (cx - 1, cy + 7), (cx + 9, cy - 7)], color, 4)
    elif kind == "check":
        line([(cx - 15, cy), (cx - 4, cy + 12), (cx + 17, cy - 16)], color, 5)


steps = [
    ("01", "Консультація", "Вивчаємо вашу ситуацію та визначаємо завдання.", "target"),
    ("02", "План дій", "Пропонуємо оптимальне рішення та чіткий план кроків.", "doc"),
    ("03", "Реалізація", "Беремо на себе супровід та впровадження рішення.", "shield"),
    ("04", "Результат", "Ви отримуєте необхідний документ, послугу або результат.", "check"),
]

text((70, 54), "3 варианта блока «Як ми працюємо»", font(FONT_SERIF_BOLD, 48), NAVY)
text((72, 112), "Все в стиле ND-Resursy: синий, золото, много воздуха, без перегруза.", font(FONT_SANS, 24), MUTED)

# Variant 1
x0, y0, ww, hh = 70, 180, 1660, 470
rect((x0, y0, x0 + ww, y0 + hh), "#fbfcfd", "#e4ecf4", 1, 18)
text((x0 + 36, y0 + 34), "Вариант 1", font(FONT_SANS_BOLD, 20), GOLD)
center_text(x0 + ww / 2, y0 + 58, "Простий шлях до рішення", font(FONT_SERIF_BOLD, 48), NAVY)
text((x0 + ww / 2, y0 + 102), "Классический timeline, но плотнее, чище и дороже", font(FONT_SANS, 22), MUTED, anchor="ma")
line_y = y0 + 220
xs = [x0 + 170, x0 + 590, x0 + 1010, x0 + 1430]
for i in range(3):
    start, end = xs[i] + 64, xs[i + 1] - 64
    xx = start
    while xx < end:
        line([(xx, line_y), (min(xx + 22, end), line_y)], "#b8c7d8", 3)
        xx += 38
for (num, title, desc, kind), cx in zip(steps, xs):
    text((cx - 92, line_y - 10), num, font(FONT_SERIF_BOLD, 26), NAVY)
    circle(cx, line_y, 48, PAPER, "#dce6f0", 2)
    icon(cx, line_y, kind)
    text((cx - 92, line_y + 78), title, font(FONT_SANS_BOLD, 25), NAVY)
    paragraph(cx - 92, line_y + 120, desc, font(FONT_SANS, 19), INK, 250, 28)

# Variant 2
x0, y0, ww, hh = 70, 710, 1660, 500
rect((x0, y0, x0 + ww, y0 + hh), CREAM, "#eadfce", 1, 18)
text((x0 + 36, y0 + 34), "Вариант 2", font(FONT_SANS_BOLD, 20), GOLD)
text((x0 + 36, y0 + 72), "Сценарий из 4 карточек", font(FONT_SERIF_BOLD, 48), NAVY)
paragraph(x0 + 38, y0 + 130, "Подходит, если нужно сделать блок более практичным и понятным: каждый шаг как отдельное действие.", font(FONT_SANS, 22), MUTED, 560, 32)
pill(x0 + 38, y0 + 230, 255, 54, "Начать консультацию")
card_w, card_h = 245, 250
start_x = x0 + 600
for idx, (num, title, desc, kind) in enumerate(steps):
    cx = start_x + idx * (card_w + 30)
    rect((cx, y0 + 122, cx + card_w, y0 + 122 + card_h), PAPER, "#e2e8f0", 1, 14)
    circle(cx + 52, y0 + 174, 35, "#fff7ed", "#f0c98b", 2)
    icon(cx + 52, y0 + 174, kind)
    text((cx + 26, y0 + 238), num, font(FONT_SERIF_BOLD, 24), GOLD)
    text((cx + 26, y0 + 278), title, font(FONT_SANS_BOLD, 24), NAVY)
    paragraph(cx + 26, y0 + 320, desc, font(FONT_SANS, 18), INK, 188, 27)

# Variant 3
x0, y0, ww, hh = 70, 1270, 1660, 520
rect((x0, y0, x0 + ww, y0 + hh), GREENISH, "#dbe7e0", 1, 18)
text((x0 + 36, y0 + 34), "Вариант 3", font(FONT_SANS_BOLD, 20), GOLD)
text((x0 + 58, y0 + 92), "От первого запроса\nдо результата", font(FONT_SERIF_BOLD, 50), NAVY)
paragraph(x0 + 60, y0 + 220, "Более современный блок: слева обещание и доверие, справа понятная дорожная карта. Хорошо смотрится на лендинге и не занимает слишком много высоты.", font(FONT_SANS, 23), INK, 520, 34)
rect((x0 + 60, y0 + 374, x0 + 430, y0 + 438), PAPER, "#d7e2ee", 1, 32)
center_text(x0 + 245, y0 + 406, "Прозоро · поетапно · з результатом", font(FONT_SANS_BOLD, 19), NAVY)
road_x = x0 + 720
road_y = y0 + 92
for idx, (num, title, desc, kind) in enumerate(steps):
    yy = road_y + idx * 98
    if idx < 3:
        line([(road_x + 38, yy + 56), (road_x + 38, yy + 98)], "#b8c7d8", 3)
    circle(road_x + 38, yy + 34, 34, PAPER, "#dce6f0", 2)
    icon(road_x + 38, yy + 34, kind)
    text((road_x + 95, yy + 8), f"{num}  {title}", font(FONT_SANS_BOLD, 26), NAVY)
    paragraph(road_x + 95, yy + 45, desc, font(FONT_SANS, 19), INK, 620, 28)

text((70, 1844), "Мой выбор: вариант 3 для более современного лендинга; вариант 1 — если хочется остаться ближе к текущему макету.", font(FONT_SANS_BOLD, 22), NAVY)

img = img.resize((W, H), Image.Resampling.LANCZOS)
OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, quality=95)
print(OUT, img.size)
