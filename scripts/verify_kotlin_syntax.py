#!/usr/bin/env python3
"""
Kotlin & XML Pre-Flight Linter & Syntax Balancer
Digunakan untuk memvalidasi:
1. Keseimbangan tanda kurung kurawal {}, (), [] pada seluruh file Kotlin.
2. Keabsahan struktur XML (AndroidManifest.xml, res/drawables, res/values).
3. Deteksi kesalahan penamaan parameter umum yang sering menggagalkan CI.
"""

import os
import sys
import xml.etree.ElementTree as ET

KNOWN_PARAMETER_ERRORS = [
    ("flexTimeIntervalTimeUnit", "Gunakan 'flexTimeIntervalUnit' atau argumen posisi (12L, TimeUnit.HOURS, 2L, TimeUnit.HOURS)"),
]

def check_kotlin_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as fp:
        content = fp.read()

    # 1. Cek parameter typo umum
    for bad_param, suggestion in KNOWN_PARAMETER_ERRORS:
        if bad_param in content:
            return False, f"{filepath}: Ditemukan parameter salah '{bad_param}'. Solusi: {suggestion}"

    stack = []
    lines = content.splitlines()
    in_block_comment = False

    for line_idx, line in enumerate(lines, 1):
        i = 0
        in_string = False
        str_char = ""
        while i < len(line):
            if in_block_comment:
                if line[i:i+2] == "*/":
                    in_block_comment = False
                    i += 2
                    continue
                i += 1
                continue
            if in_string:
                if line[i] == "\\" and i + 1 < len(line):
                    i += 2
                    continue
                if line[i] == str_char:
                    in_string = False
                i += 1
                continue
            if line[i:i+2] == "/*":
                in_block_comment = True
                i += 2
                continue
            if line[i:i+2] == "//":
                break
            if line[i] in ('"', "'"):
                in_string = True
                str_char = line[i]
                i += 1
                continue
            if line[i] in "{[(":
                stack.append((line[i], line_idx))
            elif line[i] in "}])":
                matching = {"}": "{", "]": "[", ")": "("}[line[i]]
                if not stack:
                    return False, f"{filepath}:{line_idx}: unexpected closing '{line[i]}'"
                open_ch, open_line = stack.pop()
                if open_ch != matching:
                    return False, f"{filepath}:{line_idx}: mismatched '{line[i]}' with '{open_ch}' at line {open_line}"
            i += 1

    if stack:
        return False, f"{filepath}: unclosed symbols {stack}"
    return True, None

def check_xml_file(filepath):
    try:
        ET.parse(filepath)
        return True, None
    except Exception as e:
        return False, f"{filepath}: invalid XML ({e})"

def main():
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    errors = []
    checked_kt = 0
    checked_xml = 0

    for root, _, files in os.walk(root_dir):
        # Abaikan direktori build dan caches
        if "/build/" in root or "/.gradle/" in root or "/.git/" in root:
            continue
        for f in files:
            path = os.path.join(root, f)
            if f.endswith(".kt"):
                checked_kt += 1
                ok, err = check_kotlin_file(path)
                if not ok:
                    errors.append(err)
            elif f.endswith(".xml") and ("res/" in path or "AndroidManifest.xml" in path):
                checked_xml += 1
                ok, err = check_xml_file(path)
                if not ok:
                    errors.append(err)

    print(f"Checked {checked_kt} Kotlin files and {checked_xml} XML files.")
    if errors:
        print("\n--- SYNTAX ERRORS FOUND ---")
        for err in errors:
            print(f"[ERROR] {err}")
        sys.exit(1)
    else:
        print("All Kotlin and XML files are syntactically balanced and valid!")
        sys.exit(0)

if __name__ == "__main__":
    main()
