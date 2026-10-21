"""Builds dark_mode.svg and light_mode.svg for the profile README. The build workflow runs it daily."""
import datetime
from html import escape

BIRTHDAY = datetime.date(2004, 8, 12)
W = 66  # characters per text line
ART_LINE = 9.4  # px between portrait rows (portrait font is 8px)
ART_CELL = 4.8  # px per portrait column; each row's width is pinned to this so the face keeps its proportions in any font
ROW = 24  # px between text rows

# ("head", text) | ("kv", key, value) | ("blank",); "{age}" in a value is replaced by the live age
ROWS = [
    ("head", "hashem@awad"),
    ("kv", "OS", "Fedora Linux"),
    ("kv", "Uptime", "{age}"),
    ("kv", "Host", "American University of Beirut (AUB)"),
    ("kv", "Kernel", "B.S. Computer Science, class of 2027"),
    ("kv", "IDE", "VS Code"),
    ("blank",),
    ("kv", "Languages.Programming", "Java, C, C++, Python, Ruby, JavaScript"),
    ("kv", "Languages.Computer", "HTML, CSS, SQL, LaTeX"),
    ("kv", "Languages.Real", "Arabic, English"),
    ("blank",),
    ("kv", "Hobbies.Software", "Linux Ricing"),
    ("kv", "Hobbies.Real", "Swimming"),
    ("blank",),
    ("head", "- Contact"),
    ("kv", "Email.Personal", "Hashemawaddd@gmail.com"),
    ("kv", "Email.University", "hia33@mail.aub.edu"),
    ("kv", "LinkedIn", "hashem-awad-4429ba24a"),
]

THEMES = {
    "dark_mode.svg": dict(bg="#161b22", fg="#c9d1d9", art="#f0f6fc", key="#ffa657", value="#a5d6ff", cc="#616e7f", flip=False),
    "light_mode.svg": dict(bg="#f6f8fa", fg="#24292f", art="#1f2328", key="#953800", value="#0a3069", cc="#afb8c1", flip=True),
}
RAMP = ".:+#@"  # light -> heavy; on a light background the density is reversed so the face stays a face


def age(born, today):
    y, m, d = today.year - born.year, today.month - born.month, today.day - born.day
    if d < 0:
        m -= 1
        d += (today.replace(day=1) - datetime.timedelta(days=1)).day  # days in the previous month
    if m < 0:
        y, m = y - 1, m + 12
    return y, m, d


def age_text(born, today):
    return ", ".join(f"{n} {u}{'' if n == 1 else 's'}" for n, u in zip(age(born, today), ("year", "month", "day")))


def text_lines(today):
    out = []
    for row in ROWS:
        if row[0] == "blank":
            out.append(". ")
        elif row[0] == "head":
            out.append(f"{escape(row[1])} {'-' * (W - len(row[1]) - 1)}")
        else:
            key, value = row[1], row[2].replace("{age}", age_text(BIRTHDAY, today))
            dots = "." * (W - len(f". {key}: ") - len(value) - 1)
            keys = '</tspan>.<tspan class="key">'.join(map(escape, key.split(".")))
            out.append(
                f'<tspan class="cc">. </tspan><tspan class="key">{keys}</tspan>:'
                f'<tspan class="cc"> {dots} </tspan><tspan class="value">{escape(value)}</tspan>'
            )
    return out


def build(art, theme, today):
    if theme["flip"]:
        art = art.translate(str.maketrans(RAMP, RAMP[::-1]))
    art_lines = art.split("\n")
    height = int(20 + len(art_lines) * ART_LINE + 15)
    lines = text_lines(today)
    y0 = (height - len(lines) * ROW) // 2 + 18
    art_xml = "\n".join(
        f'<tspan x="15" y="{20 + i * ART_LINE:.1f}" textLength="{len(line) * ART_CELL:.1f}" lengthAdjust="spacing">{escape(line)}</tspan>'
        for i, line in enumerate(art_lines)
    )
    text_xml = "\n".join(f'<tspan x="462" y="{y0 + i * ROW}">{line}</tspan>' for i, line in enumerate(lines))
    return f"""<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="1000px" height="{height}px" font-size="13px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
-webkit-size-adjust: 109%;
size-adjust: 109%;
}}
.key {{fill: {theme['key']};}}
.value {{fill: {theme['value']};}}
.cc {{fill: {theme['cc']};}}
text, tspan {{white-space: pre;}}
</style>
<rect width="1000px" height="{height}px" fill="{theme['bg']}" rx="15"/>
<text fill="{theme['art']}" font-size="8px" font-weight="bold">
{art_xml}
</text>
<text fill="{theme['fg']}">
{text_xml}
</text>
</svg>
"""


if __name__ == "__main__":
    b = datetime.date(2004, 8, 12)
    assert age(b, datetime.date(2026, 10, 21)) == (22, 2, 9)
    assert age(b, datetime.date(2026, 8, 12)) == (22, 0, 0)
    assert age(b, datetime.date(2026, 9, 11)) == (22, 0, 30)  # borrows from the previous month
    assert age(b, datetime.date(2026, 3, 1)) == (21, 6, 17)  # borrows from the previous year

    art = open("ascii.txt").read().rstrip("\n")
    today = datetime.date.today()
    for name, theme in THEMES.items():
        open(name, "w").write(build(art, theme, today))
