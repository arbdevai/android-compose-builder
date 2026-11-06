<p align="center">
  <img src="assets/banner.svg" alt="Android Compose Builder Banner" width="100%">
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" alt="License: MIT"></a>
  <a href="https://developer.android.com/jetpack/compose"><img src="https://img.shields.io/badge/Platform-Android%20%7C%20Jetpack%20Compose-3DDC84.svg?style=flat-square&logo=android&logoColor=white" alt="Platform"></a>
  <a href="https://kotlinlang.org/"><img src="https://img.shields.io/badge/Kotlin-2.0+-7F52FF.svg?style=flat-square&logo=kotlin&logoColor=white" alt="Kotlin"></a>
  <a href="#kompatibilitas-multi-cli"><img src="https://img.shields.io/badge/AI%20Agents-Antigravity%20%7C%20Claude%20%7C%20Codex-CCFF00.svg?style=flat-square&logo=google&logoColor=black" alt="AI Agents"></a>
  <a href="https://github.com/arbdevai/android-compose-builder/actions"><img src="https://img.shields.io/badge/CI%2FCD-100%25%20GitHub%20Actions-2088FF.svg?style=flat-square&logo=githubactions&logoColor=white" alt="CI/CD"></a>
</p>

---

## <img src="assets/icons/overview.svg" width="22" height="22" align="center" alt="Overview" /> Konsep Inti: Bikin APK Tanpa Build Lokal (100% Cloud CI)

**Android Compose Builder** adalah spesifikasi standar rekayasa agen (*Agent Engineering Standard*) resmi untuk merancang, membangun, dan merilis aplikasi Android modern (**Kotlin + Jetpack Compose Material 3**) **tanpa perlu kompilasi Gradle lokal**.

### Mengapa Nol Kompilasi Lokal (Zero Local Build)?
Biasanya, mengembangkan aplikasi Android membutuhkan Android Studio, Android SDK (~15-30 GB), dan proses `gradlew assembleRelease` lokal yang menguras 8-16 GB RAM serta memicu CPU throttling. Dalam lingkungan AI agent, cloud container, atau remote devbox, proses kompilasi lokal sering menyebabkan memori habis (*out of memory*) atau sesi coding macet total.

Skill ini mengubah paradigma tersebut:
1. **Mesin Lokal Murni untuk Rekayasa Kode**: AI agent dan developer fokus 100% menulis arsitektur Kotlin, Jetpack Compose UI, Coroutines, dan logika aplikasi.
2. **Pre-Flight Linter Ringan (`verify_kotlin_syntax.py`)**: Memverifikasi keseimbangan sintaks, batas coroutine suspend, memory leak, dan simbol impor secara instan di lokal dalam hitungan milidetik tanpa perlu memanggil Gradle.
3. **Pendelegasian Penuh ke GitHub Actions**: Setiap `git push` dengan pesan commit rilis otomatis memicu runner cloud GitHub Actions yang memiliki caching cepat, kompilasi headless terisolasi, penandatanganan release keystore otomatis, dan pembuatan rilis GitHub Release berisikan file APK siap unduh.

---

## <img src="assets/icons/install.svg" width="22" height="22" align="center" alt="Install" /> Instalasi Cepat (1-Line Auto-Detect)

Jalankan perintah berikut di terminal untuk memasang atau memperbarui skill ini secara otomatis:

```bash
curl -fsSL https://raw.githubusercontent.com/arbdevai/android-compose-builder/main/install.sh | bash
```

> **Mekanisme Otomatis:** Skrip installer secara cerdas memindai CLI yang terpasang di sistem (`agy`, `claude`, `codex`) dan mengaitkan symlink *live-sync* langsung ke direktori konfigurasi masing-masing agent.

---

## <img src="assets/icons/architecture.svg" width="22" height="22" align="center" alt="Architecture" /> Alur Kerja Produksi (Local Code to Cloud APK)

```text
[ LOCAL DEVBOX / AGENT ]
   │
   ├── 1. Tulis UI & Logic (Kotlin + Jetpack Compose Material 3)
   ├── 2. Validasi Pre-Flight (python3 scripts/verify_kotlin_syntax.py)
   └── 3. Git Commit ("Release v1.0.0 - Deskripsi fitur") & Git Push
            │
            ▼
[ GITHUB ACTIONS CLOUD RUNNER ]
   │
   ├── 1. Setup Headless JDK & Android SDK Cache
   ├── 2. Ekstrak Changelog Git Dinamis (generate_release_notes.py)
   ├── 3. Build Signed Production APK (gradlew assembleRelease)
   └── 4. Publish GitHub Release (Aset APK + Dynamic Release Notes)
            │
            ▼
[ SMARTPHONE PENGGUNA ]
   └── In-App Updater (OkHttp direct stream download + 4-tier APK deep validation)
```

---

## <img src="assets/icons/architecture.svg" width="22" height="22" align="center" alt="Architecture" /> 9 Standar Rekayasa Industri

Skill ini menetapkan 9 aturan ketat yang wajib dipatuhi oleh setiap AI agent:

### 1. Zero Local Gradle Build (Pendelegasian Penuh ke Cloud)
- **Larangan Keras:** Dilarang menjalankan `./gradlew build`, `./gradlew assembleDebug`, atau `./gradlew assembleRelease` di terminal lokal.
- **Standar:** Seluruh kompilasi didelegasikan ke GitHub Actions. Keberhasilan build dipantau via GitHub CLI (`gh run watch --interval 60` dan `gh release view`).

### 2. Skeleton Screen & Shimmer Native (Anti-Spinner Kosong)
- **Larangan:** Dilarang menampilkan `CircularProgressIndicator` di tengah layar kosong saat transisi data.
- **Standar:** Wajib menggunakan layout skeleton yang menyerupai bentuk konten asli dengan animasi kilau (*shimmer effect*) halus berbasis API Jetpack Compose murni (`rememberInfiniteTransition` + `Brush.linearGradient`) tanpa library pihak ketiga.
- **Modul Tersedia:** `SkeletonBox`, `SkeletonCard`, `SkeletonDashboard`, `SkeletonListItem`.

### 3. Resiliensi Konkurensi & Mutex (Anti-Deadlock Hardware/Router)
- **Otentikasi Atomik:** Seluruh siklus login atau request token ke router/hardware dilindungi dengan `Mutex.withLock` guna mencegah *session thrashing*.
- **Larangan Re-entrancy Semaphore:** Tidak boleh mengakuisisi permit `Semaphore` bersarang dari dalam blok permit yang sama demi mencegah *deadlock*.
- **Sekuensial Pre-Auth:** Token atau sesi aktif wajib diselesaikan secara berurutan sebelum memicu coroutine paralel (`async`).

### 4. Kebijakan Anti Data Dummy (Zero Dummy Data)
- **Larangan:** Dilarang menyematkan data palsu statis (*mock data*) pada layar produksi.
- **Standar:** Wajib menelusuri endpoint autentik, mendekode skema otentikasi (cookie, token, payload terenkripsi), serta memetakan model data yang toleran terhadap evolusi field (`ignoreUnknownKeys = true`).

### 5. In-App Updater Standar Industri (Anti-APK Korup & Streaming Buffer)
- **Larangan `DownloadManager`:** Dilarang mengandalkan `DownloadManager` sistem yang rentan macet saat sinyal lemah atau gagal menangani HTTP redirect GitHub CDN.
- **Direct OkHttp Streaming:** Wajib menggunakan streaming HTTP langsung dengan buffer 64 KB, timeout tangguh (30s connect, 60s read/write), dan penghitungan persentase presisi.
- **Isolasi File Sementara (`.part`):** Mengunduh ke file sementara `app-${version}-${flavor}.apk.part`. File hanya di-rename menjadi `.apk` setelah 100% byte terunduh dan lolos validasi. Jika terjadi gangguan jaringan, file `.part` langsung dihapus otomatis.
- **Validasi Integritas 4 Lapis (`isApkValid`):**
  1. Verifikasi ukuran fisik minimum (> 10 MB) dan exact match ukuran aset GitHub.
  2. Deep archive & DEX parsing melalui `getPackageArchiveInfo(..., GET_SIGNING_CERTIFICATES or GET_ACTIVITIES)`.
  3. Strict package name & flavor matching (`pkg.packageName == context.packageName`).
  4. Monotonic version code progression (`pkg.longVersionCode > BuildConfig.VERSION_CODE`).
- **Pembersihan Otomatis Storage:** Hapus seluruh file installer APK usang dari direktori unduhan sebelum mengunduh rilis baru atau setelah pembaruan sukses dipasang.

### 6. Formula Monotonik SemVer & Otomasi Rilis Bebas Emoji
- **Formula Monotonik `versionCode`:**
  $$\text{versionCode} = \text{MAJOR} \times 10000 + \text{MINOR} \times 100 + \text{PATCH}$$
- **Zero-Emoji Policy:** Dilarang menyematkan emoji dekoratif pada catatan rilis, changelog, dan dialog update dalam aplikasi (mengacu pada standar teknis resmi AOSP / Linux Kernel).
- **Zero-Hardcoded Changelog:** Seluruh poin catatan rilis diekstrak secara dinamis 100% dari commit git riil melalui skrip `.github/scripts/generate_release_notes.py`.
- **Rilis Satu Siklus:** Rilis dipicu otomatis via pesan commit `Release v...` tanpa manual tagging lokal.

### 7. Pre-Flight Linter & Deteksi Kebocoran Memori (Zero-CI-Failure)
- Skrip mandiri `verify_kotlin_syntax.py` wajib dijalankan sebelum setiap git commit:
  - Validasi pre-flight kelengkapan `gradlew`, `gradle/wrapper/`, `gradle.properties` (`android.useAndroidX=true` & `ksp.useKSP2=false`), serta isolasi `.gitignore` pada folder `scripts/` agar skrip chroot tidak bocor ke repositori aplikasi.
  - Validasi keseimbangan tanda kurung dan blok kode dengan string parsing yang sadar escape literal.
  - Deteksi pemanggilan fungsi `suspend` di dalam lambda Compose non-suspending.
  - Deteksi fungsi `@Dao` `suspend` dengan `@Query("DELETE ...")` atau `@Query("UPDATE ...")` yang tidak mendeklarasikan tipe kembalian `: Int` (mencegah crash KSP2 `unexpected jvm signature V`).
  - Validasi pembongkaran anggota `kotlin.Result<T>`.
  - Pengecekan impor ekstensi modifier (`Modifier.border`, `Modifier.clip`, dsb.).
  - Kewajiban blok `onDispose { ... }` pada seluruh `DisposableEffect`.
  - Advisory peringatan memori non-blocking (`collectAsStateWithLifecycle`, leak `Context`, deteksi `GlobalScope`).
  - Dukungan non-blind suppression (`// @validator-ignore`, `// @validator-ignore-file`, `@Suppress`).

### 8. Otomasi Keystore & Signing CI (Anti-Muter-Muter)
- Skrip `setup_release_keystore.py` mendeteksi dan menginstal `keytool` otomatis jika belum ada (`openjdk-17-jre-headless`).
- Pembuatan release keystore non-interaktif, konversi Base64 instan, dan konfigurasi 4 secrets signing ke GitHub repository (`KEYSTORE_BASE64`, `KEYSTORE_PASSWORD`, `KEY_ALIAS`, `KEY_PASSWORD`) dalam hitungan detik.

### 9. Paten Bebas "AI Slop" pada Ikon & UI
- Dilarang keras menggunakan gambar hasil generasi AI 3D hiperbolis yang pecah atau tidak simetris.
- Wajib menggunakan Android Adaptive Vector Icons (XML SVG bersih pada canvas 108x108 dp dengan safe zone 66 dp).
- Generator raster PNG terintegrasi (`mdpi` hingga `xxxhdpi`) berbasis Python zlib murni tanpa dependensi library eksternal.

---

## <img src="assets/icons/compatibility.svg" width="22" height="22" align="center" alt="Compatibility" /> Kompatibilitas Multi-CLI

Skill ini mematuhi **Agent Skills Standard** dan kompatibel langsung di berbagai platform AI agent:

| Agent / LLM CLI | Status | Lokasi Integrasi |
| :--- | :---: | :--- |
| **Antigravity CLI (`agy`)** | Native | `~/.gemini/config/skills/android-compose-builder/` |
| **Claude Code (`claude`)** | Native | `~/.claude/skills/android-compose-builder/` |
| **OpenAI Codex CLI (`codex`)** | Native | `~/.codex/skills/android-compose-builder/` |
| **Cursor / Copilot / Windsurf** | Native | Aturan universal via [AGENTS.md](AGENTS.md) & [GEMINI.md](GEMINI.md) |

---

## <img src="assets/icons/tools.svg" width="22" height="22" align="center" alt="Tools" /> Tooling & Skrip Otomasi

### 1. Inisiasi Proyek Compose Baru Lengkap dengan GitHub Actions CI
Untuk membuat repositori aplikasi Android Jetpack Compose baru yang sudah terkonfigurasi workflow build APK cloud:

```bash
python3 scripts/init_compose_project.py /path/ke/proyek/baru com.example.myapp "My Application"
```

### 2. Setup Keystore & GitHub Secrets dalam 1 Langkah
Membuat file keystore produksi lokal dan otomatis mengunggah 4 rahasia signing ke repositori GitHub via `gh secret set`:

```bash
python3 scripts/setup_release_keystore.py
```

### 3. Verifikasi Pre-Flight Linter Sebelum Commit
Memeriksa keseimbangan kurung, pemanggilan suspend, dan potensi memory leak:

```bash
python3 scripts/verify_kotlin_syntax.py
```

### 4. Pembuatan Ikon Adaptif Android (Vector & PNG Mipmap)
Menghasilkan aset XML Adaptive Icon dan raster PNG siap pakai tanpa library eksternal:

```bash
python3 scripts/generate_launcher_icons.py --package com.example.myapp --color "#00E676"
```

---

## <img src="assets/icons/advanced.svg" width="22" height="22" align="center" alt="Advanced" /> Pilihan Instalasi Lanjutan

### Instalasi Khusus Lingkungan
```bash
./install.sh --antigravity       # Pasang khusus Antigravity CLI (agy)
./install.sh --claude            # Pasang khusus Claude Code CLI
./install.sh --codex             # Pasang khusus Codex CLI
./install.sh --all               # Pasang ke semua CLI yang tersedia
```

### Pembatasan Per-Proyek (*Workspace Scope*)
```bash
cd /path/ke/proyek/android
/path/ke/android-compose-builder/install.sh --workspace
```

### Pembaruan Otomatis di Background
Aktifkan sinkronisasi otomatis agar definisi skill selalu mutakhir setiap terminal dibuka:

```bash
./install.sh --auto-update       # Mengaktifkan background hook di profil shell
./install.sh --update            # Melakukan update instan ke commit GitHub terbaru
./install.sh --disable-auto-update
```

---

## <img src="assets/icons/structure.svg" width="22" height="22" align="center" alt="Structure" /> Struktur Repositori

```text
android-compose-builder/
├── assets/
│   ├── banner.svg                   # Banner arsitektur resmi (Matte Charcoal x Lime Neon)
│   ├── gradle/                      # Bundel standar gradlew & gradle-wrapper (8.9)
│   └── icons/                       # Paket ikon visual SVG vektor mandiri (Bebas Emoji)
├── scripts/
│   ├── init_compose_project.py      # Generator proyek Jetpack Compose + CI workflow
│   ├── setup_release_keystore.py    # Otomasi keystore & upload GitHub secrets signing
│   ├── generate_launcher_icons.py   # Generator Adaptive Vector XML & PNG Mipmap
│   └── verify_kotlin_syntax.py      # Pre-flight linter sintaks & anti-memory-leak
├── SKILL.md                         # Spesifikasi detail instruksi & implementasi skill
├── AGENTS.md                        # Aturan standar universal AI coding agents
├── GEMINI.md                        # Instruksi khusus Gemini & Google Antigravity
├── CLAUDE.md                        # Instruksi konfigurasi Claude Code CLI
├── CODEX.md                         # Instruksi konfigurasi OpenAI Codex CLI
├── install.sh                       # Installer otomatis multi-CLI berbasis Bash
├── install.py                       # Installer alternatif mandiri berbasis Python
├── LICENSE                          # Lisensi resmi MIT
└── README.md                        # Dokumentasi teknis proyek
```

---

## <img src="assets/icons/license.svg" width="22" height="22" align="center" alt="License" /> Lisensi

Repositori ini dilisensikan di bawah lisensi terbuka [MIT](LICENSE). Bebas digunakan, diintegrasikan, dan disesuaikan untuk proyek komersial maupun open-source.
