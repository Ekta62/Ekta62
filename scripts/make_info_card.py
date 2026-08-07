#!/usr/bin/env python3
"""Hand-author the neofetch-style info card SVG.

Each line fades and slides in on a short stagger (CSS keyframes inside
the SVG — GitHub plays them), then holds and loops so the card keeps
"retyping" itself for repeat visitors. STATIC=1 emits a frozen frame
for Quick Look. Colors are theme-aware via prefers-color-scheme, so the
card doesn't show as a dark box on a light GitHub theme.

Usage: python scripts/make_info_card.py
Writes info-card.svg.
"""
import html
import os

DARK = dict(bg="#0d1117", border="#30363d", key="#39d353", val="#c9d1d9", dim="#8b949e", accent="#e0607e")

W = 560
LINE_H = 27
STAGGER = 0.28
LOOP_DUR = 24  # seconds per retype cycle

TITLE = "ekta@github"
ROWS = [
    ("", ""),
    ("Name", "Ekta Bhaggi"),
    ("Location", "Phagwara, Punjab, India"),
    ("Role", "Assistant Professor @ GNA University"),
    ("", ""),
    ("Teaching", "Python · Cloud Computing · DevOps"),
    ("", "Data Warehousing & Mining"),
    ("Research", "Author, \"Fundamentals of AI\" · Data Science"),
    ("Mentoring", "Student projects · Time Table Coordinator"),
    ("", ""),
    ("Stack", "AWS · Microsoft Azure · Docker · Kubernetes"),
    ("Tools", "Power BI · Tableau · RapidMiner · Git"),
    ("Certified", "12 credentials — AWS, Azure, Power BI, DevOps"),
    ("", ""),
    ("Contact", "linkedin.com/in/ekta-"),
]
PALETTE = ["#ff7b72", "#ffa657", "#d29922", "#39d353", "#58a6ff", "#bc8cff", "#f778ba", "#c9d1d9"]


def theme_css() -> str:
    c = DARK
    return (
        f".bg{{fill:{c['bg']}}}.bd{{stroke:{c['border']}}}"
        f".key{{fill:{c['key']}}}.val{{fill:{c['val']}}}"
        f".dim{{fill:{c['dim']}}}.accent{{fill:{c['accent']}}}"
    )


def main() -> None:
    static = os.environ.get("STATIC") == "1"
    blanks = sum(1 for k, v in ROWS if not k and not v)
    lines = len(ROWS) - blanks
    H = round(106 + blanks * LINE_H * 0.45 + lines * LINE_H + 6 + 16 + 24)

    if static:
        anim_css = ""
    else:
        anim_css = (
            ".ln{opacity:0;animation:in "
            f"{LOOP_DUR}s ease-out infinite}}"
            "@keyframes in{0%{opacity:0;transform:translateX(-8px)}"
            "2%{opacity:1;transform:none}90%{opacity:1;transform:none}"
            "92%,100%{opacity:0;transform:translateX(-8px)}}"
        )

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="14" '
        f'role="img" aria-labelledby="t d">',
        "<title id=\"t\">Ekta Bhaggi — GitHub info card</title>",
        "<desc id=\"d\">Terminal-style card: role, teaching, research, certifications, and contact.</desc>",
        f"<style>{theme_css()}{anim_css}</style>",
        f'<rect class="bg bd" x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="8"/>',
        # title bar
        f'<circle cx="22" cy="21" r="6" fill="#ff5f57"/>'
        f'<circle cx="42" cy="21" r="6" fill="#febc2e"/>'
        f'<circle cx="62" cy="21" r="6" fill="#28c840"/>',
        f'<text class="dim" x="{W / 2:.0f}" y="26" text-anchor="middle">{TITLE}</text>',
        f'<line class="bd" x1="1" y1="40" x2="{W - 1}" y2="40"/>',
    ]

    y = 72
    delay = 0.15
    parts.append(
        f'<g class="ln" style="animation-delay:{delay:.2f}s">'
        f'<text class="accent" x="24" y="{y}">{TITLE}</text>'
        f'<text class="dim" x="24" y="{y + 16}">{"-" * len(TITLE)}</text></g>'
    )
    y += 34
    for key, val in ROWS:
        delay += STAGGER * 0.55
        if not key and not val:
            y += LINE_H * 0.45
            continue
        if key:
            parts.append(
                f'<g class="ln" style="animation-delay:{delay:.2f}s">'
                f'<text x="24" y="{y}"><tspan class="key">{html.escape(key)}</tspan>'
                f'<tspan class="dim">: </tspan>'
                f'<tspan class="val" x="130">{html.escape(val)}</tspan></text></g>'
            )
        else:
            parts.append(
                f'<g class="ln" style="animation-delay:{delay:.2f}s">'
                f'<text class="dim" x="130" y="{y}">{html.escape(val)}</text></g>'
            )
        y += LINE_H

    # classic neofetch palette blocks
    delay += 0.3
    y += 6
    sw = 30
    x0 = (W - sw * len(PALETTE)) / 2
    blocks = "".join(
        f'<rect x="{x0 + i * sw:.0f}" y="{y}" width="{sw}" height="16" fill="{c}"/>'
        for i, c in enumerate(PALETTE)
    )
    parts.append(f'<g class="ln" style="animation-delay:{delay:.2f}s">{blocks}</g>')
    parts.append("</svg>")

    with open("info-card.svg", "w") as f:
        f.write("\n".join(parts))
    print("wrote info-card.svg")


if __name__ == "__main__":
    main()
