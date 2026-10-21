# Android Compose Builder Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Android%20%7C%20Jetpack%20Compose-green.svg)](https://developer.android.com/jetpack/compose)
[![AI Agents](https://img.shields.io/badge/AI%20Agents-Antigravity%20%7C%20Claude%20%7C%20Codex-purple.svg)](#multi-cli-compatibility)

**Expert Android Developer Skill & Agent Standard** untuk membangun aplikasi Android modern berbasis Kotlin + Jetpack Compose Material3. Dirancang khusus untuk asisten AI coding (Antigravity CLI, Claude Code, OpenAI Codex CLI, Cursor, Copilot) agar dapat merancang, mengembangkan, dan memelihara aplikasi kelas produksi secara mandiri, tuntas, dan berstandar industri tinggi.

---

## ⚡ 1-Line Quick Install (Auto-Detect)

Jika Anda ingin menginstal atau mengembalikan skill ini ke sistem lokal secara instan:

```bash
curl -fsSL https://raw.githubusercontent.com/arbdevai/android-compose-builder/main/install.sh | bash
```

> **Catatan:** Skrip installer otomatis mendeteksi CLI yang terpasang di sistem (`agy`, `claude`, `codex`, atau direktori konfigurasinya) dan langsung mengaktifkan skill untuk semua tool yang ditemukan.

---

## 🌟 Fitur Utama & Standar Rekayasa

1. **Standar Skeleton Screen & Anti-Loading Spinner**:
   - Dilarang menggunakan full-screen `CircularProgressIndicator` di layar kosong.
   - Wajib menggunakan Skeleton Screen dengan animasi kilau halus (*shimmer effect*) berbasis murni Jetpack Compose (`rememberInfiniteTransition` + `Brush.linearGradient`) tanpa dependensi pihak ketiga berat.
   - Komponen modular siap pakai: `SkeletonBox`, `SkeletonCard`, `SkeletonDashboard`, `SkeletonListItem`.

2. **Resiliensi Konkurensi & Mutex (Anti-Deadlock pada Hardware/Router)**:
   - **Otentikasi Atomik**: Melindungi proses otentikasi/login perangkat keras atau router dengan `Mutex.withLock` untuk mencegah tabrakan sesi (*session thrashing*).
   - **Larangan Re-entrancy Semaphore**: Melarang pemanggilan bersarang yang mengakuisisi permit `Semaphore` dari dalam blok permit yang sama demi mencegah kebuntuan total (*deadlock*).
   - **Pre-Authentication**: Mewajibkan token aktif diselesaikan secara sekuensial sebelum memicu coroutine paralel (`async`).

3. **Kebijakan Anti Data Dummy (Zero Dummy Data)**:
   - Dilarang membiarkan data tiruan statis/palsu di layar produksi.
   - Wajib menelusuri endpoint riil, mendekode skema otentikasi (enkripsi, token, cookie), dan memetakan model DTO yang toleran (`ignoreUnknownKeys = true`).

4. **Standar Gaya Bahasa Profesional (Anti-Alay)**:
   - Bebas dari bahasa berlebihan, mendramatisir, hiperbolis, atau template sok asik khas AI generik.
   - Microcopy lugas, profesional, ringkas, dan to-the-point.

5. **Paten Bebas "AI Slop" pada Ikon & Grafis**:
   - Dilarang menyematkan gambar render 3D hiperbolis yang tidak proporsional.
   - Wajib Android Adaptive Vector Icons (XML SVG bersih pada canvas safe zone).
   - Dilengkapi generator raster PNG otomatis (`mdpi` hingga `xxxhdpi`) berbasis pure Python zlib (tanpa Pillow / library eksternal).

6. **CI/CD GitHub Actions & Anti-Boncos API**:
   - Dilarang menjalankan proses kompilasi gradle berat di mesin lokal.
   - Pendelegasian penuh ke GitHub Actions CI untuk build signed APK.
   - Pemantauan build wajib dengan interval minimal 60 detik (`gh run watch --interval 60`) untuk melindungi kuota GitHub API.
   - Anti-halusinasi status CI: dilarang mengklaim rilis sukses tanpa bukti verifikasi resmi dari `gh run view` / `gh release view`.

7. **In-App Updater & Storage Hygiene**:
   - Pembersihan otomatis file installer APK lama di folder unduhan (`downloadDir`) sebelum mengunduh rilis baru atau setelah instalasi pembaruan berhasil.
   - Proteksi anti double-download untuk menghemat kuota pengguna.

8. **Pre-Flight Linter (Zero-CI-Failure)**:
   - Skrip linter mandiri `verify_kotlin_syntax.py` untuk mendeteksi potensi error CI sebelum commit:
     - Keseimbangan tanda kurung kurawal/bracket dengan pemahaman literal string dan komentar.
     - Deteksi panggilan suspend function ilegal pada non-suspending Compose lambdas.
     - Validasi pembongkaran anggota `kotlin.Result<T>`.
     - Validasi impor ekstensi Modifier Compose (`Modifier.border`, `Modifier.clip`, dsb.).
     - Validasi resolusi referensi class internal antar-package.

9. **1-Click Starter Kit & Instant Keystore Setup**:
   - Skrip otomasi `init_compose_project.py` untuk menginisiasi repositori baru lengkap dengan Material3, Navigation, ViewModel, Network Client, CI workflow, dan template Skeleton Screen.
   - Skrip `setup_release_keystore.py` (anti-muter-muter): otomatis mendeteksi/menginstall `keytool` (`openjdk-17-jre-headless`), membuat release keystore non-interaktif, meng-encode Base64, dan mengunggah 4 rahasia signing ke GitHub Secrets dalam 3 detik.

---

## 🤖 Multi-CLI Compatibility

Skill ini mengadopsi spesifikasi terbuka **Agent Skills Standard** dan kompatibel langsung dengan ekosistem agent:

| AI Agent / CLI | Status | Mekanisme Integrasi |
| :--- | :---: | :--- |
| **Antigravity CLI (`agy`)** | ✅ Native | `~/.gemini/config/skills/android-compose-builder/` atau `.agents/skills/` |
| **Claude Code (`claude`)** | ✅ Native | `~/.claude/skills/android-compose-builder/` dan `CLAUDE.md` adapter |
| **Codex CLI (`codex`)** | ✅ Native | `~/.codex/skills/android-compose-builder/` dan `CODEX.md` adapter |
| **Cursor / Copilot / Windsurf** | ✅ Native | `AGENTS.md` & `GEMINI.md` universal prompt rules |

---

## 🛠️ Opsi Instalasi Manual

Clone repositori ini:

```bash
git clone https://github.com/arbdevai/android-compose-builder.git
cd android-compose-builder
```

### 1. Auto-Detect (Rekomendasi)
Mendeteksi CLI yang aktif di mesin Anda dan memasang skill secara otomatis:
```bash
./install.sh
```

### 2. Pasang ke Semua CLI Sekaligus
```bash
./install.sh --all
```

### 3. Pasang Khusus Per CLI
```bash
./install.sh --antigravity   # Khusus Antigravity CLI (agy)
./install.sh --claude        # Khusus Claude Code CLI
./install.sh --codex         # Khusus OpenAI Codex CLI
```

### 4. Pasang ke Workspace / Project Tertentu
Jika ingin membatasi skill hanya pada direktori project aktif Anda:
```bash
cd /path/ke/proyek/android/anda
/path/ke/android-compose-builder/install.sh --workspace
```

### 5. Cek Status & Deteksi
```bash
./install.sh --check
```

### 6. Auto-Update di Background (Mirip Skill Resmi)
Aktifkan sinkronisasi otomatis agar skill selalu ter-update di background setiap terminal dibuka:
```bash
./install.sh --auto-update       # Mengaktifkan background auto-update hook di shell profile
./install.sh --disable-auto-update # Menonaktifkan auto-update hook
./install.sh --update            # Melakukan update instan ke commit GitHub terbaru
```

### 7. Uninstall
```bash
./install.sh --uninstall
```

### 8. Pengguna Windows / Tanpa Bash
Gunakan installer Python mandiri:
```bash
python3 install.py
python3 install.py --all
python3 install.py --workspace
python3 install.py --auto-update
python3 install.py --update
```

---

## 📂 Struktur Repositori

```text
android-compose-builder/
├── SKILL.md                  # Spesifikasi inti skill (Agent Skills Standard)
├── AGENTS.md                 # Aturan multi-agent universal
├── GEMINI.md                 # Konfigurasi agen Google Antigravity / Gemini
├── CLAUDE.md                 # Konfigurasi instruksi Claude Code / Claude CLI
├── CODEX.md                  # Konfigurasi instruksi OpenAI Codex CLI
├── install.sh                # Multi-CLI auto-detect installer (Bash)
├── install.py                # Multi-CLI installer alternatif (Python)
├── LICENSE                   # Lisensi MIT
├── README.md                 # Dokumentasi panduan
└── scripts/
    ├── init_compose_project.py      # Starter kit inisiasi proyek Compose dari nol
    ├── setup_release_keystore.py    # Auto-generator release keystore & GitHub secrets
    ├── generate_launcher_icons.py   # Generator Adaptive Vector & PNG Mipmap
    └── verify_kotlin_syntax.py      # Pre-flight linter sintaks Kotlin & XML
```

---

## 📜 Lisensi

Didistribusikan di bawah lisensi [MIT](LICENSE). Bebas digunakan, dimodifikasi, dan didistribusikan kembali.
