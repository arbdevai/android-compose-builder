# Universal Agent Guidelines: Android Jetpack Compose Builder

This repository contains the `android-compose-builder` agent skill.
All AI coding agents (Antigravity CLI, Claude Code, Codex CLI, Cursor, Copilot) operating in this repository or utilizing this skill must adhere to the rules defined in `SKILL.md`:

1. **Zero Half-Baked Features (Tuntas Hulu ke Hilir)**:
   - Dilarang keras meninggalkan stub `// TODO`, fungsi tanpa isi, atau UI tanpa koneksi ke ViewModel/Repository.
   - Selesaikan fitur secara vertikal penuh (DTO/Data -> ViewModel -> Compose Screen) sebelum menganggap tugas selesai.
2. **Zero AI Slop & Kebijakan Bebas Emoji (Zero Emoji)**:
   - Dilarang elemen dekorasi norak: no pulsing green dots (`animate-pulse`), no glowing borders, no marquee.
   - Dilarang menggunakan emoji dekoratif di UI, teks string, maupun commit message.
   - Wajib menggunakan Vector Icon resmi Material3 (`androidx.compose.material:material-icons-extended`) atau XML Vector Drawable.
   - **Anti-Pola "Tailwind / SaaS Tint Slop" (Larangan Hitam Kebiruan & Tint Transparan):**
     - Dilarang keras memakai warna hitam kebiruan/navy gelap (`#0F172A`, `#111622`, `#1E2638`) untuk dark mode aplikasi maupun background icon APK. Wajib gunakan warna hitam/abu-abu netral sejati (R=G=B) seperti `#000000` (True OLED) atau `#121212` (Material Dark).
     - Dilarang membuat kotak status/alert dengan background warna hijau/merah transparan bergaya glassmorphism sirup (`Color(0xFF10B981).copy(alpha = 0.12f)` + border hijau transparan). Gunakan kontainer solid Material 3 standar (`surfaceVariant`), tandai status hanya dengan teks atau dot/ikon kecil yang proporsional.
     - Latar belakang launcher icon (Icon APK) wajib solid murni tanpa saturasi warna tersembunyi.
3. **Lingkungan Chroot HP & CI/CD Hygiene**:
   - Zero local Gradle compilation (`./gradlew assembleRelease`); serahkan kompilasi biner ke GitHub Actions.
   - Dilarang melakukan micro-push per 1-2 baris edit. Push hanya dilakukan ketika satu set fitur tuntas dan lolos verifikasi sintaksis lokal.
   - Pantau CI dengan interval tepat 60 detik (`gh run watch <RUN_ID> --interval 60`).
   - Zero status halusinasi tanpa bukti riil output perintah `gh run view`.
4. **Dukungan Multi-Medan & Native (C/C++ NDK & Rust)**:
   - Dukungan penuh untuk komputasi berat, audio low-latency, crypto, dan native engines melalui panduan di `references/ndk_and_rust.md`.
5. **Zero Dummy Data**: Selalu targetkan data/API riil atau local persistence. Gunakan Skeleton Screens ber-shimmer untuk status loading.
6. **Resilient Concurrency**:
   - Otentikasi atomik menggunakan `Mutex.withLock`.
   - Anti-deadlock: nol pemanggilan nested permit pada `Semaphore`.
   - Pre-auth sekuensial sebelum worker async paralel.
7. **Clean Tone & Microcopy**: Bahasa teknis, lugas, to-the-point, tanpa basa-basi, anti-alay.
8. **Pre-Flight Verification Kontekstual (Anti-Ritual Robotik)**:
   - Eksekusi `python3 scripts/verify_kotlin_syntax.py .` **hanya jika** ada modifikasi file Kotlin (`.kt`) atau layout Android (`.xml`).
   - Jangan jalankan verifikasi Kotlin jika commit hanya mengubah aset web (`web/`), dokumen (`.md`), atau skrip konfigurasi.
   - Wajib 0 hard error sebelum commit/push jika file Kotlin disentuh.
9. **Release Keystore & Signing (Anti-Muter-Muter)**:
   - Jika `keytool` tidak ada, install langsung tanpa ragu (`sudo apt update && sudo apt install -y openjdk-17-jre-headless`).
   - Gunakan `python3 scripts/setup_release_keystore.py` untuk mengunggah 4 GitHub Secrets secara otomatis.
10. **Living Session Memory (Anti-Amnesia Sesi Baru)**:
    - Seluruh keputusan arsitektur, status tugas, dan riwayat bug wajib disimpan persisten di `docs/PRD.md` dan `docs/STATE.md`.
    - Di setiap sesi baru atau giliran kerja, AI wajib membaca kedua file tersebut terlebih dahulu sebelum bertindak.
11. **Wawancara PRD & Scaffolding Tata Letak Anti-Berantakan**:
    - Jika `docs/PRD.md` belum ada, dilarang langsung menulis kode; sajikan kuesioner terstruktur dengan opsi pilihan ganda ke user.
    - Tata letak Compose wajib mengikuti pola hierarkis: `Scaffold` + `contentWindowInsets` + `.padding(innerPadding)` + `.imePadding()` untuk mencegah UI berantakan atau tertutup keyboard.
12. **Gradle Wrapper, Properties, Room KSP2 & Anti-Leak `scripts/`**:
    - Setiap repositori aplikasi wajib memiliki `gradlew`, `gradle/wrapper/`, dan `gradle.properties` (`android.useAndroidX=true` dan `ksp.useKSP2=false`) sebelum push pertama ke CI.
    - Fungsi `suspend` di dalam `@Dao` Room yang menggunakan `@Query("DELETE ...")` atau `@Query("UPDATE ...")` wajib mendeklarasikan tipe kembalian `: Int` (bukan `Unit`) agar tidak memicu crash KSP2 (`unexpected jvm signature V`).
    - Direktori `scripts/` di workspace aplikasi wajib dimasukkan ke `.gitignore` (atau dijalankan langsung dari path skill) dan dilarang keras ikut ter-commit ke repositori Git aplikasi.
