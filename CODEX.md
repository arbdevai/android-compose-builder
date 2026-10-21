# Codex CLI Instructions: Android Jetpack Compose Development

This project and skill adhere to the `android-compose-builder` standard for high-performance Kotlin + Jetpack Compose development.

### Core Standards
1. **Skeleton Screen over Spinner:**
   - Use `Modifier.shimmerEffect()` and skeleton placeholders (`SkeletonBox`, `SkeletonCard`, `SkeletonDashboard`) instead of full-screen loading spinners.
2. **Mutex & Anti-Deadlock Concurrency:**
   - Protect hardware/router authentication with `Mutex.withLock`.
   - Never acquire nested `Semaphore` permits within the same coroutine scope to eliminate deadlocks.
   - Sequential pre-authentication before parallel `async` operations.
3. **Robust Networking:**
   - Single OkHttpClient with timeouts >= 30s.
   - Fallback on HTML responses (502/503 Cloudflare/Nginx maintenance screens) to prevent `SerializationException`.
   - Result<T> return type in repository layer.
4. **Professional UI Microcopy:**
   - Clear, clean, professional tone. No AI boilerplate or exaggerated filler text.
5. **No Local Gradle Heavy Builds & Truthful Status:**
   - Delegate building and release signing to GitHub Actions CI (`gh run watch --interval 60`).
   - Never report unverified or hallucinated build/release statuses.
6. **In-App Updater Storage Hygiene:**
   - Auto-clean legacy APK installers from download directories to preserve user storage.
7. **Pre-Flight Linter (Zero-CI-Failure):**
   - Run `verify_kotlin_syntax.py` before commit to validate coroutine boundaries, `Result<T>` unpacking, modifier imports, and cross-package symbol imports.
8. **Release Keystore & Signing (Anti-Muter-Muter):**
   - Install `keytool` immediately via `sudo apt update && sudo apt install -y openjdk-17-jre-headless` if missing.
   - Use `setup_release_keystore.py` to auto-generate non-interactive keystore and configure GitHub Secrets.
