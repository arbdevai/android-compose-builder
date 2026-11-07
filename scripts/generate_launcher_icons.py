#!/usr/bin/env python3
"""
Android Adaptive & Themed Vector Icon Generator (Pure Python - No External Dependencies)
Menghasilkan Adaptive Vector Icons modern dan solid:
- res/drawable/ic_launcher_background.xml (Solid netral murni tanpa aura lingkaran murahan)
- res/drawable/ic_launcher_foreground.xml (Objek fungsional multi-layer berlapis: bodi, elemen tombol, aksen)
- res/drawable/ic_launcher_monochrome.xml (Dukungan siluet monokrom Android 13+ Material You Themed Icons)
- res/mipmap-anydpi-v26/ic_launcher.xml & ic_launcher_round.xml
Bebas 'AI Slop', bebas huruf inisial malas, dan bebas efek gradien lingkaran kebiruan.
"""

import os
import sys
import re
import argparse
import zlib
import struct

DENSITIES = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

# -----------------------------------------------------------------------------
# Template Objek Fungsional Nyata Multi-Layer (Viewport 108x108, Safe Zone 72dp)
# Setiap preset memiliki 3 lapisan:
#   1. body: Rangka / housing objek (biasanya warna gelap kontras)
#   2. elements: Elemen fungsional (tuts, window bar, isi konten)
#   3. accent: Elemen sorotan (spacebar, prompt cursor, titik aktif)
# -----------------------------------------------------------------------------
OBJECT_PRESETS = {
    "keyboard": {
        "description": "Papan ketik mekanikal solid multi-row dengan spacebar aksen",
        "body_path": "M29,31 L79,31 A7,7 0 0,1 86,38 L86,67 A7,7 0 0,1 79,74 L29,74 A7,7 0 0,1 22,67 L22,38 A7,7 0 0,1 29,31 Z",
        "elements_path": """
            M28.5,36 L35.5,36 A1.8,1.8 0 0,1 37.3,37.8 L37.3,42.2 A1.8,1.8 0 0,1 35.5,44 L28.5,44 A1.8,1.8 0 0,1 26.7,42.2 L26.7,37.8 A1.8,1.8 0 0,1 28.5,36 Z
            M41.3,36 L48.3,36 A1.8,1.8 0 0,1 50.1,37.8 L50.1,42.2 A1.8,1.8 0 0,1 48.3,44 L41.3,44 A1.8,1.8 0 0,1 39.5,42.2 L39.5,37.8 A1.8,1.8 0 0,1 41.3,36 Z
            M54.1,36 L61.1,36 A1.8,1.8 0 0,1 62.9,37.8 L62.9,42.2 A1.8,1.8 0 0,1 61.1,44 L54.1,44 A1.8,1.8 0 0,1 52.3,42.2 L52.3,37.8 A1.8,1.8 0 0,1 54.1,36 Z
            M66.9,36 L73.9,36 A1.8,1.8 0 0,1 75.7,37.8 L75.7,42.2 A1.8,1.8 0 0,1 73.9,44 L66.9,44 A1.8,1.8 0 0,1 65.1,42.2 L65.1,37.8 A1.8,1.8 0 0,1 66.9,36 Z
            M31.5,47 L38.5,47 A1.8,1.8 0 0,1 40.3,48.8 L40.3,53.2 A1.8,1.8 0 0,1 38.5,55 L31.5,55 A1.8,1.8 0 0,1 29.7,53.2 L29.7,48.8 A1.8,1.8 0 0,1 31.5,47 Z
            M44.3,47 L51.3,47 A1.8,1.8 0 0,1 53.1,48.8 L53.1,53.2 A1.8,1.8 0 0,1 51.3,55 L44.3,55 A1.8,1.8 0 0,1 42.5,53.2 L42.5,48.8 A1.8,1.8 0 0,1 44.3,47 Z
            M57.1,47 L64.1,47 A1.8,1.8 0 0,1 65.9,48.8 L65.9,53.2 A1.8,1.8 0 0,1 64.1,55 L57.1,55 A1.8,1.8 0 0,1 55.3,53.2 L55.3,48.8 A1.8,1.8 0 0,1 57.1,47 Z
            M69.9,47 L76.9,47 A1.8,1.8 0 0,1 78.7,48.8 L78.7,53.2 A1.8,1.8 0 0,1 76.9,55 L69.9,55 A1.8,1.8 0 0,1 68.1,53.2 L68.1,48.8 A1.8,1.8 0 0,1 69.9,47 Z
            M28.5,58 L35.5,58 A1.8,1.8 0 0,1 37.3,59.8 L37.3,65.2 A1.8,1.8 0 0,1 35.5,67 L28.5,67 A1.8,1.8 0 0,1 26.7,65.2 L26.7,59.8 A1.8,1.8 0 0,1 28.5,58 Z
        """,
        "accent_path": """
            M41.5,58 L66.5,58 A2,2 0 0,1 68.5,60 L68.5,65 A2,2 0 0,1 66.5,67 L41.5,67 A2,2 0 0,1 39.5,65 L39.5,60 A2,2 0 0,1 41.5,58 Z
            M72.5,58 L79.5,58 A1.8,1.8 0 0,1 81.3,59.8 L81.3,65.2 A1.8,1.8 0 0,1 79.5,67 L72.5,67 A1.8,1.8 0 0,1 70.7,65.2 L70.7,59.8 A1.8,1.8 0 0,1 72.5,58 Z
        """,
        "monochrome_path": """
            M29,31 L79,31 A7,7 0 0,1 86,38 L86,67 A7,7 0 0,1 79,74 L29,74 A7,7 0 0,1 22,67 L22,38 A7,7 0 0,1 29,31 Z
            M28.5,36 L35.5,36 A1.8,1.8 0 0,1 37.3,37.8 L37.3,42.2 A1.8,1.8 0 0,1 35.5,44 L28.5,44 A1.8,1.8 0 0,1 26.7,42.2 L26.7,37.8 A1.8,1.8 0 0,1 28.5,36 Z
            M41.3,36 L48.3,36 A1.8,1.8 0 0,1 50.1,37.8 L50.1,42.2 A1.8,1.8 0 0,1 48.3,44 L41.3,44 A1.8,1.8 0 0,1 39.5,42.2 L39.5,37.8 A1.8,1.8 0 0,1 41.3,36 Z
            M54.1,36 L61.1,36 A1.8,1.8 0 0,1 62.9,37.8 L62.9,42.2 A1.8,1.8 0 0,1 61.1,44 L54.1,44 A1.8,1.8 0 0,1 52.3,42.2 L52.3,37.8 A1.8,1.8 0 0,1 54.1,36 Z
            M66.9,36 L73.9,36 A1.8,1.8 0 0,1 75.7,37.8 L75.7,42.2 A1.8,1.8 0 0,1 73.9,44 L66.9,44 A1.8,1.8 0 0,1 65.1,42.2 L65.1,37.8 A1.8,1.8 0 0,1 66.9,36 Z
            M41.5,58 L66.5,58 A2,2 0 0,1 68.5,60 L68.5,65 A2,2 0 0,1 66.5,67 L41.5,67 A2,2 0 0,1 39.5,65 L39.5,60 A2,2 0 0,1 41.5,58 Z
        """
    },
    "terminal": {
        "description": "Jendela terminal Linux / Developer shell dengan prompt dan blok kursor",
        "body_path": "M24,28 L84,28 A6,6 0 0,1 90,34 L90,76 A6,6 0 0,1 84,82 L24,82 A6,6 0 0,1 18,76 L18,34 A6,6 0 0,1 24,28 Z",
        "elements_path": """
            M26,34 A2.5,2.5 0 1,0 26,39 A2.5,2.5 0 1,0 26,34 Z
            M33,34 A2.5,2.5 0 1,0 33,39 A2.5,2.5 0 1,0 33,34 Z
            M40,34 A2.5,2.5 0 1,0 40,39 A2.5,2.5 0 1,0 40,34 Z
            M18,43 L90,43
            M30,52 L42,61 L30,70
        """,
        "accent_path": "M48,67 L66,67 A2,2 0 0,1 68,69 L68,71 A2,2 0 0,1 66,73 L48,73 A2,2 0 0,1 46,71 L46,69 A2,2 0 0,1 48,67 Z",
        "monochrome_path": """
            M24,28 L84,28 A6,6 0 0,1 90,34 L90,76 A6,6 0 0,1 84,82 L24,82 A6,6 0 0,1 18,76 L18,34 A6,6 0 0,1 24,28 Z
            M30,52 L42,61 L30,70
            M48,67 L66,67
        """
    },
    "code": {
        "description": "Editor kode dengan kurung siku sudut tebal dan garis slash",
        "body_path": "M26,26 L82,26 A8,8 0 0,1 90,34 L90,74 A8,8 0 0,1 82,82 L26,82 A8,8 0 0,1 18,74 L18,34 A8,8 0 0,1 26,26 Z",
        "elements_path": """
            M38,40 L26,54 L38,68
            M70,40 L82,54 L70,68
        """,
        "accent_path": "M60,35 L48,73",
        "monochrome_path": """
            M26,26 L82,26 A8,8 0 0,1 90,34 L90,74 A8,8 0 0,1 82,82 L26,82 A8,8 0 0,1 18,74 L18,34 A8,8 0 0,1 26,26 Z
            M38,40 L26,54 L38,68
            M70,40 L82,54 L70,68
            M60,35 L48,73
        """
    },
    "tool": {
        "description": "Perkakas teknikal / gear presisi dengan sumbu tengah solid",
        "body_path": "M54,26 A28,28 0 1,0 54,82 A28,28 0 1,0 54,26 Z",
        "elements_path": """
            M51,20 h6 v8 h-6 z M51,80 h6 v8 h-6 z
            M20,51 h8 v6 h-8 z M80,51 h8 v6 h-8 z
            M30,30 l6,6 l-4,4 l-6,-6 z M74,74 l6,6 l-4,4 l-6,-6 z
            M74,34 l6,-6 l4,4 l-6,6 z M30,78 l6,-6 l4,4 l-6,6 z
        """,
        "accent_path": "M54,42 A12,12 0 1,1 54,66 A12,12 0 1,1 54,42 Z",
        "monochrome_path": "M54,26 A28,28 0 1,0 54,82 A28,28 0 1,0 54,26 Z M54,44 A10,10 0 1,1 54,64 A10,10 0 1,1 54,44 Z"
    },
    "chat": {
        "description": "Geometri gelembung pesan solid dengan titik komunikasi",
        "body_path": "M30,28 h48 a10,10 0 0,1 10,10 v22 a10,10 0 0,1 -10,10 h-28 l-16,11 v-11 h-4 a10,10 0 0,1 -10,-10 v-22 a10,10 0 0,1 10,-10 z",
        "elements_path": "M40,49 a4,4 0 1,1 0,-0.01 z M54,49 a4,4 0 1,1 0,-0.01 z",
        "accent_path": "M68,49 a4,4 0 1,1 0,-0.01 z",
        "monochrome_path": "M30,28 h48 a10,10 0 0,1 10,10 v22 a10,10 0 0,1 -10,10 h-28 l-16,11 v-11 h-4 a10,10 0 0,1 -10,-10 v-22 a10,10 0 0,1 10,-10 z"
    }
}

def clean_svg_path(path_str):
    """Membersihkan whitespace pada string path SVG."""
    return " ".join(path_str.strip().split())

def detect_best_preset(app_name):
    """Mendeteksi otomatis preset objek nyata terbaik berdasarkan nama aplikasi."""
    lower = app_name.lower()
    if any(k in lower for k in ["board", "key", "ketik", "ime"]):
        return "keyboard"
    if any(k in lower for k in ["term", "box", "pty", "sh", "shell", "console"]):
        return "terminal"
    if any(k in lower for k in ["code", "ide", "edit", "script", "dev"]):
        return "code"
    if any(k in lower for k in ["chat", "talk", "msg", "pesan"]):
        return "chat"
    if any(k in lower for k in ["tool", "opt", "fix", "repair", "clean"]):
        return "tool"
    return "keyboard"

def hex_to_rgb(hex_str, default=(18, 18, 18)):
    clean = hex_str.strip().lstrip("#")
    if len(clean) == 6:
        try:
            return tuple(int(clean[i:i+2], 16) for i in (0, 2, 4))
        except ValueError:
            pass
    return default

def create_png_square(width, height, fill_rgb):
    """Membuat PNG solid sederhana untuk fallback legacy mipmap."""
    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0)
        for x in range(width):
            raw_data.extend([fill_rgb[0], fill_rgb[1], fill_rgb[2], 255])
    compressed = zlib.compress(bytes(raw_data), level=9)

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xffffffff)

    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)) + chunk(b"IDAT", compressed) + chunk(b"IEND", b"")

def generate_icons(
    res_dir,
    app_name="App",
    preset_type="auto",
    bg_hex="#000000",
    body_hex="#1E1E1E",
    elements_hex="#ECEFF4",
    accent_hex="#38BDF8",
    generate_png=False
):
    """Menghasilkan seluruh icon XML dan dukungan Themed Icons solid di folder res/."""
    drawable_dir = os.path.join(res_dir, "drawable")
    anydpi_dir = os.path.join(res_dir, "mipmap-anydpi-v26")
    os.makedirs(drawable_dir, exist_ok=True)
    os.makedirs(anydpi_dir, exist_ok=True)

    # 1. Pilih Preset Objek Nyata (Anti-Huruf Malas)
    if preset_type == "auto" or preset_type not in OBJECT_PRESETS:
        preset_type = detect_best_preset(app_name)
    preset = OBJECT_PRESETS[preset_type]
    print(f"Menghasilkan icon dengan objek nyata: [{preset_type}] ({preset['description']})")

    body_d = clean_svg_path(preset["body_path"])
    elements_d = clean_svg_path(preset["elements_path"])
    accent_d = clean_svg_path(preset["accent_path"])
    mono_d = clean_svg_path(preset["monochrome_path"])

    # 2. Generate ic_launcher_background.xml (Solid Murni Bebas AI Aura)
    bg_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <!-- Pure Solid Neutral Background (Zero AI Glow / Zero Tint Slop) -->
    <path
        android:fillColor="{bg_hex}"
        android:pathData="M0,0h108v108h-108z" />
</vector>
"""
    with open(os.path.join(drawable_dir, "ic_launcher_background.xml"), "w", encoding="utf-8") as fp:
        fp.write(bg_xml)

    # 3. Generate ic_launcher_foreground.xml (Multi-Layer Solid Geometry)
    fg_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">

    <!-- Layer 1: Solid Main Housing / Body -->
    <path
        android:fillColor="{body_hex}"
        android:strokeColor="{body_hex}"
        android:strokeWidth="1.2"
        android:pathData="{body_d}" />

    <!-- Layer 2: Functional Elements / Keycaps / Visual Lines -->
    <path
        android:fillColor="{elements_hex}"
        android:strokeColor="{elements_hex}"
        android:strokeWidth="1.0"
        android:strokeLineCap="round"
        android:strokeLineJoin="round"
        android:pathData="{elements_d}" />

    <!-- Layer 3: Solid Accent Anchor -->
    <path
        android:fillColor="{accent_hex}"
        android:strokeColor="{accent_hex}"
        android:strokeWidth="1.0"
        android:strokeLineCap="round"
        android:strokeLineJoin="round"
        android:pathData="{accent_d}" />
</vector>
"""
    with open(os.path.join(drawable_dir, "ic_launcher_foreground.xml"), "w", encoding="utf-8") as fp:
        fp.write(fg_xml)

    # 4. Generate ic_launcher_monochrome.xml (Android 13+ Material You Themed Icons)
    mono_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <!-- Pure White Silhouette for System Dynamic Color Engine -->
    <path
        android:fillColor="#FFFFFFFF"
        android:strokeColor="#FFFFFFFF"
        android:strokeWidth="1.5"
        android:strokeLineCap="round"
        android:strokeLineJoin="round"
        android:pathData="{mono_d}" />
</vector>
"""
    with open(os.path.join(drawable_dir, "ic_launcher_monochrome.xml"), "w", encoding="utf-8") as fp:
        fp.write(mono_xml)

    # 5. Tulis Adaptive Icon XML di mipmap-anydpi-v26
    adaptive_xml = """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background" />
    <foreground android:drawable="@drawable/ic_launcher_foreground" />
    <monochrome android:drawable="@drawable/ic_launcher_monochrome" />
</adaptive-icon>
"""
    with open(os.path.join(anydpi_dir, "ic_launcher.xml"), "w", encoding="utf-8") as fp:
        fp.write(adaptive_xml)
    with open(os.path.join(anydpi_dir, "ic_launcher_round.xml"), "w", encoding="utf-8") as fp:
        fp.write(adaptive_xml)

    # 6. Generate legacy PNGs jika diminta
    if generate_png:
        p_rgb = hex_to_rgb(bg_hex)
        for folder_name, size in DENSITIES.items():
            folder_path = os.path.join(res_dir, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            png_bytes = create_png_square(size, size, p_rgb)
            with open(os.path.join(folder_path, "ic_launcher.png"), "wb") as fp:
                fp.write(png_bytes)
            with open(os.path.join(folder_path, "ic_launcher_round.png"), "wb") as fp:
                fp.write(png_bytes)

    print(f"Selesai! Adaptive Vector Icons solid berhasil di-generate di: {res_dir}")

def main():
    parser = argparse.ArgumentParser(description="Solid Android Adaptive & Themed Vector Icon Generator (Anti-Letter / Anti-Slop)")
    parser.add_argument("res_dir", nargs="?", default="app/src/main/res", help="Path ke direktori res aplikasi")
    parser.add_argument("--app-name", default="Sboard", help="Nama aplikasi (digunakan untuk auto-deteksi objek)")
    parser.add_argument("--type", choices=["auto", "keyboard", "terminal", "code", "tool", "chat"], default="auto", help="Preset objek visual nyata (default: auto)")
    parser.add_argument("--bg", default="#000000", help="Warna solid background (default: #000000 True Black)")
    parser.add_argument("--body", default="#1E1E1E", help="Warna bodi objek (default: #1E1E1E Dark Neutral)")
    parser.add_argument("--elements", default="#ECEFF4", help="Warna elemen tuts/konten (default: #ECEFF4 White)")
    parser.add_argument("--accent", default="#38BDF8", help="Warna aksen tombol (default: #38BDF8)")
    parser.add_argument("--png", action="store_true", help="Generate legacy mipmap PNGs fallback")
    args = parser.parse_args()

    if not os.path.exists(args.res_dir):
        print(f"Folder res tidak ditemukan: {args.res_dir}")
        sys.exit(1)

    generate_icons(
        res_dir=args.res_dir,
        app_name=args.app_name,
        preset_type=args.type,
        bg_hex=args.bg,
        body_hex=args.body,
        elements_hex=args.elements,
        accent_hex=args.accent,
        generate_png=args.png
    )

if __name__ == "__main__":
    main()
