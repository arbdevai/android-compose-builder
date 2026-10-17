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
5. **No Local Gradle Heavy Builds:**
   - Delegate building and release signing to GitHub Actions CI (`gh run watch --interval 60`).
