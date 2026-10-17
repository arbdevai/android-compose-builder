#!/usr/bin/env python3
"""
Android Compose Builder Skill - Multi-CLI Auto-Detect Installer (Python)
Compatible with: Antigravity CLI (agy), Claude Code (claude), Codex CLI (codex)
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

SKILL_NAME = "android-compose-builder"
REPO_URL = "https://github.com/arbdevai/android-compose-builder.git"

def print_header():
    print("\033[1;36m")
    print("  ╔═══════════════════════════════════════════════════════════╗")
    print("  ║        Android Compose Builder - Multi-CLI Installer      ║")
    print("  ║  Antigravity CLI (agy) • Claude CLI • Codex CLI Compat    ║")
    print("  ╚═══════════════════════════════════════════════════════════╝")
    print("\033[0m")

def detect_environments():
    home = Path.home()
    detected = {
        "antigravity": shutil.which("agy") is not None or shutil.which("antigravity") is not None or (home / ".gemini").exists(),
        "claude": shutil.which("claude") is not None or (home / ".claude").exists(),
        "codex": shutil.which("codex") is not None or (home / ".codex").exists(),
    }
    return detected

def copy_skill(source_dir: Path, target_dir: Path):
    target_dir.mkdir(parents=True, exist_ok=True)
    scripts_target = target_dir / "scripts"
    scripts_target.mkdir(parents=True, exist_ok=True)

    shutil.copy2(source_dir / "SKILL.md", target_dir / "SKILL.md")
    for script_file in (source_dir / "scripts").glob("*.py"):
        dest = scripts_target / script_file.name
        shutil.copy2(script_file, dest)
        try:
            dest.chmod(0o755)
        except Exception:
            pass

def main():
    parser = argparse.ArgumentParser(description="Android Compose Builder Skill Installer")
    parser.add_argument("--all", action="store_true", help="Install to all CLIs (Antigravity, Claude, Codex)")
    parser.add_argument("--antigravity", "--agy", action="store_true", help="Install specifically for Antigravity CLI")
    parser.add_argument("--claude", action="store_true", help="Install specifically for Claude Code")
    parser.add_argument("--codex", action="store_true", help="Install specifically for OpenAI Codex")
    parser.add_argument("--workspace", "-w", action="store_true", help="Install to current workspace/project directory")
    parser.add_argument("--global", "-g", dest="global_install", action="store_true", default=True, help="Install globally to home directory (default)")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall skill from configurations")
    parser.add_argument("--check", "--status", action="store_true", help="Check detected CLIs and status")
    args = parser.parse_args()

    print_header()

    home = Path.home()
    source_dir = Path(__file__).resolve().parent

    detected = detect_environments()
    print("\033[1mDetected AI Agent CLI Environments:\033[0m")
    for cli, found in detected.items():
        status = "\033[32mDetected\033[0m" if found else "\033[33mNot detected\033[0m"
        print(f"  • {cli.capitalize()} CLI: {status}")
    print()

    if args.check:
        print("\033[1mInstallation Status:\033[0m")
        print(f"  • Antigravity: {'\033[32mInstalled\033[0m' if (home / '.gemini' / 'config' / 'skills' / SKILL_NAME / 'SKILL.md').exists() else '\033[33mMissing\033[0m'}")
        print(f"  • Claude     : {'\033[32mInstalled\033[0m' if (home / '.claude' / 'skills' / SKILL_NAME / 'SKILL.md').exists() else '\033[33mMissing\033[0m'}")
        print(f"  • Codex      : {'\033[32mInstalled\033[0m' if (home / '.codex' / 'skills' / SKILL_NAME / 'SKILL.md').exists() else '\033[33mMissing\033[0m'}")
        return

    if args.uninstall:
        print("\033[33m[!] Uninstalling...\033[0m")
        targets = [
            home / ".gemini" / "config" / "skills" / SKILL_NAME,
            home / ".claude" / "skills" / SKILL_NAME,
            home / ".codex" / "skills" / SKILL_NAME,
        ]
        for t in targets:
            if t.exists():
                shutil.rmtree(t)
        print("\033[32m[✓] Uninstalled successfully.\033[0m")
        return

    targets_to_install = []
    if args.all:
        targets_to_install = ["antigravity", "claude", "codex"]
    elif args.antigravity:
        targets_to_install.append("antigravity")
    elif args.claude:
        targets_to_install.append("claude")
    elif args.codex:
        targets_to_install.append("codex")
    else:
        # Auto-detect mode
        targets_to_install = [k for k, v in detected.items() if v]
        if not targets_to_install:
            targets_to_install = ["antigravity", "claude", "codex"]

    cwd = Path.cwd()
    for cli in targets_to_install:
        if args.workspace:
            if cli == "antigravity":
                t_dir = cwd / ".agents" / "skills" / SKILL_NAME
            elif cli == "claude":
                t_dir = cwd / ".claude" / "skills" / SKILL_NAME
            else:
                t_dir = cwd / ".codex" / "skills" / SKILL_NAME
        else:
            if cli == "antigravity":
                t_dir = home / ".gemini" / "config" / "skills" / SKILL_NAME
            elif cli == "claude":
                t_dir = home / ".claude" / "skills" / SKILL_NAME
            else:
                t_dir = home / ".codex" / "skills" / SKILL_NAME

        print(f"\033[34m[*] Installing for {cli.capitalize()}: {t_dir}\033[0m")
        copy_skill(source_dir, t_dir)
        print(f"\033[32m[✓] {cli.capitalize()} skill active.\033[0m")

    print("\n\033[1;32m═══════════════════════════════════════════════════════════════\033[0m")
    print(f"\033[1;32m  Installation Complete for: {', '.join(targets_to_install).upper()}\033[0m")
    print("\033[1;32m═══════════════════════════════════════════════════════════════\033[0m")

if __name__ == "__main__":
    main()
