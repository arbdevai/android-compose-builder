# Claude Code Guidelines: Android Jetpack Compose Development

When working on Android projects with this repository or when the `android-compose-builder` skill is activated, you must strictly follow these rules:

## 1. Zero Half-Baked Features (Tuntas Hulu ke Hilir)
- Dilarang keras meninggalkan stub `// TODO`, fungsi tanpa isi, atau UI tanpa koneksi ke ViewModel/Repository.
- Selesaikan fitur secara vertikal penuh (DTO/Data -> ViewModel -> Compose Screen) sebelum menganggap tugas selesai.

## 2. Zero AI Slop & Kebijakan Bebas Emoji (Zero Emoji)
- Dilarang elemen dekorasi norak: no pulsing green dots (`animate-pulse`), no glowing borders, no marquee.
- Dilarang menggunakan emoji dekoratif di UI, teks string, maupun commit message.
- Wajib menggunakan Vector Icon resmi Material3 (`androidx.compose.material:material-icons-extended`) atau XML Vector Drawable.

## 3. Lingkungan Chroot HP & CI/CD Hygiene
- Zero local Gradle compilation (`./gradlew assembleRelease`); serahkan kompilasi biner ke GitHub Actions.
- Dilarang melakukan micro-push per 1-2 baris edit. Push hanya dilakukan ketika satu set fitur tuntas dan lolos verifikasi sintaksis lokal.
- Pantau CI dengan interval tepat 60 detik (`gh run watch <RUN_ID> --interval 60`).
- Zero status halusinasi tanpa bukti riil output perintah `gh run view`.

## 4. Dukungan Multi-Medan & Native (C/C++ NDK & Rust)
- Dukungan penuh untuk komputasi berat, audio low-latency, crypto, dan native engines melalui panduan di `references/ndk_and_rust.md`.

## 5. UI & Skeleton Screens (Anti-Loading Spinner)
- Never show a full-screen `CircularProgressIndicator` on an empty screen.
- Always use Skeleton screens with a subtle shimmer effect that mirrors the target layout (`SkeletonBox`, `SkeletonCard`, `SkeletonDashboard`).
- Use pure Jetpack Compose `Modifier.shimmerEffect()`.

## 6. Concurrency, Mutex & Hardware Resilience (Anti-Deadlock)
- Guard login and session requests with `Mutex.withLock`.
- Never call a method that acquires a `Semaphore` permit from inside a block that already holds that permit (avoids deadlock).
- Pre-authenticate before launching parallel `async` coroutines.

## 7. Zero Dummy Data & Clean Tone
- Never leave mock/dummy data in production screens. Use tolerant DTO parsers (`ignoreUnknownKeys = true`).
- Use concise, direct, professional language. Prohibit hyperbole, overly informal slang, and dramatic copy.

## 8. In-App Updater & Storage Hygiene
- Stream directly via OkHttp to `.part` file; perform 4-layer `isApkValid` check before renaming to `.apk`.
- Clean up legacy APK installers before downloading new versions.

## 9. Pre-Flight Syntax Verification
- Run `python3 scripts/verify_kotlin_syntax.py .` before commit/push. Must produce 0 hard errors.
- Never call suspend functions directly in non-suspending Compose lambdas without `LaunchedEffect` or `coroutineScope.launch`.
- Never access properties directly on `kotlin.Result<T>` without `.getOrNull()` / `.getOrThrow()`.

## 10. Release Keystore & Signing (Zero Hesitation)
- Never spin in circles or hesitate if `keytool` is missing; install it instantly: `sudo apt-get update && sudo apt-get install -y openjdk-17-jre-headless`.
- Use `python3 scripts/setup_release_keystore.py` or run `keytool -genkeypair -noprompt -dname "..."` non-interactively to populate GitHub Secrets.

## 11. Living Session Memory (Anti-Amnesia Sesi Baru)
- Seluruh keputusan arsitektur, status tugas, dan riwayat bug wajib disimpan persisten di `docs/PRD.md` dan `docs/STATE.md`.
- Di setiap sesi baru atau giliran kerja, AI wajib membaca kedua file tersebut terlebih dahulu sebelum bertindak.

## 12. Wawancara PRD & Scaffolding Tata Letak Anti-Berantakan
- Jika `docs/PRD.md` belum ada, dilarang langsung menulis kode; sajikan kuesioner terstruktur dengan opsi pilihan ganda ke user.
- Tata letak Compose wajib mengikuti pola hierarkis: `Scaffold` + `contentWindowInsets` + `.padding(innerPadding)` + `.imePadding()` untuk mencegah UI berantakan atau tertutup keyboard.
