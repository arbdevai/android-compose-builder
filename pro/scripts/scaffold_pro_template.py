#!/usr/bin/env python3
"""
Pro Template Scaffolder
Membuat proyek Android dari template Pro (kasir) di atas generator Gratis:
1. Jalankan scripts/init_compose_project.py (Gratis) untuk proyek dasar.
2. Tempel overlay template Pro (package diganti sesuai --package).
3. Tambahkan dependensi Room + KSP ke gradle/libs.versions.toml,
   build.gradle.kts (root) dan app/build.gradle.kts.
4. Jalankan scripts/verify_kotlin_syntax.py — harus 0 hard error.

Template yang tersedia: kasir
"""

import argparse
import os
import shutil
import subprocess
import sys

ROOM_VERSION = "2.7.0"
KSP_VERSION = "2.2.20-1.0.28"


def replace_once(content: str, marker: str, replacement: str, label: str) -> str:
    if marker not in content:
        print(f"FAILED: Marker tidak ditemukan untuk {label}: {marker!r}")
        sys.exit(1)
    return content.replace(marker, replacement, 1)


def patch_versions_toml(path: str) -> None:
    with open(path, "r", encoding="utf-8") as fp:
        content = fp.read()
    content = replace_once(
        content,
        'junit = "4.13.2"',
        'junit = "4.13.2"\nroom = "%s"\nksp = "%s"' % (ROOM_VERSION, KSP_VERSION),
        "room/ksp versions",
    )
    content = replace_once(
        content,
        'junit = { module = "junit:junit", version.ref = "junit" }',
        'junit = { module = "junit:junit", version.ref = "junit" }\n'
        'androidx-room-runtime = { module = "androidx.room:room-runtime", version.ref = "room" }\n'
        'androidx-room-ktx = { module = "androidx.room:room-ktx", version.ref = "room" }\n'
        'androidx-room-compiler = { module = "androidx.room:room-compiler", version.ref = "room" }',
        "room libraries",
    )
    content = replace_once(
        content,
        'kotlin-serialization = { id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlin" }',
        'kotlin-serialization = { id = "org.jetbrains.kotlin.plugin.serialization", version.ref = "kotlin" }\n'
        'ksp = { id = "com.google.devtools.ksp", version.ref = "ksp" }',
        "ksp plugin",
    )
    with open(path, "w", encoding="utf-8") as fp:
        fp.write(content)


def patch_root_build(path: str) -> None:
    with open(path, "r", encoding="utf-8") as fp:
        content = fp.read()
    content = replace_once(
        content,
        "    alias(libs.plugins.kotlin.serialization) apply false",
        "    alias(libs.plugins.kotlin.serialization) apply false\n"
        "    alias(libs.plugins.ksp) apply false",
        "root ksp plugin",
    )
    with open(path, "w", encoding="utf-8") as fp:
        fp.write(content)


def patch_app_build(path: str) -> None:
    with open(path, "r", encoding="utf-8") as fp:
        content = fp.read()
    content = replace_once(
        content,
        "    alias(libs.plugins.kotlin.serialization)",
        "    alias(libs.plugins.kotlin.serialization)\n    alias(libs.plugins.ksp)",
        "app ksp plugin",
    )
    content = replace_once(
        content,
        "    implementation(libs.androidx.work.runtime.ktx)",
        "    implementation(libs.androidx.work.runtime.ktx)\n\n"
        "    // Room (Pro template)\n"
        "    implementation(libs.androidx.room.runtime)\n"
        "    implementation(libs.androidx.room.ktx)\n"
        "    ksp(libs.androidx.room.compiler)",
        "room dependencies",
    )
    with open(path, "w", encoding="utf-8") as fp:
        fp.write(content)


def copy_template(template_dir: str, target_dir: str, package_name: str, app_name: str) -> None:
    pkg_path = package_name.replace(".", "/")
    for root, _dirs, files in os.walk(template_dir):
        for name in files:
            if name == "README.md":
                continue
            src = os.path.join(root, name)
            rel = os.path.relpath(src, template_dir)
            rel = rel.replace("__PACKAGE__", pkg_path)
            dest = os.path.join(target_dir, rel)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with open(src, "r", encoding="utf-8") as fp:
                content = fp.read()
            content = content.replace("__PACKAGE__", package_name)
            content = content.replace("__APP_NAME__", app_name)
            with open(dest, "w", encoding="utf-8") as fp:
                fp.write(content)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold proyek dari template Pro")
    parser.add_argument("--template", default="kasir", choices=["kasir"],
                        help="Template Pro yang dipakai")
    parser.add_argument("--dir", required=True, help="Direktori proyek baru")
    parser.add_argument("--name", required=True, help="Nama aplikasi")
    parser.add_argument("--package", required=True, help="Package aplikasi")
    args = parser.parse_args()

    pro_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skill_root = os.path.dirname(pro_root)
    init_script = os.path.join(skill_root, "scripts", "init_compose_project.py")
    lint_script = os.path.join(skill_root, "scripts", "verify_kotlin_syntax.py")
    template_dir = os.path.join(pro_root, "templates", args.template)
    if not os.path.isdir(template_dir):
        print(f"FAILED: Template tidak ditemukan: {template_dir}")
        sys.exit(1)

    target_dir = os.path.abspath(args.dir)
    print(f"[1/4] Membuat proyek dasar '{args.name}' ({args.package}) ...")
    r = subprocess.run(
        [sys.executable, init_script, "--dir", target_dir,
         "--name", args.name, "--package", args.package],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print("FAILED: init_compose_project.py")
        print(r.stdout, r.stderr)
        sys.exit(1)

    print(f"[2/4] Menempel template Pro '{args.template}' ...")
    copy_template(template_dir, target_dir, args.package, args.name)

    print("[3/4] Menambahkan dependensi Room + KSP ...")
    patch_versions_toml(os.path.join(target_dir, "gradle", "libs.versions.toml"))
    patch_root_build(os.path.join(target_dir, "build.gradle.kts"))
    patch_app_build(os.path.join(target_dir, "app", "build.gradle.kts"))

    print("[4/4] Menjalankan verify_kotlin_syntax.py ...")
    r = subprocess.run(
        [sys.executable, lint_script, target_dir],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        print("FAILED: verify_kotlin_syntax.py returned errors:")
        print(r.stdout, r.stderr)
        sys.exit(1)

    print(f"PASS: Proyek Pro '{args.template}' siap di {target_dir}")
    print("Langkah berikut: git init, commit 'Release v1.0.0', push — CI akan build APK.")
    sys.exit(0)


if __name__ == "__main__":
    main()
