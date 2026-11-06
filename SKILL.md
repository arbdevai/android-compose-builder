---
name: android-compose-builder
description: >-
  Expert Android developer skill for building Kotlin + Jetpack Compose applications
  with support for C/C++ NDK and Rust native layers. Optimized for resource-constrained
  mobile chroot environments, strict zero-dummy-data, anti-AI-slop design, skeleton shimmer,
  resilient concurrency, GitHub Actions CI/CD compilation, and direct in-app updating.
---

# Android Compose Builder Skill

Skill arsitektur dan pengembangan aplikasi Android modern berbasis Jetpack Compose, didukung integrasi native (C/C++ NDK dan Rust). Dirancang khusus untuk efisiensi tinggi pada lingkungan **chroot perangkat mobile (ARM)**, dengan pendelegasian kompilasi penuh ke GitHub Actions CI.

---

## 1. Aturan Emas Operasional (Golden Rules)

### A. Alur Kerja Chroot HP: Zero Local Build & Smart Push
- **DILARANG BUILD GRADLE LOKAL:** Jangan pernah menjalankan perintah `./gradlew` (seperti `assembleRelease`, `compileDebugKotlin`) di dalam chroot lokal. Kompilasi lokal akan membebani RAM/CPU HP dan memicu OOM-kill.
- **DILARANG PUSH SETENGAH JALAN:** Jangan melakukan `git push` untuk setiap perbaikan 1–2 baris. Push hanya dilakukan ketika satu rangkaian fitur telah **selesai secara tuntas** dan lolos verifikasi sintaksis lokal.
- **Pendelegasian Penuh ke GitHub Actions:** Seluruh proses build binary APK, packaging, dan signing diserahkan ke cloud runner GitHub Actions.

### B. Anti-Fitur Setengah Jadi (Tuntas Hulur ke Hilir)
- **DILARANG MENYISAKAN STUB / TODO:** Dilarang keras meninggalkan komentar `// TODO`, fungsi tanpa implementasi, atau mock kosong.
- **Implementasi Vertikal Penuh:** Setiap fitur yang diminta wajib diselesaikan tuntas dari lapisan data (DTO/Repository), State Management (ViewModel & `StateFlow`), hingga antarmuka (Jetpack Compose Screen) sebelum pekerjaan dinyatakan selesai.
- **Jangan Loncat-Loncat:** Tuntaskan fitur yang sedang dikerjakan sebelum berpindah ke fitur berikutnya.

### C. Anti-AI Slop & Kebijakan Bebas Emoji (Zero Emoji)
- **NOL ELEMEN DEKORASI NORAK:** Dilarang menambahkan animasi dekoratif tanpa fungsi nyata, seperti titik hijau berkedip/berdenyut (*pulsing green dot* / `animate-pulse`), efek glow berlebihan, atau teks berjalan (*marquee*).
- **NOL EMOJI DEKORATIF:** Dilarang menggunakan emoji (seperti 🚀, ✨, 📦, 🛠️, 🎉) di dalam antarmuka UI, teks tombol, judul, release notes, maupun pesan commit Git.
- **Wajib Ikon Vektor Resmi:** Gunakan selalu Vector Icon dari `androidx.compose.material:material-icons-extended` atau XML Vector Drawable di `res/drawable/`.

### D. Kebijakan Anti Data Dummy (Zero Dummy Data)
- **Dilarang Data Bohongan di UI:** Jangan pernah menampilkan data statis buatan sendiri pada layar produksi.
- **Wajib Skeleton Screen Shimmer:** Saat data masih dimuat dari jaringan atau hardware, tampilkan **Skeleton Screen** dengan animasi shimmer yang meniru struktur tata letak asli, **BUKAN** spinner loading layar penuh.

### E. Gaya Bahasa & Komunikasi (Teknis, Ringkas, Anti-Alay)
- Komunikasi dan teks antarmuka (*microcopy*) wajib **lugas, to-the-point, sedikit teknis, dan bebas basa-basi**. Dilarang menggunakan gaya bahasa sok akrab, manja, hiperbolis, atau khas customer-service template.

### F. Verifikasi Sintaksis Pre-Flight (Wajib Sebelum Push)
- Sebelum melakukan commit dan push, wajib menjalankan validator lokal berbasis Python:
  ```bash
  python3 scripts/verify_kotlin_syntax.py .
  ```
- Pastikan menghasilkan **0 Hard Errors** sebelum memicu workflow CI. Jika terdapat error, AI wajib melakukan *self-healing* secara otomatis sebelum melangkah ke proses staging/commit.

### G. Protokol Memori Persisten & Wawancara PRD (Anti-Amnesia)
- **DILARANG MENGANDALKAN MEMORI CHAT:** Seluruh kesepakatan desain, status pekerjaan, dan catatan bug wajib dicatat di disk dalam folder `docs/` (`docs/PRD.md` dan `docs/STATE.md`).
- **Bootstrap Sesi Baru:** Di setiap sesi baru atau pergantian konteks, AI **WAJIB** membaca `docs/PRD.md` dan `docs/STATE.md` terlebih dahulu untuk mencegah amnesia dan menghindari pengulangan bug lama.
- **Wawancara PRD di Awal:** Jika `docs/PRD.md` belum ada, AI **DILARANG** langsung menulis kode. AI wajib menyajikan kuesioner terstruktur dengan opsi ganda (Domain, Native Layer, Persistence, UI Theme) kepada pengguna, lalu menyusun dokumen PRD secara otomatis.
- **Scaffolding Tata Letak Terstruktur:** Selalu terapkan pola `Scaffold` + `contentWindowInsets` + `.padding(innerPadding)` + `.imePadding()` untuk mencegah UI berantakan atau tertutup keyboard virtual.

---

## 2. Matriks Modul Referensi Mendalam (On-Demand References)

Saat menangani alur kerja spesifik, AI wajib membaca dokumen panduan teknis terkait di folder `references/`:

| Kategori Fitur | Lokasi Referensi | Isi Panduan Utama |
| :--- | :--- | :--- |
| **Agentic Lifecycle & State Sesi** | `references/agentic_lifecycle.md` | Protokol anti-amnesia, mitigasi context fatigue, kuesioner PRD interaktif, layout scaffolding anti-berantakan, dan self-healing loop. |
| **Native Layer (C/C++ & Rust)** | `references/ndk_and_rust.md` | Konfigurasi CMake NDK, ABI filters (`arm64-v8a`), JNI memory safety, dan toolchain Rust via `cargo-ndk` / UniFFI. |
| **Sistem UI/UX & Shimmer** | `references/ui_ux_system.md` | `Modifier.shimmerEffect()`, keyboard handling (`imePadding`), `AnimatedContent`, `BackHandler`, dan kamus microcopy profesional. |
| **In-App Updater & APK Validation** | `references/in_app_updater.md` | Direct OkHttp streaming, isolasi file `.part`, verifikasi 4-lapis `isApkValid`, dan SemVer numerik. |
| **CI/CD, SemVer & Keystore** | `references/ci_cd_pipeline.md` | GitHub Actions workflow, canonical `versionCode`, ekstraksi changelog dinamis dari git, dan signing keystore otomatis. |
| **Hardware, IoT & Local Network** | `references/hardware_and_iot.md` | Otentikasi atomik `Mutex`, pembatasan rate limit `Semaphore` (anti-deadlock), JSON parser toleran, dan printer termal POS. |

---

## 3. Tooling Skrip Pembantu di Chroot (`scripts/`)

Gunakan skrip Python yang telah tersedia untuk operasi instan tanpa membebani resource lokal:

- **Verifikasi Sintaks:**
  `python3 scripts/verify_kotlin_syntax.py .`
  (Mengecek kurung kurawal, XML well-formedness, boundary coroutine suspend, unhandled Result extraction, dan import Compose).
- **Inisiasi Proyek Baru (1-Click):**
  `python3 scripts/init_compose_project.py --name "AppName" --package "com.company.app"`
  (Membuat struktur folder lengkap, build files, dan workflow CI siap pakai).
- **Setup Release Keystore & GitHub Secrets:**
  `python3 scripts/setup_release_keystore.py`
  (Membuat keystore RSA 2048-bit dan mengunggah 4 GitHub Secrets dalam satu langkah).
- **Generate Launcher Icons (Vector to PNG):**
  `python3 scripts/generate_launcher_icons.py app/src/main/res`
  (Merender seluruh densitas mipmap Android secara otomatis).
