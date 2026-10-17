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

## 5. Build & CI/CD
- Never run heavy local Gradle commands (`./gradlew assembleRelease`).
- Rely on GitHub Actions CI for building signed APKs.
- Monitor workflow runs with a 1-minute interval: `gh run watch <RUN_ID> --interval 60`.
