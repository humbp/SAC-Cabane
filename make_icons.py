#!/usr/bin/env python3
"""Dessine l'icône de l'application (une cabane rouge) et l'installe dans le projet Capacitor.

Usage, depuis la racine du projet :
  python make_icons.py android            écrit les icônes dans android/app/src/main/res
  python make_icons.py preview DOSSIER    écrit icon.png, icon-foreground.png et logo.png pour contrôle

Seule dépendance : Pillow (pip install pillow). Aucune image à fournir : tout est dessiné ici.
"""
import os
import sys

from PIL import Image, ImageDraw

SKY = (207, 227, 247)
MTN = (150, 176, 204)
SNOW = (246, 249, 252)
RED = (200, 55, 45)
ROOF = (122, 31, 25)
WOOD = (74, 36, 32)
GLOW = (255, 224, 138)
WHITE = (255, 255, 255)
GOLD = (226, 186, 84)
SKY_HEX = "#CFE3F7"


def draw_art(with_sky=True, size=1024):
    """Une cabane rouge avec volets rouge et blanc, devant des montagnes. Dessin en 1024 x 1024."""
    k = 3
    S = size * k
    f = S / 1024.0
    im = Image.new("RGBA", (S, S), SKY + (255,) if with_sky else (0, 0, 0, 0))
    d = ImageDraw.Draw(im)

    def poly(pts, fill):
        d.polygon([(x * f, y * f) for x, y in pts], fill=fill)

    def rect(x0, y0, x1, y1, fill):
        d.rectangle([x0 * f, y0 * f, x1 * f, y1 * f], fill=fill)

    # montagnes et neige
    poly([(0, 720), (250, 380), (380, 520), (560, 300), (800, 560), (900, 470), (1024, 640), (1024, 1024), (0, 1024)], MTN)
    poly([(560, 300), (512, 359), (540, 347), (562, 374), (586, 345), (588, 331)], WHITE)
    poly([(250, 380), (214, 429), (238, 416), (255, 438), (280, 412)], WHITE)
    poly([(0, 800), (200, 770), (512, 760), (800, 775), (1024, 800), (1024, 1024), (0, 1024)], SNOW)

    # cheminée (derrière le toit)
    rect(600, 360, 660, 440, (92, 40, 36))
    rect(590, 348, 670, 372, WHITE)

    # corps de la cabane et toit
    rect(292, 540, 732, 800, RED)
    poly([(240, 548), (512, 320), (784, 548)], ROOF)
    rect(292, 536, 732, 548, (150, 38, 30))

    # drapeau suisse au faîte
    rect(509, 250, 515, 322, (60, 40, 36))
    rect(515, 252, 561, 298, RED)
    rect(532, 260, 544, 290, WHITE)
    rect(521, 270, 555, 282, WHITE)

    # porte
    rect(468, 640, 556, 800, WOOD)
    d.ellipse([536 * f, 716 * f, 548 * f, 728 * f], fill=GOLD)

    # fenêtres éclairées, avec volets rouge et blanc
    for x0 in (330, 604):
        rect(x0 - 8, 602, x0 + 98, 698, WHITE)
        rect(x0, 610, x0 + 90, 690, GLOW)
        rect(x0 + 42, 610, x0 + 48, 690, WHITE)
        rect(x0, 646, x0 + 90, 652, WHITE)
    for x0 in (294, 430, 568, 704):
        rect(x0, 602, x0 + 26, 698, WHITE)
        rect(x0 + 6, 610, x0 + 20, 690, RED)

    # seuil enneigé
    rect(452, 796, 572, 810, WHITE)
    return im.resize((size, size), Image.LANCZOS)


def rounded(im, radius_ratio=0.22):
    out = im.copy()
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, im.size[0] - 1, im.size[1] - 1],
                                           radius=int(im.size[0] * radius_ratio), fill=255)
    out.putalpha(mask)
    return out


def circle(im):
    out = im.copy()
    mask = Image.new("L", im.size, 0)
    ImageDraw.Draw(mask).ellipse([0, 0, im.size[0] - 1, im.size[1] - 1], fill=255)
    out.putalpha(mask)
    return out


def write_android(root="android/app/src/main/res"):
    full = draw_art(True)
    fore = draw_art(False)
    sizes = {"mdpi": (48, 108), "hdpi": (72, 162), "xhdpi": (96, 216), "xxhdpi": (144, 324), "xxxhdpi": (192, 432)}
    for dens, (legacy, adaptive) in sizes.items():
        d = os.path.join(root, "mipmap-" + dens)
        os.makedirs(d, exist_ok=True)
        base = full.resize((legacy, legacy), Image.LANCZOS)
        rounded(base).save(os.path.join(d, "ic_launcher.png"))
        circle(base).save(os.path.join(d, "ic_launcher_round.png"))
        fore.resize((adaptive, adaptive), Image.LANCZOS).save(os.path.join(d, "ic_launcher_foreground.png"))
    xml = ('<?xml version="1.0" encoding="utf-8"?>\n'
           '<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
           '    <background android:drawable="@color/ic_launcher_background"/>\n'
           '    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>\n'
           '</adaptive-icon>\n')
    v26 = os.path.join(root, "mipmap-anydpi-v26")
    os.makedirs(v26, exist_ok=True)
    for name in ("ic_launcher.xml", "ic_launcher_round.xml"):
        open(os.path.join(v26, name), "w", encoding="utf-8").write(xml)
    values = os.path.join(root, "values")
    os.makedirs(values, exist_ok=True)
    open(os.path.join(values, "ic_launcher_background.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
        '    <color name="ic_launcher_background">%s</color>\n</resources>\n' % SKY_HEX)
    # supprime les images par défaut de Capacitor, pour qu'aucune ne passe devant la nôtre
    for old in ("drawable-v24/ic_launcher_foreground.xml", "drawable/ic_launcher_background.xml"):
        path = os.path.join(root, old)
        if os.path.exists(path):
            os.remove(path)
    print("Icônes Android écrites dans", root)


def write_preview(folder):
    os.makedirs(folder, exist_ok=True)
    draw_art(True).save(os.path.join(folder, "icon.png"))
    draw_art(False).save(os.path.join(folder, "icon-foreground.png"))
    rounded(draw_art(True, 192)).save(os.path.join(folder, "logo.png"))
    print("Aperçus écrits dans", folder)


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "android":
        write_android()
    elif len(sys.argv) >= 3 and sys.argv[1] == "preview":
        write_preview(sys.argv[2])
    else:
        print(__doc__)
        sys.exit(1)
