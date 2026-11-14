#!/usr/bin/env python3
"""
Skill Smoke Test Runner (< 5 detik)
Memvalidasi kesehatan seluruh generator & linter skill secara end-to-end di direktori sementara:
1. init_compose_project.py -> scaffold proyek baru lengkap
2. Verifikasi file infrastruktur CI/CD (gradlew, gradle.properties, libs.versions.toml, workflow)
3. Verifikasi Adaptive Vector Icon default (brand)
4. verify_kotlin_syntax.py -> harus lolos 0 hard error
"""

import os
import sys
import subprocess
import tempfile
import xml.etree.ElementTree as ET


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    init_script = os.path.join(script_dir, "init_compose_project.py")
    lint_script = os.path.join(script_dir, "verify_kotlin_syntax.py")

    with tempfile.TemporaryDirectory(prefix="acb_smoke_") as tmp_dir:
        print(f"[1/4] Generating sample project in {tmp_dir} ...")
        r_init = subprocess.run(
            [sys.executable, init_script, "--dir", tmp_dir, "--name", "SmokeApp", "--package", "com.smoke.app"],
            capture_output=True,
            text=True,
        )
        if r_init.returncode != 0:
            print("FAILED: init_compose_project.py")
            print(r_init.stdout, r_init.stderr)
            sys.exit(1)

        print("[2/4] Checking required build & CI infrastructure files ...")
        required_files = [
            "gradlew",
            "gradle/wrapper/gradle-wrapper.properties",
            "gradle.properties",
            "gradle/libs.versions.toml",
            ".github/workflows/build-apk.yml",
            "app/src/main/res/drawable/ic_launcher_background.xml",
            "app/src/main/res/drawable/ic_launcher_foreground.xml",
            "app/src/main/res/drawable/ic_launcher_monochrome.xml",
            "app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml",
        ]
        for rel in required_files:
            full = os.path.join(tmp_dir, rel)
            if not os.path.exists(full):
                print(f"FAILED: Missing required generated file: {rel}")
                sys.exit(1)

        print("[3/4] Validating generated Adaptive Vector Icons XML ...")
        for icon_rel in (
            "app/src/main/res/drawable/ic_launcher_foreground.xml",
            "app/src/main/res/drawable/ic_launcher_monochrome.xml",
        ):
            icon_path = os.path.join(tmp_dir, icon_rel)
            ET.parse(icon_path)
            with open(icon_path, "r", encoding="utf-8") as fp:
                content = fp.read()
                if 'pathData=""' in content:
                    print(f"FAILED: Empty pathData found in {icon_rel}")
                    sys.exit(1)

        print("[4/4] Running verify_kotlin_syntax.py on generated project ...")
        r_lint = subprocess.run(
            [sys.executable, lint_script, tmp_dir],
            capture_output=True,
            text=True,
        )
        if r_lint.returncode != 0:
            print("FAILED: verify_kotlin_syntax.py returned errors:")
            print(r_lint.stdout, r_lint.stderr)
            sys.exit(1)

    print("PASS: All android-compose-builder smoke tests succeeded!")
    sys.exit(0)


if __name__ == "__main__":
    main()
