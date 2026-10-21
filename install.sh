#!/usr/bin/env bash
# ==============================================================================
# Android Compose Builder Skill - Multi-CLI Auto-Detect Installer
# Compatible with: Antigravity CLI (agy), Claude Code (claude), Codex CLI (codex)
# Supports: Symlink live-sync, Git auto-pull, and background shell auto-updates
# ==============================================================================

set -e

# ANSI Color codes
BOLD="\033[1m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
CYAN="\033[0;36m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
NC="\033[0m"

SKILL_NAME="android-compose-builder"
REPO_URL="https://github.com/arbdevai/android-compose-builder.git"
INSTALL_BASE_DIR="$HOME/.local/share/skills/$SKILL_NAME"

print_header() {
    echo -e "${CYAN}${BOLD}"
    echo "  ╔═══════════════════════════════════════════════════════════╗"
    echo "  ║        Android Compose Builder - Multi-CLI Installer      ║"
    echo "  ║  Antigravity CLI (agy) • Claude CLI • Codex CLI Compat    ║"
    echo "  ║      Live-Sync Symlinks • Instant Background Auto-Update  ║"
    echo "  ╚═══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Determine script source directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd)"
if [ ! -f "$SCRIPT_DIR/SKILL.md" ]; then
    SCRIPT_DIR=""
fi

# Parse Arguments
TARGET_ENV="auto"
INSTALL_SCOPE="global"
USE_SYMLINK=true
UNINSTALL=false
CHECK_ONLY=false
DO_UPDATE=false
ENABLE_AUTOUPDATE=false
DISABLE_AUTOUPDATE=false

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --all) TARGET_ENV="all" ;;
        --agy|--antigravity) TARGET_ENV="antigravity" ;;
        --claude) TARGET_ENV="claude" ;;
        --codex) TARGET_ENV="codex" ;;
        --workspace|-w) INSTALL_SCOPE="workspace"; USE_SYMLINK=false ;;
        --global|-g) INSTALL_SCOPE="global" ;;
        --link|-l) USE_SYMLINK=true ;;
        --copy|-c) USE_SYMLINK=false ;;
        --update|-u) DO_UPDATE=true ;;
        --auto-update) ENABLE_AUTOUPDATE=true ;;
        --disable-auto-update) DISABLE_AUTOUPDATE=true ;;
        --uninstall) UNINSTALL=true ;;
        --check|--status) CHECK_ONLY=true ;;
        -h|--help)
            echo "Usage: ./install.sh [OPTIONS]"
            echo ""
            echo "Installation Options:"
            echo "  --all                 Install to all supported CLIs (Antigravity, Claude, Codex)"
            echo "  --antigravity, --agy  Install specifically for Antigravity CLI"
            echo "  --claude              Install specifically for Claude Code CLI"
            echo "  --codex               Install specifically for OpenAI Codex CLI"
            echo "  --global, -g          Install globally to user config directories (default)"
            echo "  --workspace, -w       Install to current workspace/project directory"
            echo "  --link, -l            Create symlinks for instant live-sync (default for global)"
            echo "  --copy, -c            Copy files physically instead of symlinking"
            echo ""
            echo "Auto-Update & Maintenance:"
            echo "  --update, -u          Fetch latest version from GitHub and sync installation"
            echo "  --auto-update         Enable background auto-update on shell startup"
            echo "  --disable-auto-update Remove shell startup auto-update hook"
            echo "  --check, --status     Check detected CLIs and current installation status"
            echo "  --uninstall           Remove installed skills, symlinks, and hooks"
            echo "  -h, --help            Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
    shift
done

print_header

# -----------------------------------------------------------------------------
# Shell Auto-Update Hook Management
# -----------------------------------------------------------------------------
enable_autoupdate_hook() {
    local hook_snippet='
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
# <<< android-compose-builder auto-update <<<'

    local touched=false
    for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
        if [ -f "$rc" ]; then
            if ! grep -q "android-compose-builder auto-update" "$rc"; then
                echo "$hook_snippet" >> "$rc"
                echo -e "${GREEN}[✓] Background auto-update hook added to: $rc${NC}"
                touched=true
            else
                echo -e "${CYAN}[i] Background auto-update hook already present in: $rc${NC}"
                touched=true
            fi
        fi
    done
    if [ "$touched" = false ]; then
        echo "$hook_snippet" >> "$HOME/.bashrc"
        echo -e "${GREEN}[✓] Background auto-update hook added to: $HOME/.bashrc${NC}"
    fi
}

disable_autoupdate_hook() {
    for rc in "$HOME/.bashrc" "$HOME/.zshrc"; do
        if [ -f "$rc" ] && grep -q "android-compose-builder auto-update" "$rc"; then
            sed -i '/# >>> android-compose-builder auto-update >>>/,/# <<< android-compose-builder auto-update <<</d' "$rc"
            echo -e "${YELLOW}[✓] Removed background auto-update hook from: $rc${NC}"
        fi
    done
}

if [ "$DISABLE_AUTOUPDATE" = true ]; then
    disable_autoupdate_hook
    exit 0
fi

if [ "$ENABLE_AUTOUPDATE" = true ] && [ "$DO_UPDATE" = false ] && [ "$CHECK_ONLY" = false ]; then
    enable_autoupdate_hook
    exit 0
fi

# -----------------------------------------------------------------------------
# Detection Logic
# -----------------------------------------------------------------------------
DETECTED_AGY=false
DETECTED_CLAUDE=false
DETECTED_CODEX=false

if command -v agy >/dev/null 2>&1 || command -v antigravity >/dev/null 2>&1 || [ -d "$HOME/.gemini" ]; then
    DETECTED_AGY=true
fi

if command -v claude >/dev/null 2>&1 || [ -d "$HOME/.claude" ]; then
    DETECTED_CLAUDE=true
fi

if command -v codex >/dev/null 2>&1 || [ -d "$HOME/.codex" ]; then
    DETECTED_CODEX=true
fi

echo -e "${BOLD}Detected AI Agent CLI Environments:${NC}"
echo -e "  • Antigravity CLI (agy): $([ "$DETECTED_AGY" = true ] && echo -e "${GREEN}Detected${NC}" || echo -e "${YELLOW}Not detected${NC}")"
echo -e "  • Claude CLI (claude)  : $([ "$DETECTED_CLAUDE" = true ] && echo -e "${GREEN}Detected${NC}" || echo -e "${YELLOW}Not detected${NC}")"
echo -e "  • Codex CLI (codex)    : $([ "$DETECTED_CODEX" = true ] && echo -e "${GREEN}Detected${NC}" || echo -e "${YELLOW}Not detected${NC}")"
echo ""

if [ "$CHECK_ONLY" = true ]; then
    echo -e "${BOLD}Skill Installation Status:${NC}"
    echo -e "  • Antigravity Global: $([ -e "$HOME/.gemini/config/skills/$SKILL_NAME/SKILL.md" ] && echo -e "${GREEN}Installed (Live)${NC}" || echo -e "${YELLOW}Missing${NC}")"
    echo -e "  • Claude Global     : $([ -e "$HOME/.claude/skills/$SKILL_NAME/SKILL.md" ] && echo -e "${GREEN}Installed (Live)${NC}" || echo -e "${YELLOW}Missing${NC}")"
    echo -e "  • Codex Global      : $([ -e "$HOME/.codex/skills/$SKILL_NAME/SKILL.md" ] && echo -e "${GREEN}Installed (Live)${NC}" || echo -e "${YELLOW}Missing${NC}")"
    
    HAS_HOOK=false
    if grep -q "android-compose-builder auto-update" "$HOME/.bashrc" 2>/dev/null || grep -q "android-compose-builder auto-update" "$HOME/.zshrc" 2>/dev/null; then
        HAS_HOOK=true
    fi
    echo -e "  • Shell Auto-Update : $([ "$HAS_HOOK" = true ] && echo -e "${GREEN}Active in shell profile${NC}" || echo -e "${YELLOW}Not enabled (Use ./install.sh --auto-update)${NC}")"
    exit 0
fi

# Ensure Source Repository is available
prepare_source() {
    if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/SKILL.md" ]; then
        SOURCE_DIR="$SCRIPT_DIR"
    else
        echo -e "${BLUE}[i] Preparing local source repository...${NC}"
        mkdir -p "$(dirname "$INSTALL_BASE_DIR")"
        if [ -d "$INSTALL_BASE_DIR/.git" ]; then
            echo -e "    Updating existing repository at ${INSTALL_BASE_DIR}..."
            git -C "$INSTALL_BASE_DIR" pull --quiet
        else
            echo -e "    Cloning ${REPO_URL} into ${INSTALL_BASE_DIR}..."
            rm -rf "$INSTALL_BASE_DIR"
            git clone --quiet "$REPO_URL" "$INSTALL_BASE_DIR"
        fi
        SOURCE_DIR="$INSTALL_BASE_DIR"
    fi
}

# -----------------------------------------------------------------------------
# Update Mode
# -----------------------------------------------------------------------------
if [ "$DO_UPDATE" = true ]; then
    echo -e "${BLUE}[*] Updating Android Compose Builder Skill...${NC}"
    prepare_source
    if [ -d "$SOURCE_DIR/.git" ]; then
        echo -e "    Pulling latest commits in: $SOURCE_DIR"
        git -C "$SOURCE_DIR" pull --quiet
        echo -e "${GREEN}[✓] Latest commit:${NC}"
        git -C "$SOURCE_DIR" log -n 1 --oneline
    fi
    echo -e "${GREEN}[✓] Skill successfully updated.${NC}"
    if [ "$ENABLE_AUTOUPDATE" = true ]; then
        enable_autoupdate_hook
    fi
    exit 0
fi

# -----------------------------------------------------------------------------
# Uninstall Mode
# -----------------------------------------------------------------------------
if [ "$UNINSTALL" = true ]; then
    echo -e "${YELLOW}[!] Uninstalling $SKILL_NAME...${NC}"
    rm -rf "$HOME/.gemini/config/skills/$SKILL_NAME"
    rm -rf "$HOME/.claude/skills/$SKILL_NAME"
    rm -rf "$HOME/.codex/skills/$SKILL_NAME"
    if [ "$INSTALL_SCOPE" = "workspace" ]; then
        rm -rf ".agents/skills/$SKILL_NAME"
        rm -rf ".claude/skills/$SKILL_NAME"
        rm -rf ".codex/skills/$SKILL_NAME"
    fi
    disable_autoupdate_hook
    echo -e "${GREEN}[✓] Successfully uninstalled $SKILL_NAME and cleaned hooks.${NC}"
    exit 0
fi

prepare_source

# -----------------------------------------------------------------------------
# Deployment Functions
# -----------------------------------------------------------------------------
copy_skill_files() {
    local target_dir="$1"
    mkdir -p "$target_dir/scripts"
    cp "$SOURCE_DIR/SKILL.md" "$target_dir/SKILL.md"
    cp "$SOURCE_DIR"/scripts/*.py "$target_dir/scripts/"
    chmod +x "$target_dir"/scripts/*.py
}

deploy_skill() {
    local target_dir="$1"
    mkdir -p "$(dirname "$target_dir")"
    if [ "$USE_SYMLINK" = true ]; then
        rm -rf "$target_dir"
        ln -sfn "$SOURCE_DIR" "$target_dir"
        echo -e "    Linked: $target_dir -> $SOURCE_DIR (Live Sync)"
    else
        rm -rf "$target_dir"
        copy_skill_files "$target_dir"
        echo -e "    Copied: $target_dir"
    fi
}

install_antigravity() {
    if [ "$INSTALL_SCOPE" = "workspace" ]; then
        local target=".agents/skills/$SKILL_NAME"
        echo -e "${BLUE}[*] Installing to Workspace for Antigravity: $target${NC}"
        deploy_skill "$target"
        cp "$SOURCE_DIR/AGENTS.md" ./AGENTS.md 2>/dev/null || true
        cp "$SOURCE_DIR/GEMINI.md" ./GEMINI.md 2>/dev/null || true
    else
        local target="$HOME/.gemini/config/skills/$SKILL_NAME"
        echo -e "${BLUE}[*] Installing to Global Antigravity Config: $target${NC}"
        deploy_skill "$target"
    fi
    echo -e "${GREEN}[✓] Antigravity CLI compatibility active.${NC}"
}

install_claude() {
    if [ "$INSTALL_SCOPE" = "workspace" ]; then
        local target=".claude/skills/$SKILL_NAME"
        echo -e "${BLUE}[*] Installing to Workspace for Claude CLI: $target${NC}"
        deploy_skill "$target"
        cp "$SOURCE_DIR/CLAUDE.md" ./CLAUDE.md 2>/dev/null || true
    else
        local target="$HOME/.claude/skills/$SKILL_NAME"
        echo -e "${BLUE}[*] Installing to Global Claude Config: $target${NC}"
        deploy_skill "$target"
        mkdir -p "$HOME/.claude"
        if [ ! -f "$HOME/.claude/CLAUDE.md" ]; then
            cp "$SOURCE_DIR/CLAUDE.md" "$HOME/.claude/CLAUDE.md"
        fi
    fi
    echo -e "${GREEN}[✓] Claude Code / Claude CLI compatibility active.${NC}"
}

install_codex() {
    if [ "$INSTALL_SCOPE" = "workspace" ]; then
        local target=".codex/skills/$SKILL_NAME"
        echo -e "${BLUE}[*] Installing to Workspace for Codex CLI: $target${NC}"
        deploy_skill "$target"
        cp "$SOURCE_DIR/CODEX.md" ./CODEX.md 2>/dev/null || true
    else
        local target="$HOME/.codex/skills/$SKILL_NAME"
        echo -e "${BLUE}[*] Installing to Global Codex Config: $target${NC}"
        deploy_skill "$target"
        mkdir -p "$HOME/.codex"
        if [ ! -f "$HOME/.codex/instructions.md" ]; then
            cp "$SOURCE_DIR/CODEX.md" "$HOME/.codex/instructions.md"
        fi
    fi
    echo -e "${GREEN}[✓] OpenAI Codex CLI compatibility active.${NC}"
}

# -----------------------------------------------------------------------------
# Execution Flow
# -----------------------------------------------------------------------------
INSTALL_COUNT=0

if [ "$TARGET_ENV" = "antigravity" ] || [ "$TARGET_ENV" = "all" ] || { [ "$TARGET_ENV" = "auto" ] && [ "$DETECTED_AGY" = true ]; }; then
    install_antigravity
    INSTALL_COUNT=$((INSTALL_COUNT + 1))
fi

if [ "$TARGET_ENV" = "claude" ] || [ "$TARGET_ENV" = "all" ] || { [ "$TARGET_ENV" = "auto" ] && [ "$DETECTED_CLAUDE" = true ]; }; then
    install_claude
    INSTALL_COUNT=$((INSTALL_COUNT + 1))
fi

if [ "$TARGET_ENV" = "codex" ] || [ "$TARGET_ENV" = "all" ] || { [ "$TARGET_ENV" = "auto" ] && [ "$DETECTED_CODEX" = true ]; }; then
    install_codex
    INSTALL_COUNT=$((INSTALL_COUNT + 1))
fi

if [ "$INSTALL_COUNT" -eq 0 ] && [ "$TARGET_ENV" = "auto" ]; then
    echo -e "${YELLOW}[i] No specific CLI detected. Installing globally to Antigravity, Claude, and Codex standards...${NC}"
    install_antigravity
    install_claude
    install_codex
fi

# Enable shell auto-update if requested
if [ "$ENABLE_AUTOUPDATE" = true ]; then
    enable_autoupdate_hook
fi

echo ""
echo -e "${GREEN}${BOLD}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}${BOLD}  Installation Complete!                                        ${NC}"
echo -e "${GREEN}${BOLD}═══════════════════════════════════════════════════════════════${NC}"
echo -e "Skill '${SKILL_NAME}' is now loaded and available for your AI agents."
if [ "$USE_SYMLINK" = true ]; then
    echo -e "Live Sync: Enabled (Any update in repository instantly reflects in all agents)."
fi
echo -e "Tip: Run './install.sh --auto-update' to keep skills automatically synced via background git pull."
echo ""
