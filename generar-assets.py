# Genera los SVG del README (banner, diálogos, encabezados, stats y pie) con estética DELTARUNE.
# Las fuentes y el alma van incrustadas en base64 porque GitHub no deja cargar archivos externos dentro de un SVG.
# Uso: python generar-assets.py   (necesita Pillow; toma las fuentes del portafolio)
import base64
import io
import math
import random
from pathlib import Path

from PIL import Image

PUBLIC = Path(r'C:\Users\USER\Documents\Portfolio\Portfolio.Frontend\public')
OUT = Path(__file__).resolve().parent / 'assets'
OUT.mkdir(exist_ok=True)

# Paleta del portafolio
WHITE, YELLOW, SOUL, GRAY, DIM = '#ffffff', '#ffff00', '#d535d9', '#9a9a9a', '#444444'
FRAME, FRAME_DIM = '#cfcaf0', '#3d3352'
KRIS, SUSIE, RALSEI, TP = '#00c2ff', '#ff6ad5', '#5dff8a', '#ff9f2e'


def b64(path):
    return base64.b64encode(Path(path).read_bytes()).decode()


FONT_FILES = {
    'DTM Sans': PUBLIC / 'fonts/DeterminationSansWeb.ttf',
    'DTM Mono': PUBLIC / 'fonts/DeterminationMonoWeb.ttf',
    'DR Logo': PUBLIC / 'fonts/logo_font_dr.ttf',
}
SOUL_PNG = b64(PUBLIC / 'soul.png')


def fonts_css(*names):
    return ''.join(
        f"@font-face{{font-family:'{n}';src:url(data:font/ttf;base64,{b64(FONT_FILES[n])}) format('truetype');}}"
        for n in names
    )


def esc(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def svg(w, h, body, css='', title=''):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}">'
        f'<title>{esc(title)}</title><style>{css}'
        'text{font-kerning:none;text-rendering:optimizeSpeed}'
        '.px{image-rendering:pixelated;image-rendering:crisp-edges}</style>'
        f'{body}</svg>'
    )


def write(name, content):
    (OUT / name).write_text(content, encoding='utf-8')
    print(f'{name}: {len(content.encode()) // 1024} KB')


def soul(x, y, size, extra=''):
    return (f'<image class="px" x="{x}" y="{y}" width="{size}" height="{size}" '
            f'href="data:image/png;base64,{SOUL_PNG}" xlink:href="data:image/png;base64,{SOUL_PNG}" {extra}/>')


def dw_box(w, h, scale=2):
    """Caja "darkworld" del juego: 9 partes de 16 px con el centro estirado, como el border-image del portafolio."""
    src = Image.open(PUBLIC / 'ui/box-darkworld.png').convert('RGBA')
    bw, bh = w // scale, h // scale
    img = Image.new('RGBA', (bw, bh), (1, 1, 1, 255))
    c = 16
    for sx, dx in ((0, 0), (17, bw - 16)):
        for sy, dy in ((0, 0), (17, bh - 16)):
            img.paste(src.crop((sx, sy, sx + 16, sy + 16)), (dx, dy))
    top, bottom = src.crop((c, 0, c + 1, 16)), src.crop((c, 17, c + 1, 33))
    left, right = src.crop((0, c, 16, c + 1)), src.crop((17, c, 33, c + 1))
    img.paste(top.resize((bw - 32, 16)), (16, 0))
    img.paste(bottom.resize((bw - 32, 16)), (16, bh - 16))
    img.paste(left.resize((16, bh - 32)), (0, 16))
    img.paste(right.resize((16, bh - 32)), (bw - 16, 16))
    img = img.resize((bw * scale, bh * scale), Image.NEAREST)
    buf = io.BytesIO()
    img.save(buf, 'PNG', optimize=True)
    data = base64.b64encode(buf.getvalue()).decode()
    return (f'<image class="px" x="0" y="0" width="{bw * scale}" height="{bh * scale}" '
            f'href="data:image/png;base64,{data}" xlink:href="data:image/png;base64,{data}"/>')


def pixel_star(x, y, s, color, cls=''):
    """Estrellita de 4 puntas hecha con cuadros, como los destellos del juego."""
    p = [(0, -2), (0, -1), (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (0, 1), (0, 2)]
    rects = ''.join(f'<rect x="{x + dx * s}" y="{y + dy * s}" width="{s}" height="{s}"/>' for dx, dy in p)
    return f'<g fill="{color}" class="{cls}">{rects}</g>'


# ---------------------------------------------------------------- Banner

def banner():
    W, H = 1200, 440
    random.seed(7)
    css = fonts_css('DTM Sans', 'DTM Mono', 'DR Logo') + (
        '@keyframes tw{0%,100%{opacity:.15}50%{opacity:1}}'
        '.tw{animation:tw 3s steps(4) infinite}'
        '@keyframes bob{0%,100%{transform:translateX(0)}50%{transform:translateX(-8px)}}'
        '.bob{animation:bob 1.2s steps(3) infinite}'
        '@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}'
        '.blink{animation:blink 1s infinite}'
    )
    body = [f'<rect width="{W}" height="{H}" fill="#000"/>']

    # Cielo con estrellas que titilan
    for _ in range(70):
        x, y = random.randint(0, W), random.randint(0, 290)
        s = random.choice((2, 2, 3, 4))
        color = random.choice((WHITE, FRAME, FRAME, SOUL))
        delay = random.random() * 3
        body.append(f'<rect class="tw" style="animation-delay:-{delay:.2f}s" x="{x}" y="{y}" '
                    f'width="{s}" height="{s}" fill="{color}"/>')
    for x, y, s, d in ((90, 70, 3, 0.3), (1110, 110, 3, 1.4), (240, 230, 2, 2.1), (980, 250, 2, 0.8), (1050, 40, 2, 1.9)):
        body.append(f'<g class="tw" style="animation-delay:-{d}s">{pixel_star(x, y, s, WHITE)}</g>')

    # Suelo cuadriculado en perspectiva que avanza (como el Mundo Cibernético)
    horizon, floor_h = 312, H - 312
    body.append('<defs><linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">'
                f'<stop offset="0" stop-color="#000" stop-opacity="1"/><stop offset=".55" stop-color="#000" stop-opacity="0"/>'
                '</linearGradient><clipPath id="floor"><rect x="0" y="312" width="1200" height="128"/></clipPath></defs>')
    grid = [f'<g clip-path="url(#floor)" stroke="{SOUL}" stroke-width="2" shape-rendering="crispEdges">']
    vx = W / 2
    for i in range(-14, 15):
        grid.append(f'<line x1="{vx}" y1="{horizon}" x2="{vx + i * 130}" y2="{H}" stroke-opacity=".55"/>')
    n, k, zmin = 9, 360, 2.6
    for i in range(n):
        ys = [horizon + k / (zmin + (i + 1 - t / 24) * 1.15) for t in range(25)]
        frames = ''.join(f'{t / 24 * 100:.2f}%{{transform:translateY({y - ys[0]:.1f}px)}}' for t, y in enumerate(ys))
        css += f'@keyframes fl{i}{{{frames}}}.fl{i}{{animation:fl{i} 1.6s linear infinite}}'
        grid.append(f'<line class="fl{i}" x1="0" x2="{W}" y1="{ys[0]:.1f}" y2="{ys[0]:.1f}" stroke-opacity=".8"/>')
    grid.append(f'<line x1="0" x2="{W}" y1="{horizon}" y2="{horizon}" stroke="{FRAME}" stroke-opacity=".9"/>')
    grid.append('</g>')
    body += grid
    body.append(f'<rect x="0" y="{horizon}" width="{W}" height="{floor_h}" fill="url(#fade)"/>')

    # Nombre con el alma como cursor del menú
    title = 'Nicholas De la Rosa'  # en mayúsculas la fuente pone corazones en todas las letras
    body.append(f'<text x="{W / 2 + 4}" y="176" text-anchor="middle" font-family="DR Logo" font-size="84" '
                f'letter-spacing="3" fill="{FRAME_DIM}">{title}</text>')
    body.append(f'<text x="{W / 2}" y="172" text-anchor="middle" font-family="DR Logo" font-size="84" '
                f'letter-spacing="3" fill="{WHITE}">{title}</text>')
    body.append(f'<g class="bob">{soul(132, 110, 44)}</g>')
    body.append(f'<text x="{W / 2}" y="224" text-anchor="middle" font-family="DTM Sans" font-size="30" '
                f'letter-spacing="2" fill="{FRAME}">DESARROLLADOR DE SOFTWARE  ·  SOFTWARE DEVELOPER</text>')
    body.append(f'<text x="{W / 2}" y="268" text-anchor="middle" font-family="DTM Mono" font-size="24" fill="{YELLOW}">'
                f'★ C# · .NET · REACT · TYPESCRIPT · PYTHON ★</text>')
    body.append(f'<text x="{W - 24}" y="{H - 18}" text-anchor="end" font-family="DTM Mono" font-size="18" fill="{GRAY}">'
                f'LV 1 · COLOMBIA</text>')
    body.append(f'<text x="24" y="{H - 18}" font-family="DTM Mono" font-size="18" fill="{WHITE}">'
                f'<tspan class="blink" fill="{YELLOW}">▶</tspan> PRESS Z TO START</text>')
    write('banner.svg', svg(W, H, ''.join(body), css, 'Nicholas De la Rosa — Software Developer'))


# ---------------------------------------------------------------- Diálogo con efecto de máquina de escribir

def dialogue(name, lines, title):
    W, size, adv, lh = 1000, 28, 14, 46  # DTM Mono avanza 0.5 em por carácter
    pad_x, pad_y = 56, 74
    H = pad_y + lh * (len(lines) - 1) + 70
    cycle, per_char, gap = 14.0, 0.035, 0.35
    css = fonts_css('DTM Mono') + (
        '@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}.blink{animation:blink 1s infinite}'
        '.cover{display:none}@media (prefers-reduced-motion:no-preference){.cover{display:inline}}')
    body = [dw_box(W, H), f'<defs><clipPath id="inner"><rect x="32" y="32" width="{W - 64}" height="{H - 64}"/></clipPath></defs>'
            '<g clip-path="url(#inner)">']
    t = 0.4
    for i, line in enumerate(lines):
        y = pad_y + i * lh
        x0 = pad_x
        body.append(f'<text x="{x0}" y="{y}" font-family="DTM Mono" font-size="{size}" fill="{WHITE}" '
                    f'xml:space="preserve">{esc(line)}</text>')
        # Tapa negra que se corre letra por letra
        n = len(line)
        start, end = t / cycle * 100, (t + n * per_char) / cycle * 100
        css += (f'@keyframes ty{i}{{0%,{start:.2f}%{{transform:translateX(0);animation-timing-function:steps({n},end)}}'
                f'{end:.2f}%,100%{{transform:translateX({n * adv}px)}}}}'
                f'.ty{i}{{animation:ty{i} {cycle}s infinite}}')
        t += n * per_char + gap
        body.append(f'<rect class="cover ty{i}" x="{x0 - 2}" y="{y - size}" width="{W}" height="{size + 12}" fill="#010101"/>')
    body.append('</g>')
    body.append(f'<polygon class="blink" points="{W - 64},{H - 58} {W - 50},{H - 58} {W - 57},{H - 48}" fill="{WHITE}"/>')
    write(name, svg(W, H, ''.join(body), css, title))


# ---------------------------------------------------------------- Encabezado de sección (opción de menú elegida)

def header(name, text):
    W, H = 1000, 72
    css = fonts_css('DTM Sans') + (
        '@keyframes in{0%{transform:translateX(-36px);opacity:0}100%{transform:translateX(0);opacity:1}}'
        '.in{animation:in .3s steps(3) both}'
        '@keyframes bob{0%,100%{transform:translateX(0)}50%{transform:translateX(-5px)}}'
        '.bob{animation:bob 1.2s steps(2) infinite .3s}')
    body = (f'<g class="in"><g class="bob">{soul(6, 18, 34)}</g></g>'
            f'<text x="56" y="48" font-family="DTM Sans" font-size="44" letter-spacing="1" fill="{YELLOW}">{esc(text)}</text>'
            f'<rect x="0" y="66" width="{W}" height="4" fill="{FRAME_DIM}"/>'
            f'<rect x="0" y="66" width="120" height="4" fill="{SOUL}"/>')
    write(name, svg(W, H, body, css, text))


# ---------------------------------------------------------------- Pantalla de stats

SKILLS = [  # nivel 1-5, igual que el borrador del portafolio
    ('C#', 4, SUSIE), ('.NET', 4, SUSIE), ('Python', 3, SUSIE),
    ('HTML', 5, KRIS), ('CSS / SCSS', 4, KRIS), ('JavaScript', 4, KRIS),
    ('TypeScript', 3, KRIS), ('React', 3, KRIS), ('Angular', 2, KRIS),
    ('PostgreSQL', 3, RALSEI), ('Docker', 3, RALSEI), ('Git / GitHub', 4, TP),
]


def stats(name, t):
    W, H = 1000, 500
    css = fonts_css('DTM Sans', 'DTM Mono') + (
        '@keyframes tw{0%,100%{opacity:.3}50%{opacity:1}}.tw{animation:tw 2s steps(3) infinite}')
    b = [dw_box(W, H)]
    # Columna izquierda: el personaje
    b.append(f'<text x="56" y="88" font-family="DTM Sans" font-size="44" fill="{WHITE}">NICHOLAS</text>')
    b.append(f'<text x="290" y="88" font-family="DTM Sans" font-size="32" fill="{YELLOW}">LV 1</text>')
    b.append(f'<text x="56" y="124" font-family="DTM Mono" font-size="22" fill="{FRAME}">{esc(t["role"])}</text>')
    rows = [(t['weapon'], 'C# / .NET'), (t['armor'], 'Docker + PostgreSQL'), (t['magic'], 'React + TypeScript'),
            (t['from'], 'Colombia'), (t['langs'], t['langs_value']), (t['guild'], t['guild_value'])]
    for i, (k, v) in enumerate(rows):
        y = 180 + i * 40
        b.append(f'<text x="56" y="{y}" font-family="DTM Sans" font-size="24" fill="{GRAY}">{esc(k)}</text>')
        b.append(f'<text x="196" y="{y}" font-family="DTM Mono" font-size="22" fill="{WHITE}">{esc(v)}</text>')
    b.append(f'<g class="tw">{pixel_star(64, 438, 3, YELLOW)}</g>')
    b.append(f'<text x="84" y="447" font-family="DTM Sans" font-size="26" fill="{YELLOW}">{esc(t["status"])}</text>')
    b.append(f'<rect x="478" y="48" width="4" height="{H - 96}" fill="{FRAME_DIM}"/>')

    # Columna derecha: habilidades con barras por segmentos
    b.append(f'<text x="516" y="88" font-family="DTM Sans" font-size="32" fill="{WHITE}">{esc(t["skills"])}</text>')
    for i, (skill, lvl, color) in enumerate(SKILLS):
        y = 128 + i * 26
        b.append(f'<text x="516" y="{y + 14}" font-family="DTM Mono" font-size="18" fill="{WHITE}">{esc(skill)}</text>')
        for s in range(5):
            x = 690 + s * 46
            b.append(f'<rect x="{x}" y="{y}" width="40" height="16" fill="none" stroke="{FRAME_DIM}" stroke-width="2"/>')
            if s < lvl:
                b.append(f'<rect x="{x + 3}" y="{y + 3}" width="34" height="10" fill="{color}"/>')
    legend = [(KRIS, 'Frontend'), (SUSIE, 'Backend'), (RALSEI, t['data']), (TP, t['tools'])]
    x = 516
    for color, label in legend:
        b.append(f'<rect x="{x}" y="440" width="12" height="12" fill="{color}"/>')
        b.append(f'<text x="{x + 18}" y="451" font-family="DTM Mono" font-size="14" fill="{GRAY}">{esc(label)}</text>')
        x += 18 + len(label) * 7 + 18
    write(name, svg(W, H, ''.join(b), css, t['title']))


# ---------------------------------------------------------------- Pie: punto de guardado

def footer(name, line, sub):
    W, H = 1000, 150
    css = fonts_css('DTM Mono') + (
        '@keyframes glow{0%,100%{opacity:1}50%{opacity:.35}}.glow{animation:glow 1.4s steps(3) infinite}'
        '@keyframes spin{0%,100%{transform:scale(1)}50%{transform:scale(.7)}}'
        '.spin{transform-box:fill-box;transform-origin:center;animation:spin 1.4s steps(3) infinite}')
    # Estrella de guardado grande, pixel por pixel
    shape = ['....#....', '....#....', '...###...', '#########', '.#######.', '..#####..', '.###.###.', '.##...##.', '#.......#']
    px = 6
    star = ''.join(f'<rect x="{x * px}" y="{y * px}" width="{px}" height="{px}"/>'
                   for y, row in enumerate(shape) for x, c in enumerate(row) if c == '#')
    body = (f'<g transform="translate({W / 2 - 27},10)"><g class="spin" fill="{YELLOW}">{star}</g></g>'
            f'<text x="{W / 2}" y="104" text-anchor="middle" font-family="DTM Mono" font-size="26" fill="{WHITE}">{esc(line)}</text>'
            f'<text class="glow" x="{W / 2}" y="138" text-anchor="middle" font-family="DTM Mono" font-size="18" fill="{GRAY}">{esc(sub)}</text>')
    write(name, svg(W, H, body, css, line))


def divider():
    W, H = 1000, 60
    body = (f'<rect x="0" y="28" width="440" height="4" fill="{FRAME_DIM}"/>'
            f'<rect x="560" y="28" width="440" height="4" fill="{FRAME_DIM}"/>'
            f'{pixel_star(470, 30, 3, FRAME)}{soul(484, 14, 32)}{pixel_star(530, 30, 3, FRAME)}')
    write('divider.svg', svg(W, H, body, '', '—'))


if __name__ == '__main__':
    banner()
    divider()

    dialogue('dialogo-es.svg', [
        '* ¡Hola, viajero! Soy Nicholas.',
        '* Desarrollador de software de Colombia.',
        '* Construyo con C#/.NET, Python y React.',
        '* Nicholas está lleno de determinación.',
    ], 'Hola, soy Nicholas, desarrollador de software de Colombia')
    dialogue('dialogue-en.svg', [
        "* Howdy, traveler! I'm Nicholas.",
        '* Software developer from Colombia.',
        '* I build with C#/.NET, Python and React.',
        '* Nicholas is filled with determination.',
    ], "Howdy, I'm Nicholas, a software developer from Colombia")

    for file, text in {
        'es-sobre-mi': 'SOBRE MÍ', 'es-stats': 'ESTADÍSTICAS', 'es-habilidades': 'HABILIDADES',
        'es-proyectos': 'PROYECTOS', 'es-guardado': 'PUNTOS DE GUARDADO', 'es-github': 'MI GITHUB',
        'es-contacto': 'CONTACTO',
        'en-about': 'ABOUT ME', 'en-stats': 'STATS', 'en-skills': 'SKILLS',
        'en-projects': 'PROJECTS', 'en-save-points': 'SAVE POINTS', 'en-github': 'MY GITHUB',
        'en-contact': 'CONTACT',
    }.items():
        header(f'header-{file}.svg', text)

    stats('stats-es.svg', {
        'title': 'Estadísticas de Nicholas', 'role': 'Desarrollador de Software',
        'weapon': 'ARMA', 'armor': 'ARMADURA', 'magic': 'MAGIA', 'from': 'ORIGEN',
        'langs': 'IDIOMAS', 'langs_value': 'Español · Inglés C1+',
        'guild': 'GREMIO', 'guild_value': 'Riwi (en curso)',
        'status': 'Disponible para trabajar', 'skills': 'HABILIDADES',
        'data': 'Datos/DevOps', 'tools': 'Herramientas',
    })
    stats('stats-en.svg', {
        'title': "Nicholas' stats", 'role': 'Software Developer',
        'weapon': 'WEAPON', 'armor': 'ARMOR', 'magic': 'MAGIC', 'from': 'FROM',
        'langs': 'TONGUES', 'langs_value': 'Spanish · English C1+',
        'guild': 'GUILD', 'guild_value': 'Riwi (in progress)',
        'status': 'Open to work', 'skills': 'SKILLS',
        'data': 'Data/DevOps', 'tools': 'Tools',
    })

    footer('footer-es.svg', '* (El poder del código limpio brilla dentro de ti.)', '* Progreso guardado. ¡Gracias por pasar!')
    footer('footer-en.svg', '* (The power of clean code shines within you.)', '* Progress saved. Thanks for stopping by!')
