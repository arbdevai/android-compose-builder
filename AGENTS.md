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
5. **CI/CD Hygiene**:
   - Zero local Gradle compilation; delegate to GitHub Actions.
   - Strictly monitor CI with 60-second intervals to preserve GitHub API quotas.
