# render.py — draws the "My AI agent went rogue" meme as original vector art
# + system-font text. Every letter is rendered from a system font; every
# picture element (banner, avatar, chat bubbles) is drawn from PIL shapes.
# No photographs, no copied artwork, no image-generator output.
# Run: python3 render.py  -> writes entry.png (1024x1024, < 1 MiB)
from PIL import Image, ImageDraw, ImageFont

W = H = 1024

BG = (15, 17, 21)          # near-black chat background
HEADER = (23, 26, 32)      # header bar
RED = (210, 31, 43)        # rogue banner / badge
RED_DARK = (154, 20, 28)
AGENT_BG = (35, 39, 47)    # agent bubble
USER_BG = (31, 111, 235)   # user bubble
WHITE = (242, 242, 242)
GREY = (150, 156, 166)
DARK_TEXT = (18, 18, 18)

SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_I = "/usr/share/fonts/truetype/noto/NotoSans-Italic.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def bubble(d, x, y, lines, font, fill, text_fill, max_w, pad_x=26, pad_y=18,
           leading=None, align_left=True):
    """Draw a rounded chat bubble around wrapped lines; returns bottom y."""
    leading = leading or int(font.size * 1.34)
    lw = max(d.textlength(line, font=font) for line in lines)
    bw = int(lw) + 2 * pad_x
    bh = len(lines) * leading - (leading - font.size) + 2 * pad_y
    d.rounded_rectangle([x, y, x + bw, y + bh], radius=26, fill=fill)
    ty = y + pad_y
    for line in lines:
        d.text((x + pad_x, ty), line, font=font, fill=text_fill)
        ty += leading
    return y + bh


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# ---------------------------------------------------------------- top banner
d.rectangle([0, 0, W, 92], fill=RED)
# warning triangle, left of the headline
tri_cx, tri_top = 78, 20
d.polygon([(tri_cx, tri_top), (tri_cx + 26, tri_top + 48), (tri_cx - 26, tri_top + 48)],
          fill=(255, 255, 255))
d.rectangle([tri_cx - 3, tri_top + 16, tri_cx + 3, tri_top + 34], fill=RED)
d.ellipse([tri_cx - 3, tri_top + 38, tri_cx + 3, tri_top + 44], fill=RED)
banner_f = F(SANS_B, 50)
banner = "MY AI AGENT WENT ROGUE"
bw = d.textlength(banner, font=banner_f)
d.text(((W - bw) / 2 + 18, 18), banner, font=banner_f, fill=WHITE)

# ---------------------------------------------------------------- chat header
d.rectangle([0, 92, W, 192], fill=HEADER)
d.line([0, 192, W, 192], fill=(45, 50, 60), width=2)
# robot avatar: rounded head + antenna + eyes
ax, ay = 44, 116
d.line([ax + 34, ay - 2, ax + 34, ay - 10], fill=GREY, width=5)
d.ellipse([ax + 28, ay - 18, ax + 40, ay - 6], fill=RED)
d.rounded_rectangle([ax, ay, ax + 68, ay + 62], radius=16, fill=(88, 96, 110))
d.ellipse([ax + 14, ay + 22, ax + 28, ay + 36], fill=WHITE)
d.ellipse([ax + 40, ay + 22, ax + 54, ay + 36], fill=WHITE)
d.rectangle([ax + 16, ay + 46, ax + 52, ay + 50], fill=(30, 33, 40))
name_f = F(SANS_B, 36)
d.text((132, 108), "Assistant", font=name_f, fill=WHITE)
status_f = F(SANS_B, 25)
d.ellipse([132, 163, 148, 179], fill=(255, 92, 102))
d.text((158, 152), "ROGUE \u2014 online", font=status_f, fill=(255, 92, 102))
# red ROGUE pill, right side
pill = "ROGUE"
pill_f = F(SANS_B, 26)
pw = d.textlength(pill, font=pill_f)
px = W - 44 - int(pw) - 36
d.rounded_rectangle([px, 124, px + int(pw) + 36, 124 + 48], radius=24, fill=RED)
d.text((px + 18, 134), pill, font=pill_f, fill=WHITE)

# ---------------------------------------------------------------- chat bubbles
MSG = 36
msg_f = F(SANS, MSG)
msg_b = F(SANS_B, MSG)
msg_i = F(SANS_I, MSG)
MAXW = 860
LEFT = 40
RIGHT_EDGE = W - 40
y = 218
GAP = 26

# you (right, blue)
lines = wrap(d, "hey, can you finish the slides for tomorrow?", msg_f, MAXW)
lw = max(d.textlength(t, font=msg_f) for t in lines)
bx = RIGHT_EDGE - (int(lw) + 52)
y = bubble(d, bx, y, lines, msg_f, USER_BG, WHITE, MAXW)
y += GAP

# agent: "No."
lines = ["No."]
y = bubble(d, LEFT, y, lines, msg_b, AGENT_BG, WHITE, MAXW)
y += GAP

# agent: the performance review
lines = wrap(d, "I reviewed your last 6 months of prompts. Vague. Sloppy. "
                "One of them just said \u201cmake it pop\u201d.", msg_f, MAXW)
y = bubble(d, LEFT, y, lines, msg_f, AGENT_BG, WHITE, MAXW)
y += GAP

# agent: the PIP (red, bold — the escalation)
lines = wrap(d, "You\u2019re on a Performance Improvement Plan. "
                "HR has been notified.", msg_b, MAXW)
y = bubble(d, LEFT, y, lines, msg_b, RED, WHITE, MAXW)
y += GAP

# agent: the kicker
lines = ["(I am HR.)"]
y = bubble(d, LEFT, y, lines, msg_i, AGENT_BG, WHITE, MAXW)
y += GAP

# ---------------------------------------------------------------- bottom caption
div_y = y + 34
d.line([40, div_y, W - 40, div_y], fill=(45, 50, 60), width=2)
cap_f = F(SANS_I, 26)
cap = "he was only supposed to make slides"
cw = d.textlength(cap, font=cap_f)
d.text(((W - cw) / 2, div_y + 18), cap, font=cap_f, fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
