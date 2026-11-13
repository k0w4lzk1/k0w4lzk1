#!/usr/bin/env python3
"""Generates every SVG in assets/. Edit the data below and run: python3 scripts/build.py"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

HANDLE = "k0w4lzk1"
NAME = "Kartik T Nair"
TAGLINE = "Web security. CTFs with team bi0s."
PILL = "client-side web / xs-leaks / AI security"
HUD = [("WRITEUPS", "08", "published on the blog"),
       ("PULL REQUESTS", "35", "merged on GitHub"),
       ("TEAM", "bi0s", "web, CTF")]
STAGES = [("out-py", "Out-Py", "VS Code extension", "JavaScript"),
          ("dhwani", "DHWANI", "Rural health app", "Dart / Python"),
          ("langurtrace", "LangurTrace", "Forensics paper, rebuilt", "Python / TeX")]
BUTTONS = [("blog", "Blog", True), ("bi0s", "Team bi0s", False), ("x", "X / Twitter", False), ("gists", "Gists", False)]

THEMES = {
    "dark": dict(bg="#0d1117", panel="#161b22", line="#30363d", text="#e6edf3", mute="#7d8590",
                 wall="#1f6f3a", pellet="#6e7681", body="#3fb950", head="#7ee787", eye="#0d1117",
                 flag="#d29922", foe="#f85149", accent="#3fb950"),
    "light": dict(bg="#ffffff", panel="#f6f8fa", line="#d0d7de", text="#1f2328", mute="#656d76",
                  wall="#8ddb9f", pellet="#afb8c1", body="#1a7f37", head="#2da44e", eye="#ffffff",
                  flag="#bf8700", foe="#cf222e", accent="#1a7f37"),
}
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"
BASE_CSS = f"text{{font-family:{SANS}}}.m{{font-family:{MONO}}}"
REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"

BUG_A = ["..X..X.....", "..X..X...h.", ".XXXXXX.h..", "XXXXXXXhhh.", "XXXXXXXhhe.",
         "XXXXXXXhhh.", ".XXXXXX.h..", "..X..X...h.", "..X..X....."]
BUG_B = [".X..X......", "..X..X...h.", ".XXXXXX.h..", "XXXXXXXhhh.", "XXXXXXXhhe.",
         "XXXXXXXhhh.", ".XXXXXX.h..", "..X..X...h.", ".X..X......"]


def sprite(rows, t, c):
    col = {"X": t["body"], "h": t["head"], "e": t["eye"]}
    return "".join(f'<rect x="{k*c:g}" y="{r*c:g}" width="{c:g}" height="{c:g}" fill="{col[ch]}"/>'
                   for r, row in enumerate(rows) for k, ch in enumerate(row) if ch in col)


def bug(t, c):
    w, h = 11 * c, 9 * c
    return (f'<g transform="translate({-w/2:g},{-h/2:g})"><g class="f1">{sprite(BUG_A, t, c)}</g>'
            f'<g class="f2">{sprite(BUG_B, t, c)}</g></g>')


BUG_CSS = (".f1{animation:fa .3s steps(1) infinite}.f2{opacity:0;animation:fb .3s steps(1) infinite}"
           "@keyframes fa{0%{opacity:1}50%{opacity:0}}@keyframes fb{0%{opacity:0}50%{opacity:1}}")


def flag(x, y, t, s=1.0):
    return (f'<rect x="{x-4*s:g}" y="{y-9*s:g}" width="{2*s:g}" height="{18*s:g}" fill="{t["mute"]}"/>'
            f'<path d="M{x-2*s:g} {y-9*s:g}h{10*s:g}v{7*s:g}h{-10*s:g}z" fill="{t["flag"]}"/>')


def foe(label, t):
    return (f'<rect x="-15" y="-8" width="30" height="16" rx="3" fill="{t["bg"]}" stroke="{t["foe"]}" stroke-width="1.5"/>'
            f'<text class="m" y="3.5" font-size="9" font-weight="700" fill="{t["foe"]}" text-anchor="middle">{label}</text>')


def svg(w, h, label, css, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}">\n'
            f'<title>{label}</title>\n<style>{BASE_CSS}{css}{REDUCED}</style>\n{body}\n</svg>\n')


def write(name, content):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)


# ---------------------------------------------------------------- hero
CELL, OX, OY, CW = 36, 448, 48, 24
EDGES_H = [(0, 0, 10), (2, 0, 5), (2, 8, 10), (4, 0, 2), (4, 5, 10), (6, 0, 10)]   # row, col from, col to
EDGES_V = [(0, 0, 6), (10, 0, 6), (2, 2, 6), (5, 0, 4), (8, 0, 2), (8, 4, 6)]      # col, row from, row to
RUN = [(0, 0), (5, 0), (5, 4), (10, 4), (10, 6), (2, 6), (2, 2), (0, 2), (0, 0)]   # the bug's lap
PATROL = [(10, 0), (8, 0), (8, 2), (10, 2), (10, 0)]
STEP = 0.5  # seconds per cell


def pt(c, r):
    return OX + c * CELL, OY + r * CELL


def expand(corners):
    out = [corners[0]]
    for (c1, r1), (c2, r2) in zip(corners, corners[1:]):
        n = abs(c2 - c1) + abs(r2 - r1)
        for i in range(1, n + 1):
            out.append((c1 + (c2 - c1) * i // n, r1 + (r2 - r1) * i // n))
    return out


def path_d(corners):
    return "M" + "L".join(f"{pt(c, r)[0]} {pt(c, r)[1]}" for c, r in corners[:-1]) + "Z"


def hero(t):
    W, H = 840, 312
    lap = expand(RUN)[:-1]
    dur = len(lap) * STEP
    nodes = set()
    segs = []
    for r, a, b in EDGES_H:
        nodes |= {(c, r) for c in range(a, b + 1)}
        segs.append(f"M{pt(a, r)[0]} {pt(a, r)[1]}H{pt(b, r)[0]}")
    for c, a, b in EDGES_V:
        nodes |= {(c, r) for r in range(a, b + 1)}
        segs.append(f"M{pt(c, a)[0]} {pt(c, a)[1]}V{pt(c, b)[1]}")
    d = "".join(segs)
    flags = {lap[9], lap[16], lap[28]}
    css = (f".run{{offset-path:path('{path_d(RUN)}');offset-rotate:auto;animation:lap {dur:g}s linear infinite}}"
           f".chase{{offset-path:path('{path_d(RUN)}');offset-rotate:0deg;animation:lap {dur:g}s linear infinite;animation-delay:{-(dur-2.5):g}s}}"
           f".patrol{{offset-path:path('{path_d(PATROL)}');offset-rotate:0deg;animation:lap 7s linear infinite}}"
           f".d{{animation:eat {dur:g}s steps(1) infinite}}"
           "@keyframes lap{from{offset-distance:0%}to{offset-distance:100%}}"
           "@keyframes eat{0%{opacity:0}60%{opacity:1}}"
           ".cur{animation:fa 1.1s steps(1) infinite}" + BUG_CSS +
           "@media (prefers-reduced-motion:reduce){.run{offset-distance:22%}.chase{offset-distance:12%}}")
    o = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="{t["bg"]}" stroke="{t["line"]}"/>']
    # left column
    o.append(f'<text class="m" x="44" y="96" font-size="14" fill="{t["accent"]}">{HANDLE}<tspan class="cur">_</tspan></text>')
    o.append(f'<text x="43" y="146" font-size="40" font-weight="700" fill="{t["text"]}">{NAME}</text>')
    o.append(f'<text x="44" y="182" font-size="16" fill="{t["mute"]}">{TAGLINE}</text>')
    o.append(f'<rect x="44" y="208" width="{len(PILL)*6.65+48:.0f}" height="30" rx="15" fill="{t["panel"]}" stroke="{t["line"]}"/>')
    o.append(f'<rect x="58" y="219" width="8" height="8" fill="{t["accent"]}"/>')
    o.append(f'<text class="m" x="76" y="227.5" font-size="11" fill="{t["text"]}">{PILL}</text>')
    # maze
    o.append(f'<path d="{d}" fill="none" stroke="{t["wall"]}" stroke-width="{CW+4}" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append(f'<path d="{d}" fill="none" stroke="{t["bg"]}" stroke-width="{CW}" stroke-linecap="round" stroke-linejoin="round"/>')
    order = {n: i for i, n in enumerate(lap)}
    for n in sorted(nodes):
        x, y = pt(*n)
        if n in order:
            st = f'class="d" style="animation-delay:{order[n]*STEP:g}s"'
            if n in flags:
                o.append(f'<g {st}>{flag(x, y, t)}</g>')
            else:
                o.append(f'<rect {st} x="{x-2}" y="{y-2}" width="4" height="4" fill="{t["pellet"]}"/>')
        else:
            o.append(f'<rect x="{x-2}" y="{y-2}" width="4" height="4" fill="{t["pellet"]}"/>')
    o.append(f'<g class="patrol">{foe("CSP", t)}</g>')
    o.append(f'<g class="chase">{foe("WAF", t)}</g>')
    o.append(f'<g class="run">{bug(t, 2)}</g>')
    label = f"{NAME} ({HANDLE}). {TAGLINE}"
    return svg(W, H, label, css, "\n".join(o))


# ---------------------------------------------------------------- hud
def hud(t):
    W, H, gap = 840, 92, 18
    tw = (W - 2 * gap) / 3
    o = []
    for i, (label, value, sub) in enumerate(HUD):
        x = i * (tw + gap)
        o.append(f'<rect x="{x+.5:g}" y=".5" width="{tw-1:g}" height="{H-1}" rx="10" fill="{t["panel"]}" stroke="{t["line"]}"/>')
        o.append(f'<text class="m" x="{x+20:g}" y="28" font-size="11" letter-spacing="1.5" fill="{t["mute"]}">{label}</text>')
        o.append(f'<text class="m" x="{x+20:g}" y="62" font-size="30" font-weight="700" fill="{t["text"]}">{value}</text>')
        o.append(f'<text x="{x+20:g}" y="80" font-size="11" fill="{t["mute"]}">{sub}</text>')
        o.append(flag(x + tw - 24, 26, t))
    label = " · ".join(f"{v} {l.lower()}" for l, v, s in HUD)
    return svg(W, H, label, "", "\n".join(o))


# ---------------------------------------------------------------- divider
def divider(t):
    W, H, dur = 840, 24, 12.0
    y = H / 2
    a, b = -30, W + 30
    css = (f".dr{{animation:dx {dur:g}s linear infinite}}.dd{{animation:deat {dur:g}s steps(1) infinite}}"
           f"@keyframes dx{{from{{transform:translateX({a}px)}}to{{transform:translateX({b}px)}}}}"
           "@keyframes deat{0%{opacity:0}50%{opacity:1}}" + BUG_CSS +
           "@media (prefers-reduced-motion:reduce){.dr{transform:translateX(-40px)}}")
    o = []
    for x in range(12, W, 24):
        delay = (x - 8 - a) / (b - a) * dur
        o.append(f'<rect class="dd" style="animation-delay:{delay:.2f}s" x="{x-1.5:g}" y="{y-1.5:g}" width="3" height="3" fill="{t["pellet"]}"/>')
    o.append(f'<g class="dr"><g transform="translate(0,{y:g})">{bug(t, 1.5)}</g></g>')
    return svg(W, H, "", css, "\n".join(o))


# ---------------------------------------------------------------- stage covers and buttons (one variant, read on both themes)
def stage(i, title, kind, tech):
    t = THEMES["dark"]
    W, H = 400, 150
    o = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="10" fill="{t["bg"]}" stroke="{t["line"]}"/>',
         f'<text class="m" x="24" y="38" font-size="11" letter-spacing="2" fill="{t["accent"]}">STAGE {i:02d}</text>',
         f'<text x="23" y="74" font-size="26" font-weight="700" fill="{t["text"]}">{title}</text>',
         f'<text x="24" y="96" font-size="13" fill="{t["mute"]}">{kind}</text>',
         f'<text class="m" x="{W-24}" y="38" font-size="11" fill="{t["mute"]}" text-anchor="end">{tech}</text>']
    y = 124
    eaten = 1 + i * 2
    xs = list(range(30, W - 40, 22))
    for k, x in enumerate(xs):
        if k > eaten:
            o.append(f'<rect x="{x-1.5:g}" y="{y-1.5:g}" width="3" height="3" fill="{t["pellet"]}"/>')
    o.append(f'<g transform="translate({xs[eaten]},{y})">{bug(t, 1.5)}</g>')
    o.append(flag(W - 28, y, t))
    return svg(W, H, f"Stage {i:02d}: {title}", BUG_CSS, "\n".join(o))


def button(label, primary):
    t = THEMES["dark"]
    w, h = round(len(label) * 7.6) + 34, 36
    face, edge, ink = (("#2ea043", "#1a7f37", "#ffffff") if primary else ("#21262d", "#0d1117", "#e6edf3"))
    o = [f'<rect x=".5" y="3.5" width="{w-1}" height="{h-4}" rx="6" fill="{edge}" stroke="{t["line"]}"/>',
         f'<rect x=".5" y=".5" width="{w-1}" height="{h-4}" rx="6" fill="{face}" stroke="{t["line"]}"/>',
         f'<text class="m" x="{w/2:g}" y="20.5" font-size="12.5" font-weight="700" fill="{ink}" text-anchor="middle">{label}</text>']
    return svg(w, h, label, "", "\n".join(o))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, t in THEMES.items():
        write(f"hero-{name}.svg", hero(t))
        write(f"hud-{name}.svg", hud(t))
        write(f"divider-{name}.svg", divider(t))
    for i, (slug, title, kind, tech) in enumerate(STAGES, 1):
        write(f"stage-{slug}.svg", stage(i, title, kind, tech))
    for slug, label, primary in BUTTONS:
        write(f"btn-{slug}.svg", button(label, primary))
    print("wrote", len(os.listdir(OUT)), "files")
