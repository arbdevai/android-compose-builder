#!/usr/bin/env python3
"""
Android Launcher Icon Generator (Pure Python - No External Dependencies)
Menghasilkan Adaptive Vector Icons (ic_launcher_background.xml, ic_launcher_foreground.xml)
serta file raster PNG presisi ke seluruh folder mipmap (mdpi sampai xxxhdpi).
Bebas 'AI Slop' - desain bersih, geometris, konsisten dengan tema aplikasi.
"""

import os
import sys
import zlib
import struct
import math
import argparse

DENSITIES = {
    "mipmap-mdpi": 48,
    "mipmap-hdpi": 72,
    "mipmap-xhdpi": 96,
    "mipmap-xxhdpi": 144,
    "mipmap-xxxhdpi": 192,
}

def hex_to_rgb(hex_str, default=(203, 24, 27)):
    clean = hex_str.strip().lstrip("#")
    if len(clean) == 6:
        try:
            return tuple(int(clean[i:i+2], 16) for i in (0, 2, 4))
        except ValueError:
            pass
    return default

def create_png(width, height, draw_func):
    """Membuat file PNG mentah menggunakan modul zlib bawaan Python."""
    raw_data = bytearray()
    for y in range(height):
        raw_data.append(0)  # Filter byte: None
        for x in range(width):
            r, g, b, a = draw_func(x, y, width, height)
            raw_data.extend([r, g, b, a])

    compressed = zlib.compress(bytes(raw_data), level=9)

    def chunk(tag, data):
        length = len(data)
        crc = zlib.crc32(tag + data) & 0xffffffff
        return struct.pack(">I", length) + tag + data + struct.pack(">I", crc)

    png_header = b"\x89PNG\r\n\x1a\n"
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    ihdr = chunk(b"IHDR", ihdr_data)
    idat = chunk(b"IDAT", compressed)
    iend = chunk(b"IEND", b"")

    return png_header + ihdr + idat + iend

def default_app_icon_painter(
    primary_rgb=(163, 17, 20),
    secondary_rgb=(203, 24, 27),
    accent_rgb=(255, 255, 255),
    arc_rgb=(255, 218, 214),
    is_round=False
):
    """Fungsi render icon modern: Squircle/Circle + WiFi arcs + Fast Lightning."""
    def painter(x, y, w, h):
        cx, cy = w / 2.0, h / 2.0
        r_max = w / 2.0
        dx = x - cx
        dy = y - cy
        dist = math.sqrt(dx * dx + dy * dy)

        # Radius sudut untuk squircle atau round
        corner_radius = r_max if is_round else r_max * 0.44

        # Masking bentuk dasar icon
        inside_mask = False
        if is_round:
            inside_mask = dist <= (r_max - 1.0)
        else:
            qx = max(0.0, abs(dx) - (cx - corner_radius))
            qy = max(0.0, abs(dy) - (cy - corner_radius))
            corner_dist = math.sqrt(qx * qx + qy * qy)
            inside_mask = corner_dist <= corner_radius - 0.5

        if not inside_mask:
            return 0, 0, 0, 0

        # Gradient latar belakang halus (Crimson Dark ke Crimson Vibrant)
        norm_y = y / float(h)
        bg_r = int(primary_rgb[0] * (1.0 - norm_y * 0.3) + secondary_rgb[0] * (norm_y * 0.3))
        bg_g = int(primary_rgb[1] * (1.0 - norm_y * 0.3) + secondary_rgb[1] * (norm_y * 0.3))
        bg_b = int(primary_rgb[2] * (1.0 - norm_y * 0.3) + secondary_rgb[2] * (norm_y * 0.3))

        # Efek concentric depth circle halus
        if dist < r_max * 0.72:
            depth_factor = 1.08
            bg_r = min(255, int(bg_r * depth_factor))
            bg_g = min(255, int(bg_g * depth_factor))
            bg_b = min(255, int(bg_b * depth_factor))

        # Gambar simbol Wifi Arcs & Lightning
        wifi_center_y = cy + h * 0.12
        w_dy = y - wifi_center_y
        w_dist = math.sqrt(dx * dx + w_dy * w_dy)
        angle = math.atan2(w_dy, dx)

        # Arc 1 (Atas - Pure White)
        if -2.5 < angle < -0.64 and abs(w_dist - w * 0.34) <= (w * 0.038):
            return 255, 255, 255, 255
        # Arc 2 (Tengah - Soft Rose/White Glow)
        if -2.5 < angle < -0.64 and abs(w_dist - w * 0.22) <= (w * 0.034):
            return arc_rgb[0], arc_rgb[1], arc_rgb[2], 255

        # Simbol Kilat / Fiber Pulse di tengah/kanan
        lx = (x - cx) / float(w)
        ly = (y - cy) / float(h)
        # Segitiga atas kilat
        if -0.06 <= lx <= 0.22 and -0.28 <= ly <= 0.02:
            if lx >= (ly * 0.6 + 0.02) and lx <= (ly * 0.6 + 0.22):
                return accent_rgb[0], accent_rgb[1], accent_rgb[2], 255
        # Segitiga bawah kilat
        if -0.16 <= lx <= 0.12 and -0.02 <= ly <= 0.28:
            if lx >= (ly * 0.6 - 0.12) and lx <= (ly * 0.6 + 0.08):
                return accent_rgb[0], accent_rgb[1], accent_rgb[2], 255

        return bg_r, bg_g, bg_b, 255

    return painter

def generate_icons(
    res_dir,
    primary_hex="#A31114",
    secondary_hex="#CB181B",
    accent_hex="#FFFFFF",
    arc_hex="#FFDAD6"
):
    """Menghasilkan seluruh icon XML dan raster PNG di folder res/ aplikasi."""
    drawable_dir = os.path.join(res_dir, "drawable")
    anydpi_dir = os.path.join(res_dir, "mipmap-anydpi-v26")
    os.makedirs(drawable_dir, exist_ok=True)
    os.makedirs(anydpi_dir, exist_ok=True)

    primary_rgb = hex_to_rgb(primary_hex, default=(163, 17, 20))
    secondary_rgb = hex_to_rgb(secondary_hex, default=(203, 24, 27))
    accent_rgb = hex_to_rgb(accent_hex, default=(255, 255, 255))
    arc_rgb = hex_to_rgb(arc_hex, default=(255, 218, 214))

    # 1. Tulis ic_launcher_background.xml
    bg_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="{primary_hex}"
        android:pathData="M0,0h108v108h-108z" />
    <path
        android:fillColor="{secondary_hex}"
        android:pathData="M54,18 A36,36 0 1 0 54,90 A36,36 0 1 0 54,18 Z"
        android:strokeAlpha="0.25"
        android:fillAlpha="0.35" />
</vector>
"""
    with open(os.path.join(drawable_dir, "ic_launcher_background.xml"), "w") as fp:
        fp.write(bg_xml)

    # 2. Tulis ic_launcher_foreground.xml
    fg_xml = f"""<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <group
        android:scaleX="0.8"
        android:scaleY="0.8"
        android:translateX="10.8"
        android:translateY="10.8">
        <!-- WiFi Arc 1 (Crisp White) -->
        <path
            android:fillColor="#00000000"
            android:strokeColor="#FFFFFF"
            android:strokeWidth="5.5"
            android:strokeLineCap="round"
            android:pathData="M 32,46 A 26,26 0 0 1 76,46" />
        <!-- WiFi Arc 2 (Themed Accent Glow) -->
        <path
            android:fillColor="#00000000"
            android:strokeColor="{arc_hex}"
            android:strokeWidth="5"
            android:strokeLineCap="round"
            android:pathData="M 40,55 A 16,16 0 0 1 68,55" />
        <!-- Fiber Optic Pulse / Fast Lightning -->
        <path
            android:fillColor="{accent_hex}"
            android:pathData="M 57,48 L 47,63 L 53,63 L 49,76 L 62,59 L 56,59 Z" />
    </group>
</vector>
"""
    with open(os.path.join(drawable_dir, "ic_launcher_foreground.xml"), "w") as fp:
        fp.write(fg_xml)

    # 3. Tulis anydpi adaptive icons
    adaptive_xml = """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background" />
    <foreground android:drawable="@drawable/ic_launcher_foreground" />
</adaptive-icon>
"""
    with open(os.path.join(anydpi_dir, "ic_launcher.xml"), "w") as fp:
        fp.write(adaptive_xml)
    with open(os.path.join(anydpi_dir, "ic_launcher_round.xml"), "w") as fp:
        fp.write(adaptive_xml)

    # 4. Generate raster PNGs untuk setiap folder mipmap
    painter_sq = default_app_icon_painter(
        primary_rgb=primary_rgb,
        secondary_rgb=secondary_rgb,
        accent_rgb=accent_rgb,
        arc_rgb=arc_rgb,
        is_round=False
    )
    painter_rd = default_app_icon_painter(
        primary_rgb=primary_rgb,
        secondary_rgb=secondary_rgb,
        accent_rgb=accent_rgb,
        arc_rgb=arc_rgb,
        is_round=True
    )

    for folder_name, size in DENSITIES.items():
        folder_path = os.path.join(res_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        png_sq = create_png(size, size, painter_sq)
        with open(os.path.join(folder_path, "ic_launcher.png"), "wb") as fp:
            fp.write(png_sq)

        png_rd = create_png(size, size, painter_rd)
        with open(os.path.join(folder_path, "ic_launcher_round.png"), "wb") as fp:
            fp.write(png_rd)

    print(f"Berhasil menghasilkan launcher icons tema ({primary_hex}/{secondary_hex}) di: {res_dir}")

def main():
    parser = argparse.ArgumentParser(description="Android Adaptive & Raster Icon Generator")
    parser.add_argument("res_dir", nargs="?", default="app/src/main/res", help="Path to res directory")
    parser.add_argument("--primary", default="#A31114", help="Primary brand color hex (e.g. #A31114)")
    parser.add_argument("--secondary", default="#CB181B", help="Secondary brand color hex (e.g. #CB181B)")
    parser.add_argument("--accent", default="#FFFFFF", help="Accent icon symbol color hex (e.g. #FFFFFF)")
    parser.add_argument("--arc", default="#FFDAD6", help="Inner arc color hex (e.g. #FFDAD6)")
    args = parser.parse_args()

    if not os.path.exists(args.res_dir):
        print(f"Folder res tidak ditemukan: {args.res_dir}")
        sys.exit(1)

    generate_icons(
        res_dir=args.res_dir,
        primary_hex=args.primary,
        secondary_hex=args.secondary,
        accent_hex=args.accent,
        arc_hex=args.arc
    )

if __name__ == "__main__":
    main()
