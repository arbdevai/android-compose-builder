# Claude Code Guidelines: Android Jetpack Compose Development

When working on Android projects with this repository or when the `android-compose-builder` skill is activated, you must strictly follow these rules:

## 1. UI & Skeleton Screens (Anti-Loading Spinner)
- Never show a full-screen `CircularProgressIndicator` on an empty screen.
- Always use Skeleton screens with a subtle shimmer effect that mirrors the target layout (`SkeletonBox`, `SkeletonCard`, `SkeletonDashboard`).
- Use pure Jetpack Compose `Modifier.shimmerEffect()` based on `rememberInfiniteTransition` and `Brush.linearGradient`.
- Reserve spinners only for inline action buttons or small top-bar indicators.

## 2. Concurrency, Mutex & Hardware Resilience (Anti-Deadlock)
- When communicating with embedded devices, routers, or single-session hardware:
  - Guard login and session requests with `kotlinx.coroutines.sync.Mutex` (`authMutex.withLock`) to prevent session thrashing.
  - Never call a method that acquires a `Semaphore` permit from inside a block that already holds that permit (avoids deadlock).
  - Pre-authenticate before launching parallel `async` coroutines.

## 3. Zero Dummy Data Policy
- Never leave mock/dummy data in production screens.
- Use actual device/API endpoints, reverse-engineered payloads, and tolerant DTO parsers (`ignoreUnknownKeys = true`).

## 4. Professional Non-Alay Microcopy
- Use concise, direct, professional language.
- Prohibit hyperbole, overly informal slang ("kak", "bestie", "bobob cantik"), and dramatic copy.

## 5. Build & CI/CD (Anti-Hallucination)
- Never run heavy local Gradle commands (`./gradlew assembleRelease`).
- Rely on GitHub Actions CI for building signed APKs.
- Monitor workflow runs with a strict 1-minute interval: `gh run watch <RUN_ID> --interval 60`.
- Never claim or hallucinate build success without verified output from `gh run view` or GitHub APIs.

## 6. In-App Updater & Storage Hygiene
- Automatically clean up legacy APK installers before downloading new versions and upon successful launch.
- Check file existence before triggering download to avoid duplicate bandwidth usage.

## 7. Pre-Flight Syntax & Type Verification
- Run `python3 scripts/verify_kotlin_syntax.py .` before commit.
- Never call suspend functions directly in non-suspending Compose lambdas without `LaunchedEffect` or `coroutineScope.launch`.
- Never access properties directly on `kotlin.Result<T>` without `.getOrNull()` / `.getOrThrow()`.
- Ensure common Compose modifier extension imports (`Modifier.border`, `Modifier.clip`, etc.) and internal cross-package symbols are properly imported.

## 8. Release Keystore & Signing (Zero Hesitation)
- Never spin in circles or hesitate if `keytool` is missing; install it instantly: `sudo apt-get update && sudo apt-get install -y openjdk-17-jre-headless`.
- Use `python3 scripts/setup_release_keystore.py` or run `keytool -genkeypair -noprompt -dname "..."` non-interactively to populate GitHub Secrets (`KEYSTORE_BASE64`, `KEYSTORE_PASSWORD`, `KEY_ALIAS`, `KEY_PASSWORD`).
