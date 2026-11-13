#!/usr/bin/env python3
"""Draws assets/screen.svg. Change the text below and run: python3 scripts/build.py"""
import os

TITLE = "K0W4LZK1"
TOP_LEFT, TOP_RIGHT = "TEAM BI0S", "WEB SECURITY / CTF"
START = "PRESS START"
BOTTOM = "XSS - XS-LEAKS - AI SECURITY"

W, H = 840, 380
BG, YELLOW, PINK, CYAN, WHITE, DIM, GREEN, LIME, RED = (
    "#07070d", "#ffd23f", "#ff3d6e", "#5ef2ff", "#f4f4f8", "#5b5b78", "#39d353", "#9be9a8", "#ff4d5e")

FONT = {
 "A": ".XXX.|X...X|X...X|XXXXX|X...X|X...X|X...X", "B": "XXXX.|X...X|X...X|XXXX.|X...X|X...X|XXXX.",
 "C": ".XXX.|X...X|X....|X....|X....|X...X|.XXX.", "D": "XXXX.|X...X|X...X|X...X|X...X|X...X|XXXX.",
 "E": "XXXXX|X....|X....|XXXX.|X....|X....|XXXXX", "F": "XXXXX|X....|X....|XXXX.|X....|X....|X....",
 "G": ".XXX.|X...X|X....|X.XXX|X...X|X...X|.XXX.", "H": "X...X|X...X|X...X|XXXXX|X...X|X...X|X...X",
 "I": "XXXXX|..X..|..X..|..X..|..X..|..X..|XXXXX", "J": "..XXX|...X.|...X.|...X.|...X.|X..X.|.XX..",
 "K": "X...X|X..X.|X.X..|XX...|X.X..|X..X.|X...X", "L": "X....|X....|X....|X....|X....|X....|XXXXX",
 "M": "X...X|XX.XX|X.X.X|X.X.X|X...X|X...X|X...X", "N": "X...X|XX..X|X.X.X|X..XX|X...X|X...X|X...X",
 "O": ".XXX.|X...X|X...X|X...X|X...X|X...X|.XXX.", "P": "XXXX.|X...X|X...X|XXXX.|X....|X....|X....",
 "Q": ".XXX.|X...X|X...X|X...X|X.X.X|X..X.|.XX.X", "R": "XXXX.|X...X|X...X|XXXX.|X.X..|X..X.|X...X",
 "S": ".XXXX|X....|X....|.XXX.|....X|....X|XXXX.", "T": "XXXXX|..X..|..X..|..X..|..X..|..X..|..X..",
 "U": "X...X|X...X|X...X|X...X|X...X|X...X|.XXX.", "V": "X...X|X...X|X...X|X...X|X...X|.X.X.|..X..",
 "W": "X...X|X...X|X...X|X.X.X|X.X.X|XX.XX|X...X", "X": "X...X|X...X|.X.X.|..X..|.X.X.|X...X|X...X",
 "Y": "X...X|X...X|.X.X.|..X..|..X..|..X..|..X..", "Z": "XXXXX|....X|...X.|..X..|.X...|X....|XXXXX",
 "0": ".XXX.|X...X|X..XX|X.X.X|XX..X|X...X|.XXX.", "1": "..X..|.XX..|..X..|..X..|..X..|..X..|.XXX.",
 "2": ".XXX.|X...X|....X|...X.|..X..|.X...|XXXXX", "3": "XXXX.|....X|....X|.XXX.|....X|....X|XXXX.",
 "4": "...X.|..XX.|.X.X.|X..X.|XXXXX|...X.|...X.", "5": "XXXXX|X....|XXXX.|....X|....X|X...X|.XXX.",
 "6": ".XXX.|X....|X....|XXXX.|X...X|X...X|.XXX.", "7": "XXXXX|....X|...X.|..X..|..X..|..X..|..X..",
 "8": ".XXX.|X...X|X...X|.XXX.|X...X|X...X|.XXX.", "9": ".XXX.|X...X|X...X|.XXXX|....X|....X|.XXX.",
 "-": ".....|.....|.....|XXXXX|.....|.....|.....", "/": "....X|....X|...X.|..X..|.X...|X....|X....",
 ".": ".....|.....|.....|.....|.....|.XX..|.XX..", " ": ".....|.....|.....|.....|.....|.....|.....",
}
BUG_A = ["..X..X.....", "..X..X...h.", ".XXXXXX.h..", "XXXXXXXhhh.", "XXXXXXXhhe.",
         "XXXXXXXhhh.", ".XXXXXX.h..", "..X..X...h.", "..X..X....."]
BUG_B = [".X..X......", "..X..X...h.", ".XXXXXX.h..", "XXXXXXXhhh.", "XXXXXXXhhe.",
         "XXXXXXXhhh.", ".XXXXXX.h..", "..X..X...h.", ".X..X......"]


def text_w(s, c):
    return len(s) * 6 * c - c


def pixels(s, x, y, c, fill):
    """Pixel text as one path; horizontal runs are merged."""
    d = []
    for i, ch in enumerate(s):
        for r, row in enumerate(FONT[ch].split("|")):
            k = 0
            while k < 5:
                if row[k] == "X":
                    j = k
                    while j < 5 and row[j] == "X":
                        j += 1
                    d.append(f"M{x + (i*6 + k)*c:g} {y + r*c:g}h{(j-k)*c:g}v{c:g}h{-(j-k)*c:g}z")
                    k = j
                else:
                    k += 1
    return f'<path d="{"".join(d)}" fill="{fill}"/>'


def centered(s, y, c, fill):
    return pixels(s, (W - text_w(s, c)) / 2, y, c, fill)


def sprite(rows, c):
    col = {"X": GREEN, "h": LIME, "e": BG}
    return "".join(f'<rect x="{k*c}" y="{r*c}" width="{c}" height="{c}" fill="{col[ch]}"/>'
                   for r, row in enumerate(rows) for k, ch in enumerate(row) if ch in col)


def build():
    dur, y = 13.0, 236
    a, b = -80, W + 80
    css = (f".run{{animation:x {dur:g}s linear infinite}}"
           f".foe{{animation:x {dur:g}s linear infinite;animation-delay:1.3s;animation-fill-mode:backwards}}"
           f".p{{animation:eat {dur:g}s steps(1) infinite}}"
           ".f1{animation:a .28s steps(1) infinite}.f2{opacity:0;animation:b .28s steps(1) infinite}"
           ".start{animation:a 1.1s steps(1) infinite}"
           f"@keyframes x{{from{{transform:translateX({a}px)}}to{{transform:translateX({b}px)}}}}"
           "@keyframes eat{0%{opacity:0}55%{opacity:1}}"
           "@keyframes a{0%{opacity:1}50%{opacity:0}}@keyframes b{0%{opacity:0}50%{opacity:1}}"
           "@media (prefers-reduced-motion:reduce){*{animation:none!important}"
           ".run{transform:translateX(330px)}.foe{transform:translateX(200px)}}")
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{TITLE}">',
         f"<title>{TITLE}</title><style>{css}</style>",
         '<defs><pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" y="2" fill="#000" opacity=".28"/></pattern>'
         '<radialGradient id="vig" cx="50%" cy="50%" r="72%"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".75"/></radialGradient>'
         f'<clipPath id="tube"><rect x="14" y="14" width="{W-28}" height="{H-28}" rx="26"/></clipPath></defs>',
         f'<rect width="{W}" height="{H}" rx="22" fill="#1a1a22"/>',
         f'<rect x="14" y="14" width="{W-28}" height="{H-28}" rx="26" fill="{BG}"/>',
         '<g clip-path="url(#tube)">',
         pixels(TOP_LEFT, 48, 44, 2, CYAN),
         pixels(TOP_RIGHT, W - 48 - text_w(TOP_RIGHT, 2), 44, 2, CYAN)]
    c = 11
    tx = (W - text_w(TITLE, c)) / 2
    o.append(pixels(TITLE, tx + 6, 96 + 6, c, PINK))
    o.append(pixels(TITLE, tx, 96, c, YELLOW))
    for i, x in enumerate(range(60, W - 40, 32)):
        delay = (x - 18 - a) / (b - a) * dur
        st = f'class="p" style="animation-delay:{delay:.2f}s"'
        if i % 6 == 4:
            o.append(f'<g {st}><rect x="{x-6}" y="{y-12}" width="3" height="24" fill="{WHITE}"/><path d="M{x-3} {y-12}h15v9h-15z" fill="{PINK}"/></g>')
        else:
            o.append(f'<rect {st} x="{x-3}" y="{y-3}" width="6" height="6" fill="{WHITE}"/>')
    o.append(f'<g class="foe"><g transform="translate(-24,{y-13})"><rect x="1.5" y="1.5" width="45" height="23" fill="{BG}" stroke="{RED}" stroke-width="3"/>{pixels("WAF", 7, 6, 2, RED)}</g></g>')
    o.append(f'<g class="run"><g transform="translate(-22,{y-18})"><g class="f1">{sprite(BUG_A, 4)}</g><g class="f2">{sprite(BUG_B, 4)}</g></g></g>')
    o.append(f'<g class="start">{centered(START, 282, 3, WHITE)}</g>')
    o.append(centered(BOTTOM, 328, 2, DIM))
    o.append(f'<rect width="{W}" height="{H}" fill="url(#scan)"/><rect width="{W}" height="{H}" fill="url(#vig)"/>')
    o.append("</g></svg>")
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "screen.svg"), "w") as f:
        f.write("\n".join(o) + "\n")


if __name__ == "__main__":
    build()
