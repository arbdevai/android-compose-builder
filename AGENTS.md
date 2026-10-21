# Universal Agent Guidelines: Android Jetpack Compose Builder

This repository contains the `android-compose-builder` agent skill.
All AI coding agents (Antigravity CLI, Claude Code, Codex CLI, Cursor, Copilot) operating in this repository or utilizing this skill must adhere to the rules defined in `SKILL.md`:

1. **Zero Dummy Data**: Always target authentic hardware/cloud APIs with robust reverse-engineering.
2. **Skeleton Screens & Shimmer**: Reject empty-screen loading spinners in favor of layout-matching skeleton shimmer screens.
3. **Resilient Concurrency**:
   - Atomic authentication using `Mutex.withLock`.
   - Anti-deadlock: zero re-entrant Semaphore permit acquisitions.
   - Sequential pre-auth before parallel async workers.
4. **Clean Tone**: Professional, direct microcopy without dramatic or condescending phrasing.
5. **CI/CD Hygiene & Anti-Hallucination**:
   - Zero local Gradle compilation; delegate to GitHub Actions.
   - Strictly monitor CI with 60-second intervals to preserve GitHub API quotas.
   - Zero fabricated CI/release status without verified command outputs (`gh run view`, `gh release view`).
6. **In-App Updater & Storage Hygiene**:
   - Automatic cleanup of legacy APK files from download directories to prevent device storage bloat.
   - Pre-check local files to prevent redundant downloads.
7. **Zero-CI-Failure Pre-Flight Verification**:
   - Mandatory execution of `verify_kotlin_syntax.py` before commit/push.
   - Verifies coroutine suspend boundaries, `kotlin.Result` extraction, Compose modifier imports, and cross-package symbol resolution.
8. **Release Keystore & Signing (Anti-Muter-Muter)**:
   - Zero hesitation when `keytool` is missing: install immediately (`sudo apt update && sudo apt install -y openjdk-17-jre-headless`).
   - Run `python3 scripts/setup_release_keystore.py` or use non-interactive `keytool -genkeypair -noprompt -dname "..."` to configure GitHub Secrets (`KEYSTORE_BASE64`, `KEYSTORE_PASSWORD`, `KEY_ALIAS`, `KEY_PASSWORD`) in one step.
