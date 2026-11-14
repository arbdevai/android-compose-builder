# Universal Agent Guidelines: Android Jetpack Compose Builder

This repository contains the `android-compose-builder` agent skill.
**Single Source of Truth:** All AI coding agents (Antigravity CLI, Claude Code, Codex CLI, Cursor, Copilot) MUST read and strictly follow [`SKILL.md`](./SKILL.md) (and its referenced docs in `references/`) before taking action.

## Non-Negotiable Execution Contract (Summary)
1. **Zero Local Gradle Build:** Never run `./gradlew` locally in chroot. Delegate compilation to GitHub Actions.
2. **Pre-Flight Check:** Run `python3 scripts/verify_kotlin_syntax.py .` whenever `.kt` or Android `.xml` files are modified (0 hard errors required before push).
3. **Autopilot Delivery:** Do NOT ask the user to run `git push`. After verification passes, commit, push, monitor CI (`gh run watch <RUN_ID> --interval 60`), and deliver the finished GitHub Release APK download link.
4. **CI Failure Pattern Loop:** On CI failure, inspect `gh run view <RUN_ID> --log-failed`, log the root-cause pattern in `docs/STATE.md`, fix it, re-verify locally, and push again until green.
5. **Living Session Memory:** Always read `docs/PRD.md` and `docs/STATE.md` at session start; if `docs/PRD.md` is missing, interview the user first.
