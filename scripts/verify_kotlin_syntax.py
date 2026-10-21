#!/usr/bin/env python3
"""
Kotlin & XML Pre-Flight Linter & Syntax Balancer (Upgraded for Zero-CI-Failure)
Validasi menyeluruh sebelum commit/push:
1. Keseimbangan tanda kurung {}, (), [] dengan pemahaman penuh string literal (termasuk triple quotes \"\"\"...\"\"\"),
   char literal, komentar baris //, dan komentar blok /* ... */.
2. Validasi struktur XML (AndroidManifest.xml, res/drawables, res/values).
3. Deteksi typo parameter Compose/WorkManager umum yang sering menggagalkan CI.
4. Deteksi akses properti ilegal langsung pada tipe `kotlin.Result` tanpa `.getOrNull()` / `.getOrThrow()`.
5. Deteksi pemanggilan ekstensi Modifier Compose umum tanpa import yang sesuai (border, clip, clickable, dsb).
6. Deteksi pemanggilan suspend function di dalam non-coroutine lambda umum.
"""

import os
import sys
import re
import xml.etree.ElementTree as ET

KNOWN_PARAMETER_ERRORS = [
    ("flexTimeIntervalTimeUnit", "Gunakan 'flexTimeIntervalUnit' atau argumen posisi (12L, TimeUnit.HOURS, 2L, TimeUnit.HOURS)"),
]

SUSPEND_FUNCTIONS = [
    "scrollTo(",
    "animateScrollTo(",
    "showSnackbar(",
]

# Anggota legal dari kotlin.Result<T>
KOTLIN_RESULT_MEMBERS = {
    "isSuccess", "isFailure", "getOrNull", "getOrThrow", "getOrDefault",
    "getOrElse", "fold", "map", "mapCatching", "recover", "recoverCatching",
    "onSuccess", "onFailure", "exceptionOrNull", "toString", "hashCode", "equals"
}

# Ekstensi Compose Modifier yang memerlukan import spesifik
COMPOSE_MODIFIER_EXTENSIONS = [
    (re.compile(r'\.border\s*\('), "androidx.compose.foundation.border", "Modifier.border"),
    (re.compile(r'\.clip\s*\('), "androidx.compose.ui.draw.clip", "Modifier.clip"),
    (re.compile(r'\.clickable\s*(?:<[^>]+>)?\s*\('), "androidx.compose.foundation.clickable", "Modifier.clickable"),
    (re.compile(r'\.background\s*\('), "androidx.compose.foundation.background", "Modifier.background"),
    (re.compile(r'\.heightIn\s*\('), "androidx.compose.foundation.layout.heightIn", "Modifier.heightIn"),
    (re.compile(r'\.widthIn\s*\('), "androidx.compose.foundation.layout.widthIn", "Modifier.widthIn"),
    (re.compile(r'\.sizeIn\s*\('), "androidx.compose.foundation.layout.sizeIn", "Modifier.sizeIn"),
    (re.compile(r'\.imePadding\s*\('), "androidx.compose.foundation.layout.imePadding", "Modifier.imePadding"),
    (re.compile(r'\.systemBarsPadding\s*\('), "androidx.compose.foundation.layout.systemBarsPadding", "Modifier.systemBarsPadding"),
]

def check_kotlin_brackets(filepath, content):
    """
    Tokenizer yang memahami penuh sintaks Kotlin:
    - Triple-quoted multiline strings (\"\"\" ... \"\"\")
    - Double-quoted single-line strings (\" ... \") dengan escape sequence
    - Single-quoted char literals (' ... ') dengan escape sequence
    - Line comments (// ...)
    - Block comments (/* ... */)
    - Keseimbangan kurung {}, (), []
    """
    stack = []
    i = 0
    n = len(content)
    line_no = 1

    while i < n:
        # Newlines
        if content[i] == '\n':
            line_no += 1
            i += 1
            continue

        # Block comments /* ... */
        if content[i:i+2] == '/*':
            i += 2
            while i < n and content[i:i+2] != '*/':
                if content[i] == '\n':
                    line_no += 1
                i += 1
            i += 2
            continue

        # Line comments // ...
        if content[i:i+2] == '//':
            i += 2
            while i < n and content[i] != '\n':
                i += 1
            continue

        # Triple-quoted strings """ ... """
        if content[i:i+3] == '"""':
            i += 3
            while i < n and content[i:i+3] != '"""':
                if content[i] == '\n':
                    line_no += 1
                i += 1
            i += 3
            continue

        # Normal strings " ... "
        if content[i] == '"':
            i += 1
            while i < n and content[i] != '"':
                if content[i] == '\\':
                    i += 2
                    continue
                if content[i] == '\n':
                    line_no += 1
                i += 1
            i += 1
            continue

        # Char literal ' ... '
        if content[i] == "'":
            i += 1
            while i < n and content[i] != "'":
                if content[i] == '\\':
                    i += 2
                    continue
                if content[i] == '\n':
                    line_no += 1
                i += 1
            i += 1
            continue

        # Symbols
        ch = content[i]
        if ch in '{[(':
            stack.append((ch, line_no))
        elif ch in '}])':
            matching = {'}': '{', ']': '[', ')': '('}[ch]
            if not stack:
                return False, f"{filepath}:{line_no}: Karakter penutup '{ch}' tidak memiliki pasangan pembuka."
            open_ch, open_line = stack.pop()
            if open_ch != matching:
                return False, f"{filepath}:{line_no}: Penutup '{ch}' tidak cocok dengan pembuka '{open_ch}' pada baris {open_line}."
        i += 1

    if stack:
        unclosed_desc = ", ".join([f"'{ch}' (baris {l})" for ch, l in stack[-5:]])
        return False, f"{filepath}: Ditemukan simbol pembuka yang belum ditutup: {unclosed_desc}"
    return True, None

def check_kotlin_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as fp:
        content = fp.read()

    # 1. Cek parameter typo umum
    for bad_param, suggestion in KNOWN_PARAMETER_ERRORS:
        if bad_param in content:
            return False, f"{filepath}: Ditemukan parameter salah '{bad_param}'. Solusi: {suggestion}"

    # 2. Cek pemanggilan fungsi suspend di dalam non-coroutine lambda umum
    for line_idx, line in enumerate(content.splitlines(), 1):
        stripped = line.strip()
        if not stripped.startswith("//") and not stripped.startswith("*"):
            for sf in SUSPEND_FUNCTIONS:
                if sf in line and ("onValueChange" in line or "onKeyEvent" in line):
                    return False, f"{filepath}:{line_idx}: Pemanggilan fungsi suspend '{sf}' langsung di dalam non-coroutine lambda. Bungkus dengan 'coroutineScope.launch {{ ... }}'."

    # 3. Deteksi akses properti langsung pada variabel kotlin.Result<T> secara scope-aware
    lines = content.splitlines()
    scope_stack = [{}]
    res_assign_re = re.compile(r'\bval\s+([a-zA-Z0-9_]+)\s*(?::\s*Result<[^>]+>)?\s*=\s*(?:[a-zA-Z0-9_.]*(?:execute|executeSync|runCatching)\b|Result\.(?:success|failure))')
    other_val_re = re.compile(r'\bval\s+([a-zA-Z0-9_]+)\s*[:=]')

    for line_idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('*'):
            continue
        for char in line:
            if char == '{':
                scope_stack.append({})
            elif char == '}' and len(scope_stack) > 1:
                scope_stack.pop()
        m_res = res_assign_re.search(line)
        if m_res:
            scope_stack[-1][m_res.group(1)] = True
        else:
            m_other = other_val_re.search(line)
            if m_other:
                scope_stack[-1][m_other.group(1)] = False

        active_result_vars = set()
        for scope in scope_stack:
            for v, is_res in scope.items():
                if is_res:
                    active_result_vars.add(v)
                elif v in active_result_vars:
                    active_result_vars.remove(v)

        for v in active_result_vars:
            for m in re.finditer(r'\b' + re.escape(v) + r'\.([a-zA-Z0-9_]+)', line):
                prop = m.group(1)
                if prop not in KOTLIN_RESULT_MEMBERS:
                    return False, f"{filepath}:{line_idx}: Variabel '{v}' bertipe Result<T>. Properti '{prop}' tidak dapat diakses langsung tanpa '.getOrNull()?.{prop}' atau '.getOrThrow().{prop}'."

    # 4. Deteksi Modifier extension functions tanpa import yang sesuai
    for ext_regex, req_import, desc in COMPOSE_MODIFIER_EXTENSIONS:
        if ext_regex.search(content):
            pkg_prefix = req_import.rsplit('.', 1)[0]
            wildcard_import = f"import {pkg_prefix}.*"
            direct_import = f"import {req_import}"
            if direct_import not in content and wildcard_import not in content:
                return False, f"{filepath}: Memanggil {desc} tetapi tidak menemukan import '{direct_import}' atau '{wildcard_import}'."

    # 5. Deteksi penggunaan 'it' di dalam lambda dengan parameter bernama ({ param -> it.something })
    named_lambda_re = re.compile(r'\{\s*([a-zA-Z0-9_,\s()]+)\s*->')
    it_providers_re = re.compile(r'\b(?:let|also|takeIf|takeUnless|forEach|forEachIndexed|map|mapIndexed|filter|filterNot|find|firstOrNull|any|all|count|sortBy|sortWith|minByOrNull|maxByOrNull|groupBy|distinctBy|associateBy|onValueChange|onCheckedChange)\b')
    brace_depth = 0
    stack = [(0, False, 'file')]
    for line_idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('*'):
            continue
        # Masking lambda satu baris yang menyediakan 'it' sendiri
        masked_line = re.sub(r'\{[^{}>\-]*\bit\b[^{}>\-]*\}', '{ __SAFE_IT__ }', line)

        m_named = named_lambda_re.search(line)
        named_param = None
        if m_named:
            p = m_named.group(1).strip()
            if p == 'it' or ' it' in p or 'it ' in p:
                named_param = 'it'
            else:
                named_param = p

        has_it_provider = bool(it_providers_re.search(line) and '{' in line)

        for char in line:
            if char == '{':
                brace_depth += 1
                if named_param:
                    if named_param == 'it':
                        stack.append((brace_depth, True, 'lambda_it'))
                    else:
                        stack.append((brace_depth, False, f'lambda:{named_param}'))
                elif has_it_provider:
                    stack.append((brace_depth, True, 'it_provider'))
                else:
                    parent_has_it = stack[-1][1]
                    parent_src = stack[-1][2]
                    stack.append((brace_depth, parent_has_it, parent_src))
            elif char == '}':
                if len(stack) > 1 and stack[-1][0] == brace_depth:
                    stack.pop()
                brace_depth = max(0, brace_depth - 1)

        if re.search(r'\bit\b(?!\s*->)', masked_line) and '->' not in masked_line:
            curr_has_it = stack[-1][1]
            curr_src = stack[-1][2]
            if not curr_has_it and curr_src.startswith('lambda:'):
                param_name = curr_src.split(':', 1)[1]
                return False, f"{filepath}:{line_idx}: Penggunaan 'it' tidak valid di dalam lambda dengan parameter bernama '{param_name} ->'."

    # 6. Keseimbangan tanda kurung kurawal {}, (), []
    return check_kotlin_brackets(filepath, content)

def check_xml_file(filepath):
    try:
        ET.parse(filepath)
        return True, None
    except Exception as e:
        return False, f"{filepath}: Format XML tidak valid ({e})"

def main():
    root_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    errors = []
    checked_kt = 0
    checked_xml = 0

    kt_files = []
    class_map = {}
    class_decl_re = re.compile(r'^(?:data\s+class|class|object|interface|enum\s+class)\s+([a-zA-Z0-9_]+)', re.MULTILINE)
    pkg_re = re.compile(r'^\s*package\s+([a-zA-Z0-9_.]+)', re.MULTILINE)

    for root, _, files in os.walk(root_dir):
        # Abaikan direktori build, caches, dan git
        if "/build/" in root or "/.gradle/" in root or "/.git/" in root:
            continue
        for f in files:
            path = os.path.join(root, f)
            if f.endswith(".kt"):
                checked_kt += 1
                kt_files.append(path)
                ok, err = check_kotlin_file(path)
                if not ok:
                    errors.append(err)
                try:
                    with open(path, "r", encoding="utf-8") as fp:
                        txt = fp.read()
                    m_pkg = pkg_re.search(txt)
                    pkg = m_pkg.group(1) if m_pkg else ""
                    for m in class_decl_re.finditer(txt):
                        cname = m.group(1)
                        class_map[cname] = pkg
                except Exception:
                    pass
            elif f.endswith(".xml") and ("res/" in path or "AndroidManifest.xml" in path):
                checked_xml += 1
                ok, err = check_xml_file(path)
                if not ok:
                    errors.append(err)

    # 7. Deteksi referensi class internal proyek tanpa import yang valid (Cross-Reference Resolution)
    for path in kt_files:
        try:
            with open(path, "r", encoding="utf-8") as fp:
                txt = fp.read()
            m_pkg = pkg_re.search(txt)
            cur_pkg = m_pkg.group(1) if m_pkg else ""
            for cname, cpkg in class_map.items():
                if not cpkg or cur_pkg == cpkg:
                    continue
                # Jika file memanggil nama class tersebut
                if re.search(r'\b' + re.escape(cname) + r'\b', txt):
                    direct_import = f"import {cpkg}.{cname}"
                    wildcard_import = f"import {cpkg}.*"
                    fqcn = f"{cpkg}.{cname}"
                    if direct_import not in txt and wildcard_import not in txt and fqcn not in txt:
                        errors.append(f"{path}: Memanggil class/object '{cname}' dari package '{cpkg}', tetapi tidak menemukan import '{direct_import}' atau '{wildcard_import}'.")
        except Exception:
            pass

    print(f"Checked {checked_kt} Kotlin files and {checked_xml} XML files.")
    if errors:
        print("\n--- PRE-FLIGHT LINTER ERRORS FOUND ---")
        for err in errors:
            print(f"[ERROR] {err}")
        sys.exit(1)
    else:
        print("All Kotlin and XML files are syntactically balanced, imports valid, and pre-flight checks passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
