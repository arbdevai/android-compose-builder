#!/usr/bin/env python3
"""
Android Compose Builder Skill - Multi-CLI Auto-Detect Installer (Python)
Compatible with: Antigravity CLI (agy), Claude Code (claude), Codex CLI (codex)
Supports: Symlink live-sync, Git auto-pull, and background shell auto-updates
"""

import os
import sys
import shutil
import subprocess
import argparse
from pathlib import Path

SKILL_NAME = "android-compose-builder"
REPO_URL = "https://github.com/arbdevai/android-compose-builder.git"

def print_header():
    print("\033[1;36m")
    print("  ╔═══════════════════════════════════════════════════════════╗")
    print("  ║        Android Compose Builder - Multi-CLI Installer      ║")
    print("  ║  Antigravity CLI (agy) • Claude CLI • Codex CLI Compat    ║")
    print("  ║      Live-Sync Symlinks • Instant Background Auto-Update  ║")
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

def deploy_skill(source_dir: Path, target_dir: Path, use_symlink: bool = True):
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    if use_symlink:
        if target_dir.is_symlink() or target_dir.exists():
            if target_dir.is_symlink():
                target_dir.unlink()
            else:
                shutil.rmtree(target_dir)
        try:
            target_dir.symlink_to(source_dir, target_is_directory=True)
            print(f"    Linked: {target_dir} -> {source_dir} (Live Sync)")
            return
        except Exception as e:
            print(f"    \033[33m[!] Symlink creation failed ({e}), falling back to copy.\033[0m")
    
    if target_dir.is_symlink():
        target_dir.unlink()
    elif target_dir.exists():
        shutil.rmtree(target_dir)
    copy_skill(source_dir, target_dir)
    print(f"    Copied: {target_dir}")

def enable_autoupdate_hook():
    home = Path.home()
    hook_snippet = """
# >>> android-compose-builder auto-update >>>
_update_android_compose_builder() {
    local target_repo=""
    if [ -d "$HOME/projects/android-compose-builder/.git" ]; then
        target_repo="$HOME/projects/android-compose-builder"
    elif [ -d "$HOME/.local/share/skills/android-compose-builder/.git" ]; then
        target_repo="$HOME/.local/share/skills/android-compose-builder"
    fi
    if [ -n "$target_repo" ] && git -C "$target_repo" diff --quiet 2>/dev/null; then
        (git -C "$target_repo" pull --quiet &>/dev/null &)
    fi
}
_update_android_compose_builder
# <<< android-compose-builder auto-update <<<
"""
    touched = False
    for rc_name in [".bashrc", ".zshrc"]:
        rc_path = home / rc_name
        if rc_path.exists():
            content = rc_path.read_text(encoding="utf-8")
            if "android-compose-builder auto-update" not in content:
                with rc_path.open("a", encoding="utf-8") as f:
                    f.write(hook_snippet)
                print(f"\033[32m[✓] Background auto-update hook added to: {rc_path}\033[0m")
                touched = True
            else:
                print(f"\033[36m[i] Background auto-update hook already present in: {rc_path}\033[0m")
                touched = True

    if not touched:
        rc_path = home / ".bashrc"
        with rc_path.open("a", encoding="utf-8") as f:
            f.write(hook_snippet)
        print(f"\033[32m[✓] Background auto-update hook added to: {rc_path}\033[0m")

def disable_autoupdate_hook():
    home = Path.home()
    import re
    pattern = re.compile(r'\n?# >>> android-compose-builder auto-update >>>.*?# <<< android-compose-builder auto-update <<<\n?', re.DOTALL)
    for rc_name in [".bashrc", ".zshrc"]:
        rc_path = home / rc_name
        if rc_path.exists():
            content = rc_path.read_text(encoding="utf-8")
            if "android-compose-builder auto-update" in content:
                new_content = pattern.sub('\n', content)
                rc_path.write_text(new_content, encoding="utf-8")
                print(f"\033[33m[✓] Removed background auto-update hook from: {rc_path}\033[0m")

def main():
    parser = argparse.ArgumentParser(description="Android Compose Builder Skill Installer")
    parser.add_argument("--all", action="store_true", help="Install to all CLIs (Antigravity, Claude, Codex)")
    parser.add_argument("--antigravity", "--agy", action="store_true", help="Install specifically for Antigravity CLI")
    parser.add_argument("--claude", action="store_true", help="Install specifically for Claude Code")
    parser.add_argument("--codex", action="store_true", help="Install specifically for OpenAI Codex")
    parser.add_argument("--workspace", "-w", action="store_true", help="Install to current workspace/project directory")
    parser.add_argument("--global", "-g", dest="global_install", action="store_true", default=True, help="Install globally to home directory (default)")
    parser.add_argument("--link", "-l", dest="use_symlink", action="store_true", default=True, help="Create symlinks for instant live-sync (default for global)")
    parser.add_argument("--copy", "-c", dest="use_symlink", action="store_false", help="Copy files physically instead of symlinking")
    parser.add_argument("--update", "-u", action="store_true", help="Fetch latest version from GitHub and sync installation")
    parser.add_argument("--auto-update", action="store_true", help="Enable background auto-update on shell startup")
    parser.add_argument("--disable-auto-update", action="store_true", help="Remove shell startup auto-update hook")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall skill from configurations and hooks")
    parser.add_argument("--check", "--status", action="store_true", help="Check detected CLIs and status")
    args = parser.parse_args()

    print_header()

    home = Path.home()
    source_dir = Path(__file__).resolve().parent

    if args.disable_auto_update:
        disable_autoupdate_hook()
        return

    if args.auto_update and not args.update and not args.check:
        enable_autoupdate_hook()
        return

    detected = detect_environments()
    print("\033[1mDetected AI Agent CLI Environments:\033[0m")
    for cli, found in detected.items():
        status = "\033[32mDetected\033[0m" if found else "\033[33mNot detected\033[0m"
        print(f"  • {cli.capitalize()} CLI: {status}")
    print()

    if args.check:
        print("\033[1mInstallation Status:\033[0m")
        print(f"  • Antigravity: {'\033[32mInstalled (Live)\033[0m' if (home / '.gemini' / 'config' / 'skills' / SKILL_NAME / 'SKILL.md').exists() else '\033[33mMissing\033[0m'}")
        print(f"  • Claude     : {'\033[32mInstalled (Live)\033[0m' if (home / '.claude' / 'skills' / SKILL_NAME / 'SKILL.md').exists() else '\033[33mMissing\033[0m'}")
        print(f"  • Codex      : {'\033[32mInstalled (Live)\033[0m' if (home / '.codex' / 'skills' / SKILL_NAME / 'SKILL.md').exists() else '\033[33mMissing\033[0m'}")
        has_hook = False
        for rc_name in [".bashrc", ".zshrc"]:
            p = home / rc_name
            if p.exists() and "android-compose-builder auto-update" in p.read_text(encoding="utf-8", errors="ignore"):
                has_hook = True
                break
        print(f"  • Shell Auto-Update: {'\033[32mActive in shell profile\033[0m' if has_hook else '\033[33mNot enabled (Use python3 install.py --auto-update)\033[0m'}")
        return

    if args.uninstall:
        print("\033[33m[!] Uninstalling...\033[0m")
        targets = [
            home / ".gemini" / "config" / "skills" / SKILL_NAME,
            home / ".claude" / "skills" / SKILL_NAME,
            home / ".codex" / "skills" / SKILL_NAME,
        ]
        for t in targets:
            if t.is_symlink():
                t.unlink()
            elif t.exists():
                shutil.rmtree(t)
        disable_autoupdate_hook()
        print("\033[32m[✓] Uninstalled successfully.\033[0m")
        return

    if args.update:
        print("\033[34m[*] Updating Android Compose Builder Skill...\033[0m")
        git_dir = source_dir / ".git"
        if git_dir.exists():
            subprocess.run(["git", "-C", str(source_dir), "pull", "--quiet"])
            print("\033[32m[✓] Source repository updated to latest.\033[0m")
        if args.auto_update:
            enable_autoupdate_hook()
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
    use_symlink = args.use_symlink and not args.workspace

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
        deploy_skill(source_dir, t_dir, use_symlink=use_symlink)
        print(f"\033[32m[✓] {cli.capitalize()} skill active.\033[0m")

    if args.auto_update:
        enable_autoupdate_hook()

    print("\n\033[1;32m═══════════════════════════════════════════════════════════════\033[0m")
    print(f"\033[1;32m  Installation Complete for: {', '.join(targets_to_install).upper()}\033[0m")
    print("\033[1;32m═══════════════════════════════════════════════════════════════\033[0m")
    if use_symlink:
        print("Live Sync: Enabled (Any change in repository instantly reflects in all agents).")
    print("Tip: Run './install.sh --auto-update' to keep skills automatically synced via background git pull.\n")

if __name__ == "__main__":
    main()
