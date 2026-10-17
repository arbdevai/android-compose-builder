#!/usr/bin/env bash
# ==============================================================================
# Android Compose Builder Skill - Multi-CLI Auto-Detect Installer
# Compatible with: Antigravity CLI (agy), Claude Code (claude), Codex CLI (codex)
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
UNINSTALL=false
CHECK_ONLY=false

while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --all) TARGET_ENV="all" ;;
        --agy|--antigravity) TARGET_ENV="antigravity" ;;
        --claude) TARGET_ENV="claude" ;;
        --codex) TARGET_ENV="codex" ;;
        --workspace|-w) INSTALL_SCOPE="workspace" ;;
        --global|-g) INSTALL_SCOPE="global" ;;
        --uninstall) UNINSTALL=true ;;
        --check|--status) CHECK_ONLY=true ;;
        -h|--help)
            echo "Usage: ./install.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --all                 Install to all supported CLIs (Antigravity, Claude, Codex)"
            echo "  --antigravity, --agy  Install specifically for Antigravity CLI"
            echo "  --claude              Install specifically for Claude Code CLI"
            echo "  --codex               Install specifically for OpenAI Codex CLI"
            echo "  --global, -g          Install to user global config directory (default)"
            echo "  --workspace, -w       Install to current workspace/project directory"
            echo "  --check, --status     Check detected CLIs and current installation status"
            echo "  --uninstall           Remove installed skills and configs"
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
    echo -e "  • Antigravity Global: $([ -f "$HOME/.gemini/config/skills/$SKILL_NAME/SKILL.md" ] && echo -e "${GREEN}Installed${NC}" || echo -e "${YELLOW}Missing${NC}")"
    echo -e "  • Claude Global     : $([ -f "$HOME/.claude/skills/$SKILL_NAME/SKILL.md" ] && echo -e "${GREEN}Installed${NC}" || echo -e "${YELLOW}Missing${NC}")"
    echo -e "  • Codex Global      : $([ -f "$HOME/.codex/skills/$SKILL_NAME/SKILL.md" ] && echo -e "${GREEN}Installed${NC}" || echo -e "${YELLOW}Missing${NC}")"
    exit 0
fi

# Ensure Source Repository is available
prepare_source() {
    if [ -n "$SCRIPT_DIR" ] && [ -f "$SCRIPT_DIR/SKILL.md" ]; then
        SOURCE_DIR="$SCRIPT_DIR"
    else
        echo -e "${BLUE}[i] Running via remote installer. Preparing source files...${NC}"
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
    chmod +x "$SOURCE_DIR"/scripts/*.py 2>/dev/null || true
}

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
    echo -e "${GREEN}[✓] Successfully uninstalled $SKILL_NAME from configs.${NC}"
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

install_antigravity() {
    if [ "$INSTALL_SCOPE" = "workspace" ]; then
        local target=".agents/skills/$SKILL_NAME"
        echo -e "${BLUE}[*] Installing to Workspace for Antigravity: $target${NC}"
        copy_skill_files "$target"
        cp "$SOURCE_DIR/AGENTS.md" ./AGENTS.md 2>/dev/null || true
        cp "$SOURCE_DIR/GEMINI.md" ./GEMINI.md 2>/dev/null || true
    else
        local target="$HOME/.gemini/config/skills/$SKILL_NAME"
        echo -e "${BLUE}[*] Installing to Global Antigravity Config: $target${NC}"
        copy_skill_files "$target"
    fi
    echo -e "${GREEN}[✓] Antigravity CLI compatibility active.${NC}"
}

install_claude() {
    if [ "$INSTALL_SCOPE" = "workspace" ]; then
        local target=".claude/skills/$SKILL_NAME"
        echo -e "${BLUE}[*] Installing to Workspace for Claude CLI: $target${NC}"
        copy_skill_files "$target"
        cp "$SOURCE_DIR/CLAUDE.md" ./CLAUDE.md 2>/dev/null || true
    else
        local target="$HOME/.claude/skills/$SKILL_NAME"
        echo -e "${BLUE}[*] Installing to Global Claude Config: $target${NC}"
        copy_skill_files "$target"
        # Also copy reference CLAUDE.md template if global config dir exists
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
        copy_skill_files "$target"
        cp "$SOURCE_DIR/CODEX.md" ./CODEX.md 2>/dev/null || true
    else
        local target="$HOME/.codex/skills/$SKILL_NAME"
        echo -e "${BLUE}[*] Installing to Global Codex Config: $target${NC}"
        copy_skill_files "$target"
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

# Fallback: if auto-detect found none of them, install globally for all 3 as default
if [ "$INSTALL_COUNT" -eq 0 ] && [ "$TARGET_ENV" = "auto" ]; then
    echo -e "${YELLOW}[i] No specific CLI detected. Installing globally to Antigravity, Claude, and Codex standards...${NC}"
    install_antigravity
    install_claude
    install_codex
fi

echo ""
echo -e "${GREEN}${BOLD}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}${BOLD}  Installation Complete!                                        ${NC}"
echo -e "${GREEN}${BOLD}═══════════════════════════════════════════════════════════════${NC}"
echo -e "Skill '${SKILL_NAME}' is now loaded and available for your AI agents."
echo -e "You can trigger it anytime in Antigravity, Claude Code, or Codex CLI."
echo ""
