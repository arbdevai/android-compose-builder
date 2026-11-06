# Protokol Agentic Lifecycle & Manajemen State Sesi (Anti-Amnesia)

Dokumen ini mendefinisikan arsitektur eksekusi mandiri (agentic) untuk AI coding agent yang bekerja pada proyek Android Jetpack Compose. Protokol ini dirancang untuk mengeliminasi **Kelelahan Konteks (Context Fatigue)**, **Amnesia Sesi Baru (New Session Amnesia)**, dan **Halusinasi Tata Letak (UI/UX Positioning Chaos)**.

---

## 1. Anatomi & Efek Kelelahan Konteks (Context Fatigue)

Dalam pengembangan aplikasi jangka panjang, obrolan (chat context) mengalami degradasi kinerja akibat arsitektur Attention Transformer. Memahami mekanismenya adalah kunci pencegahannya:

1. **Lost in the Middle (Degradasi Atensi):**
   Mekanisme *self-attention* model bahasa memberikan bobot probabilitas tertinggi pada awal prompt (system instructions) dan akhir prompt (pesan terbaru). Ketika konteks percakapan memanjang (>30k–50k token), instruksi arsitektur dan kesepakatan desain di tengah percakapan akan "tenggelam", menyebabkan agen melenceng dari rencana awal.
2. **Context Pollution & Penurunan Rasio SNR (Signal-to-Noise Ratio):**
   Log error yang panjang, stack trace kegagalan Gradle/ADB, eksperimen kode yang dibatalkan, dan obrolan basa-basi mencemari context window. Agen mulai bingung membedakan antara kode yang aktif dan kode yang sudah dibuang.
3. **Premature Turn-Completion Bias:**
   Model yang mendekati batas konteks atau menerima prompt yang sangat panjang memiliki kecenderungan bawaan (akibat RLHF) untuk segera menyelesaikan percakapan dengan jawaban dangkal ("Semua fitur sudah tuntas!", padahal masih banyak fungsi kosong).
4. **Stateless Sesi Baru (Amnesia Total):**
   Setiap kali sesi chat baru dibuka, context window kembali ke nol. Diskusi 2 jam di sesi sebelumnya hilang total kecuali disimpan secara persisten di media penyimpanan (file sistem proyek).
5. **Kebutaan Visual Tata Letak Compose (Layout Hallucination):**
   AI tidak memiliki mata untuk merender UI Compose secara visual. Jika tidak dipandu oleh sistem scaffolding hierarkis yang ketat (`Scaffold`, `paddingValues`, `imePadding`, `WindowInsets`), AI akan menebak-nebak posisi komponen, menghasilkan teks tertutup keyboard, tombol keluar layar, atau padding tumpang-tindih.

---

## 2. Solusi: Disk-First State Management (Memori Persisten Proyek)

AI **DILARANG MENGANDALKAN MEMORI CHAT**. Seluruh keputusan arsitektur, status pengerjaan, dan catatan bug wajib ditulis ke dalam disk pada folder `docs/`:

```
proyek/
├── docs/
│   ├── PRD.md         # Kontrak kebutuhan, arsitektur, dan batasan fitur
│   └── STATE.md       # Status aktif, fitur selesai, bug terselesaikan, tugas berikutnya
```

### Aturan Emas Sesi Baru (Zero-Amnesia Bootstrap):
Setiap kali AI memulai giliran kerja (terutama di sesi baru), AI **WAJIB** membaca dua file ini sebelum melakukan tindakan apa pun:
1. Baca `docs/PRD.md` untuk memahami lingkup dan batasan proyek.
2. Baca `docs/STATE.md` untuk mengetahui checkpoint terakhir, bug yang sudah di-fix (agar tidak diulangi), dan tugas prioritas saat ini.

---

## 3. Fase Penemuan Kebutuhan: Wawancara PRD Terstruktur

Jika proyek baru dibuat atau file `docs/PRD.md` belum ada, AI **DILARANG LANGSUNG MENULIS KODE**.
AI wajib mengajukan pertanyaan terstruktur (menggunakan UI multiple-choice atau daftar opsi bernomor) kepada pengguna:

### Format Kuesioner Interaktif Awal:
```markdown
Sebelum mulai menulis kode, mari tetapkan fondasi arsitektur aplikasi melalui opsi berikut:

1. Domain & Target Utama Aplikasi:
   - [A] Utilitas / Phone Diagnostic / Hardware Tool
   - [B] POS / Kasir / Thermal Printer (ESC/POS)
   - [C] Router ISP / Jaringan Lokal / Raw Socket
   - [D] Multimedia / Audio / Native Processing
   - [E] Kustom (Tentukan sendiri)

2. Kebutuhan Lapisan Native (C/C++ & Rust):
   - [A] Pure Kotlin + Jetpack Compose (Tanpa native)
   - [B] C/C++ NDK (CMake + JNI untuk komputasi/low-latency)
   - [C] Rust Native (Cargo-NDK + UniFFI untuk memory safety & crypto)

3. Lapisan Penyimpanan Data (Persistence):
   - [A] Room Database (Relational SQLite + Flow)
   - [B] Jetpack DataStore Preferences (Key-Value ringan)
   - [C] Ktor / OkHttp Network Cache Only

4. Tema UI & Perangkat:
   - [A] True Dark OLED (#000000 murni) + Material3
   - [B] Modern Dynamic Color (Material You)
   - [C] Custom High-Contrast Industrial (Untuk teknisi lapangan)
```

Setelah pengguna memilih, AI mengompilasi jawaban ke dalam `docs/PRD.md`.

---

## 4. Format Standar `docs/PRD.md`

```markdown
# Product Requirement Document (PRD)

## 1. Identitas Aplikasi
- **Nama Aplikasi:** [Nama]
- **Package Name:** [com.domain.app]
- **Min SDK / Target SDK:** 26 / 35 (Android 15 Ready)
- **Arsitektur:** Single-Activity, Clean Architecture (Data -> Domain -> UI), Jetpack Compose Material3.

## 2. Kebutuhan Teknis & Native
- **Native Engine:** [None / C++ NDK / Rust UniFFI]
- **Storage:** [Room / DataStore / In-Memory]
- **Network / Hardware:** [OkHttp / Bluetooth ESC/POS / Raw Socket]

## 3. Daftar Fitur Utama (Vertical Slices)
- [ ] Fitur 1: [Deskripsi detail dari DTO hingga Screen]
- [ ] Fitur 2: [Deskripsi detail dari DTO hingga Screen]
- [ ] Fitur 3: [Deskripsi detail dari DTO hingga Screen]

## 4. Batasan & Desain Sistem
- Bebas AI slop (Nol pulsing green dot, nol marquee, nol glow).
- Nol emoji di seluruh UI, microcopy, dan log.
- Gunakan Vector Icons resmi Material3.
- Shimmer skeleton loading untuk semua status tunggu.
```

---

## 5. Format Standar `docs/STATE.md` (Living Session Memory)

```markdown
# Project State & Session Memory

## Status Saat Ini
- **Fase Aktif:** [Fase 1: Setup Arsitektur / Fase 2: Implementasi Data Layer / dll]
- **Versi Terakhir:** v1.0.0 (versionCode: 10000)
- **Status CI Terakhir:** [Hijau / Menunggu Push / dll]

## Fitur yang Selesai Tuntas (Vertical Slices)
- [x] Inisiasi Proyek & CI/CD GitHub Actions
- [x] In-App Updater dengan streaming .part & isApkValid

## Catatan Bug Terselesaikan & Workaround (Anti-Mengulang Masalah)
- *Bug #01:* `WindowInsets.ime` menyebabkan layout terpotong di Android 14.
  *Solusi:* Wajib pasang `.imePadding()` pada `Column` pembungkus form, bukan di `Scaffold`.
- *Bug #02:* Deadlock pada koneksi paralel router.
  *Solusi:* Gunakan `Mutex.withLock` pada session token, hindari nested `Semaphore`.

## Tugas Aktif Selanjutnya (Next Actions)
1. Buat ViewModel dan Repository untuk Fitur X.
2. Hubungkan ke Compose Screen dengan Shimmer Effect.
3. Jalankan `python3 scripts/verify_kotlin_syntax.py .` sebelum commit.
```

---

## 6. Blueprint Tata Letak Compose (Anti-UI Berantakan)

Untuk mencegah UI berantakan, tertimpa status bar, atau terpotong keyboard virtual, AI **WAJIB** mengikuti hierarki scaffolding berikut:

```kotlin
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MainScreen(viewModel: MainViewModel) {
    val state by viewModel.uiState.collectAsStateWithLifecycle()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Judul Layar") },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surface
                )
            )
        },
        contentWindowInsets = WindowInsets.safeDrawing // Tangani status bar & navigation bar
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding) // Wajib konsumsi padding Scaffold
                .imePadding()          // Geser layout saat keyboard aktif
                .verticalScroll(rememberScrollState())
        ) {
            // Konten Layar
        }
    }
}
```

### Aturan Tata Letak:
1. **Wajib Konsumsi `innerPadding`:** Selalu teruskan `innerPadding` dari `Scaffold` ke root container via `.padding(innerPadding)`. Mengabaikannya akan membuat konten tertutup TopAppBar atau navigasi bawah.
2. **Keyboard Handling:** Pasang `.imePadding()` pada container yang memiliki `TextField` agar form otomatis terangkat saat keyboard virtual muncul.
3. **Scroll Container Safety:** Form input panjang wajib dibungkus `Modifier.verticalScroll(rememberScrollState())` agar tidak terpotong di layar HP berdimensi kecil.

---

## 7. Siklus Mandiri Agentic (Self-Healing Execution Loop)

Sebelum menyatakan tugas selesai atau melakukan commit:
1. **Verifikasi Sintaksis Mandiri:**
   Jalankan `python3 scripts/verify_kotlin_syntax.py .` secara mandiri.
2. **Self-Healing Otomatis:**
   Jika validator mendeteksi hard error (kurung kurawal tidak seimbang, unhandled Result, boundary coroutine terlanggar), AI langsung membaca file terkait, memperbaiki kode, dan menguji ulang hingga menghasilkan **0 Hard Errors**.
3. **Update Living State:**
   Perbarui `docs/STATE.md` dengan mencatat tugas yang selesai dan bug yang berhasil di-fix.
4. **Commit & Push Tuntas:**
   Lakukan git commit dengan pesan teknis ringkas, lalu pantau CI melalui GitHub CLI (`gh run watch <RUN_ID> --interval 60`).
