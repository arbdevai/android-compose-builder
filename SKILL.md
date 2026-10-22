---
name: android-compose-builder
description: >-
  Expert Android developer skill for building Kotlin + Jetpack Compose applications.
  Use this skill when creating or modifying Android apps, focusing on modern UI/UX,
  smooth animations, authentic vector icons (anti-AI slop), professional non-alay copy,
  zero dummy data, autonomous modern library selection, 1-minute CI monitoring interval
  (anti-boncos GitHub API), skeleton screens & shimmer effect (anti-loading spinner),
  concurrency & mutex resilience (anti-deadlock), robust API management,
  background tasks (WorkManager), deep linking, GitHub Actions CI/CD, and proper APK signing without Play Store.
---

# Android Compose Builder Skill

Gunakan skill ini saat Anda diminta untuk membuat atau mengembangkan aplikasi Android (APK) dari nol maupun memodifikasi dan meningkatkan aplikasi yang sudah ada. Skill ini dirancang agar AI dapat bekerja secara mandiri, tuntas, tanpa perlu diajari ulang setiap kali membuat atau memodifikasi aplikasi.

---

## 1. Kebebasan Penuh Penggunaan Library (Autonomous Library Selection)

- **AI Bebas Memilih Library Terbaik:** Anda (AI) **BEBAS dan DIBERIKAN WEWENANG PENUH** untuk memilih, menambahkan, dan mengonfigurasi pustaka (library) pihak ketiga modern apapun yang relevan, stabil, dan efisien tanpa perlu meminta izin kepada pengguna.
- **Rekomendasi Ekosistem Standar:**
  - **Networking & Serialization:** Retrofit / Ktor Client, OkHttp 5+, Kotlinx Serialization Json.
  - **Asynchronous & Concurrency:** Kotlin Coroutines (`StateFlow`, `SharedFlow`), `Mutex`, `Semaphore`, CoroutineWorker.
  - **Image Loading:** Coil 3+ (`io.coil-kt.coil3:coil-compose`).
  - **Local Persistence & Cache:** Jetpack DataStore Preferences (pengganti SharedPreferences) & Room DB.
  - **Background Processing:** AndroidX WorkManager (`androidx.work:work-runtime-ktx`).
  - **UI & Icons:** Jetpack Compose Material3, Material Icons Extended (`androidx.compose.material:material-icons-extended`).
  - **QR Code & Barcode:** ZXing Core (`com.google.zxing:core`).
  - **Bluetooth & Hardware:** Android Bluetooth API, POS thermal printer protocols (ESC/POS).
- **Manajemen Dependensi Terpusat:** Selalu kelola versi pustaka secara rapi melalui Gradle Version Catalog (`gradle/libs.versions.toml`) dan sinkronkan dengan `app/build.gradle.kts`.

---

## 2. Kebijakan Anti Data Dummy & Hardcoded (Zero Dummy Data Policy)

- **DILARANG DATA DUMMY DI PRODUKSI:** Pada aplikasi yang terhubung ke perangkat keras (router, modem GPON/EPON, IoT), backend REST/GraphQL, atau database, **JANGAN PERNAH** membiarkan nilai tiruan (*dummy*), mock statis, atau data bohongan tetap tampil di layar.
- **Reverse-Engineering & Dokumentasi API Nyata:**
  - Telusuri endpoint nyata (misal: router FiberHome, ZTE, Huawei, Mikrotik, atau server lokal).
  - Dekode skema otentikasi nyata (enkripsi AES, token sesi, cookie, header unik, penggantian tanda baca seperti `_point_` menjadi `.`).
  - Catat struktur response riil ke dalam dokumentasi (`API.md` / `ROUTER_API.md`).
  - Petakan ke Kotlin `data class` DTO lengkap dengan parser yang toleran (`ignoreUnknownKeys = true`).
- **Penanganan Kondisi Kosong (Empty & Loading State):**
  - Jika data belum selesai dimuat, tampilkan placeholder loader atau skeleton screen (`"-"`, `"0"`, skeleton cards), **BUKAN** data fiktif buatan sendiri (misal: jangan tampilkan IP `192.168.1.100` atau redaman `-20.5 dBm` palsu).

---

## 3. UI/UX dan Kualitas Kode Jetpack Compose

- **Bahasa & Framework:** Wajib menggunakan Kotlin modern dan Jetpack Compose (Material3).
- **Arsitektur:** Terapkan Clean Architecture dengan pola MVVM atau MVI. Pisahkan lapisan UI (Compose Screens & Components), ViewModel (`StateFlow`), Repository, dan Data/API Client.
- **Transisi Layar Halus (Smooth Navigation & Animations):**
  - **JANGAN PERNAH** menggunakan pergantian layar `when (...)` instan tanpa animasi.
  - Gunakan `AnimatedContent` dengan transisi directional slide + fade yang halus (`slideInHorizontally + fadeIn togetherWith slideOutHorizontally + fadeOut`) untuk perpindahan antar-layar dan tab navigasi.
  - Berikan animasi interaktif pada komponen aktif (misalnya *animated capsule pill indicator*, *spring elevation*, ripple feedback).
- **Aturan Navigasi & BackHandler:**
  - Tangani tombol fisik/gesture kembali menggunakan `BackHandler` secara bertingkat (dari sub-halaman kembali ke dashboard sebelum keluar aplikasi).
  - **JANGAN PERNAH** menambahkan tombol "Keluar" atau "Exit" di `TopAppBar` atau navigasi utama. Ini melanggar pedoman mobile UX standar Android.
- **Konsistensi Tema & Warna (Color System):**
  - Definisikan seluruh konstanta warna secara terpusat di `ui/theme/Color.kt`.
  - Berikan alias jika ada nama yang mirip (contoh: `val SignalPoor = SignalWeak`) agar tidak menimbulkan compiler error `Unresolved reference`.

---

## 4. Standar Skeleton Screen (Shimmer Effect) & Anti-Loading Spinner

- **DILARANG FULL-SCREEN LOADING SPINNER:**
  - **JANGAN PERNAH** menampilkan `CircularProgressIndicator` spinner besar di tengah layar kosong saat memuat konten awal halaman atau berpindah tab/menu. Layar kosong dengan spinner berputar membuat aplikasi terkesan lambat, usang, dan menimbulkan *content jumping* kasar saat data muncul.
- **WAJIB MENGGUNAKAN SKELETON SCREEN BER-SHIMMER:**
  - Gantikan layar loading dengan **Skeleton Screen** yang meniru struktur tata letak (layout mockup) data riil yang akan dimuat (misal: kartu status, chip metrik, daftar item, form input).
  - Berikan animasi kilau cahaya berjalan halus (**Shimmer Effect**) secara berulang.
- **Implementasi Murni Jetpack Compose (Zero Dependency Tambahan):**
  - Tidak memerlukan library berat eksternal. Gunakan ekstensi `Modifier.shimmerEffect()` berbasis `rememberInfiniteTransition` dan `Brush.linearGradient`:
    ```kotlin
    fun Modifier.shimmerEffect(): Modifier = composed {
        var size by remember { mutableStateOf(IntSize.Zero) }
        val transition = rememberInfiniteTransition(label = "shimmerTransition")
        val startOffsetX by transition.animateFloat(
            initialValue = -2 * size.width.toFloat(),
            targetValue = 2 * size.width.toFloat(),
            animationSpec = infiniteRepeatable(
                animation = tween(1200, easing = LinearEasing),
                repeatMode = RepeatMode.Restart
            ),
            label = "shimmerOffset"
        )
        background(
            brush = Brush.linearGradient(
                colors = listOf(
                    MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f),
                    MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.2f),
                    MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.5f),
                ),
                start = Offset(startOffsetX, 0f),
                end = Offset(startOffsetX + size.width.toFloat(), size.height.toFloat())
            )
        ).onGloballyPositioned { size = it.size }
    }
    ```
- **Komponen Skeleton Siap Pakai:**
  - Sediakan komponen modular di `ui/components/SkeletonComponents.kt`:
    - `SkeletonBox(modifier, shape)`: Balok shimmer untuk teks/tombol.
    - `SkeletonCard(modifier)`: Kartu shimmer untuk widget informasi.
    - `SkeletonDashboard()`: Placeholder satu layar penuh khusus dashboard.
    - `SkeletonListItem()`: Placeholder baris data/list.
- **Kapan Spinner Masih Boleh Digunakan?**
  - Hanya untuk aksi inline berskala kecil (ukuran 16dp - 24dp): di dalam tombol submit form saat proses kirim sedang berlangsung, atau ikon refresh kecil di `TopAppBar`.

---

## 5. Aturan Keyboard & Soft Input UX (Anti Keyboard Overlap)

Di Jetpack Compose, masalah umum adalah keyboard virtual menutupi tombol aksi atau input field saat difokuskan:
- **Wajib Ime Padding & Scroll:** Pada setiap layar formulir atau layar yang memiliki `TextField`/`OutlinedTextField`, bungkus tata letak dengan:
  ```kotlin
  Modifier
      .fillMaxSize()
      .imePadding()
      .verticalScroll(rememberScrollState())
  ```
- **Manifest Soft Input Mode:** Pastikan Activity di `AndroidManifest.xml` memiliki atribut:
  ```xml
  android:windowSoftInputMode="adjustResize"
  ```
- **Auto-Dismiss Keyboard:** Pasang `LocalFocusManager.clearFocus()` saat pengguna mengetuk di luar area input agar keyboard menutup secara alami.

---

## 6. Aturan Gaya Bahasa: Anti-Alay & Bebas Bahasa Berlebihan

Dilarang keras menggunakan gaya bahasa berlebihan, mendramatisir, hiperbolis, sok asik, manja, kaku, atau khas template "AI / Alay" pada seluruh elemen aplikasi:
- **Terapkan pada:** Teks tombol, label input, placeholder formulir, dialog konfirmasi, banner notifikasi in-app, notifikasi status bar, teks struk/nota, komentar kode, dan pesan commit git.
- **Prinsip Utama:** Bahasa harus **lugas, profesional, natural, to-the-point, dan sopan.**

### Microcopy Dictionary:

| Konteks | ❌ DILARANG (Alay / Lebay / Khas AI) | ✅ STANDAR BENAR (Profesional & Ringkas) |
| :--- | :--- | :--- |
| **Teks Tombol** | "Yuk Bayar Sekarang Juga Kakak Sayang ✨", "Gaskeun Bayar!" | "Bayar Sekarang", "Cek Tagihan", "Konfirmasi Pembayaran" |
| **Notifikasi Tagihan** | "Aduh bestie gawat! Internet kamu mau diputus nih, cus buruan transfer ya say 😭🙏" | "Tagihan internet WiFi sebesar Rp 150.000 jatuh tempo hari ini. Segera selesaikan pembayaran." |
| **Pesan Error Server** | "Aduh maaf banget ya kak, servernya lagi bobo cantik nih, jangan sedih ya 💔" | "Server sedang dalam pemeliharaan (Maintenance). Silakan coba beberapa saat lagi." |
| **Pesan Jaringan Putus** | "Koneksi internetmu hilang ditelan bumi kak, coba cek lagi ya..." | "Koneksi ke server terputus (Timeout). Periksa koneksi internet Anda." |
| **Input / Placeholder** | "Ketikkan nomor pelanggan tercintamu di sini ya kak..." | "Masukkan ID atau Nomor HP Pelanggan" |
| **Status Berhasil** | "Horeee berhasil banget dong kak! Senangnya transaksi kamu sukses 🎉🥳" | "Pembayaran Berhasil. Paket internet Anda telah aktif." |
| **Dialog Konfirmasi** | "Yakin nih mau ninggalin aplikasi yang unyu ini?" | "Konfirmasi Pembayaran: Lanjutkan pembayaran tagihan ini?" |

---

## 7. Lapisan API "Anti Rontok", Mutex & Resilience (Robust Networking & Concurrency)

Untuk menjamin aplikasi tidak pernah force close / crash akibat perubahan di sisi server web, gangguan jaringan, maupun batasan hardware lokal/router:

- **Concurrency & Anti-Deadlock pada Perangkat Keras / Router:**
  - **Otentikasi Atomik dengan `Mutex`:**
    Jika aplikasi berkomunikasi dengan router/embedded device yang membatasi 1 sesi login aktif, gunakan `kotlinx.coroutines.sync.Mutex` untuk mengamankan proses login (`authMutex.withLock { ... }`). Jangan biarkan coroutine paralel memicu login bersamaan yang menyebabkan *session thrashing* atau token invalid.
  - **Larangan Re-entrancy pada Semaphore (Anti-Deadlock):**
    Jika menggunakan `Semaphore` untuk membatasi *rate limit* router (misal `Semaphore(2)` atau `Semaphore(4)`):
    **JANGAN PERNAH** memanggil fungsi yang juga meminta izin semaphore dari dalam blok yang sudah memegang permit semaphore tersebut! Pemanggilan bersarang (*nested permit acquisition*) pada single-thread atau permit terbatas akan menyebabkan kebuntuan permanen (**Deadlock**), membuat aplikasi menggantung selamanya.
  - **Pre-Authentication Sebelum Request Paralel:**
    Sebelum mengeksekusi banyak panggilan API secara paralel menggunakan `async { ... }`, pastikan token otentikasi / sesi aktif sudah diperoleh terlebih dahulu secara sekuensial. Jangan mendistribusikan otentikasi ke dalam masing-masing worker async.
- **Single Singleton OkHttpClient:**
  - Konfigurasi `OkHttpClient` terpusat dengan timeout yang wajar (`connectTimeout`, `readTimeout`, `writeTimeout` minimal 30 detik).
  - Tambahkan interceptor terpusat untuk header wajib (`Accept: application/json`, API Key, atau Bearer Token).
  - Gunakan `HttpLoggingInterceptor` (level `BODY` untuk tracing saat debug).
- **Golden Rule Model DTO (Kotlinx Serialization):**
  - Konfigurasi JSON parser wajib toleran:
    ```kotlin
    Json {
        ignoreUnknownKeys = true  // Abaikan field baru tak dikenal dari backend
        isLenient = true          // Fleksibel terhadap format string/kuotasi longgar
        encodeDefaults = true     // Sertakan default value saat serialisasi
        coerceInputValues = true  // Otomatis fallback ke default jika null/tipe mismatch
    }
    ```
  - Pada seluruh data class model DTO, **selalu berikan default value** (`= null` atau `= emptyList()` atau `= false`) agar aman dari perubahan skema API backend.
- **Mitigasi Server Down / Halaman HTML (Maintenance Fallback):**
  - Sering kali ketika server web backend mengalami maintenance atau gangguan Cloudflare/Nginx, server mengembalikan status 502/503 dalam bentuk dokumen HTML (`<html>...Bad Gateway...</html>`), bukan JSON.
  - Sebelum memparsing error body sebagai JSON, selalu periksa apakah string error berawalan `<` atau mengandung tag HTML. Jika ya, jangan coba di-deserialize (akan menyebabkan `SerializationException`), melainkan langsung petakan ke pesan:
    `"Server sedang dalam pemeliharaan (Maintenance). Silakan coba beberapa saat lagi."`
- **Sentralisasi Pemetaan Kode HTTP:**
  - `401 / 403`: `"Nomor HP atau kata sandi tidak cocok, atau sesi login berakhir."`
  - `404`: `"Data tidak ditemukan di server."`
  - `500`: `"Terjadi gangguan sistem pada server. Silakan coba kembali."`
  - `502 / 503 / 504`: `"Server sedang dalam pemeliharaan (Maintenance). Silakan coba beberapa saat lagi."`
- **Pemetaan Network Exception:**
  - `SocketTimeoutException`: `"Koneksi ke server terputus (Timeout). Periksa sinyal internet Anda."`
  - `UnknownHostException` / `ConnectException`: `"Tidak dapat terhubung ke server. Periksa koneksi internet Anda."`
- **Pola Arsitektur `Result<T>` di Repository:**
  - Seluruh fungsi repository wajib membungkus respons dalam `Result<T>` (`Result.success` atau `Result.failure(Exception(friendlyMessage))`).
  - ViewModel tidak boleh membiarkan exception jaringan mentah lolos ke antarmuka pengguna tanpa diformat.
- **Dukungan Cleartext Traffic (Koneksi HTTP & Server Lokal):**
  - Pastikan menambahkan atribut:
    ```xml
    android:usesCleartextTraffic="true"
    ```
    pada tag `<application>` di `AndroidManifest.xml` agar koneksi HTTP ke IP gateway lokal (seperti `192.168.1.1` atau printer termal lokal) tidak diblokir Android 9+.

---

## 8. Standar Ikon & Desain Grafis (Paten Bebas "AI Slop")

- **DILARANG "AI SLOP":** Jangan pernah meminta atau menyematkan ikon aplikasi berupa gambar render 3D hiperbolis yang tampak seperti buatan AI generik dan tidak proporsional.
- **Wajib Adaptive Vector Icons:**
  - Gunakan standar resmi Android Adaptive Icon di `res/mipmap-anydpi-v26/ic_launcher.xml` dan `ic_launcher_round.xml`.
  - Pisahkan latar belakang (`res/drawable/ic_launcher_background.xml`) dan simbol latar depan (`res/drawable/ic_launcher_foreground.xml`) menggunakan vektor SVG/XML yang bersih, geometris, dan tajam (safe zone 72dp di dalam canvas 108dp).
- **Generator Otomatis Raster PNG Mipmap:**
  - Jalankan skrip helper bawaan skill untuk otomatis merender seluruh densitas PNG murni (`mdpi`, `hdpi`, `xhdpi`, `xxhdpi`, `xxxhdpi`):
    ```bash
    # Menggunakan skrip lokal di dalam skill / repo:
    python3 scripts/generate_launcher_icons.py app/src/main/res
    # Atau dari konfigurasi global:
    python3 ~/.gemini/config/skills/android-compose-builder/scripts/generate_launcher_icons.py app/src/main/res
    ```

---

## 9. Logic In-App Updater yang Kebal Bug & Bersih Storage

- **Pembersihan Otomatis File APK Lama (Anti-Sampah & Anti-Penumpukan APK):**
  - **JANGAN PERNAH** membiarkan file-file APK installer menumpuk di memori perangkat pengguna (`devbox-v1.0.9.apk`, `devbox-v1.0.10.apk`, dll.) setiap kali update dirilis. File APK yang menumpuk dapat menguras ratusan MB memori pengguna secara diam-diam.
  - **Auto-Cleanup Saat Cek & Unduh:** Sebelum memulai pengunduhan versi baru, `UpdateManager` **WAJIB** memindai direktori unduhan (`downloadDir`) dan menghapus seluruh file APK usang dari versi sebelumnya.
  - **Auto-Cleanup Pasca-Update Berhasil:** Saat aplikasi dibuka dan versi yang berjalan sudah sama dengan atau lebih baru dari file APK yang ada di storage (artinya instalasi pembaruan telah sukses), hapus installer APK tersebut secara otomatis.
  - **Contoh Implementasi Standar:**
    ```kotlin
    fun cleanupOldApks(context: Context, keepVersion: String? = null) {
        try {
            val downloadDir = context.getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS)
                ?: context.cacheDir
            val keepFileName = if (keepVersion != null) "app-$keepVersion.apk" else null

            downloadDir.listFiles { file -> file.isFile && file.name.endsWith(".apk") }?.forEach { file ->
                if (keepFileName == null || file.name != keepFileName) {
                    val deleted = file.delete()
                    Log.i("UpdateManager", "Membersihkan APK usang: ${file.name} (dihapus: $deleted)")
                }
            }
        } catch (e: Exception) {
            Log.w("UpdateManager", "Gagal membersihkan APK lama: ${e.message}")
        }
    }
    ```
- **Cek File Sebelum Unduh (Anti Double-Download):**
  - Sebelum memicu `DownloadManager`, periksa apakah file APK untuk versi target sudah pernah diunduh dan valid di penyimpanan lokal. Jika sudah ada, langsung arahkan ke instalasi tanpa mengunduh ulang.
- **Pantau Status DownloadManager:**
  - Pantau progres download secara reaktif (`DownloadManager.STATUS_RUNNING`, `STATUS_SUCCESSFUL`, `STATUS_FAILED`) agar pengguna mendapat indikator unduhan yang jelas.
- **Pemasangan Mandiri via FileProvider:**
  - Pemicu instalasi wajib menggunakan `FileProvider` dengan intent `ACTION_VIEW` dan tipe MIME `application/vnd.android.package-archive`:
    ```kotlin
    val contentUri = FileProvider.getUriForFile(context, "${context.packageName}.provider", apkFile)
    val installIntent = Intent(Intent.ACTION_VIEW).apply {
        setDataAndType(contentUri, "application/vnd.android.package-archive")
        flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_GRANT_READ_URI_PERMISSION
    }
    context.startActivity(installIntent)
    ```
  - **JANGAN** melempar pengguna ke browser eksternal untuk mengunduh APK manual jika sudah ada in-app update.

---

## 10. Background Tasks (WorkManager) & Deep Linking

- **Gunakan WorkManager:**
  - Untuk tugas berkala di latar belakang, wajib menggunakan `androidx.work:work-runtime-ktx` dengan `CoroutineWorker` (`PeriodicWorkRequestBuilder`), **BUKAN** Background Service biasa yang mudah dibunuh oleh Doze Mode Android modern.
  - Jadwalkan tugas dengan `ExistingPeriodicWorkPolicy.KEEP` agar tidak mereset jadwal setiap kali aplikasi dibuka.
- **Izin Notifikasi Android 13+ (TIRAMISU):**
  - Periksa izin `Manifest.permission.POST_NOTIFICATIONS` dengan dialog penjelasan edukatif terlebih dahulu.
- **Deep Linking:**
  - Daftarkan `<intent-filter android:autoVerify="true">` pada `MainActivity` untuk protokol `http`, `https`, dan skema kustom.
  - Tangani parameter URL baik di `onCreate` maupun `onNewIntent`.

---

## 11. Proses Build & CI/CD GitHub Actions (Zero Local Build & Anti-Boncos API)

- **DILARANG BUILD LOKAL & RESPON INSTAN:**
  - **JANGAN SEKALI-KALI** menjalankan perintah gradle lokal (seperti `./gradlew assembleRelease` atau `./gradlew compileDebugKotlin` atau perintah `gradlew` lainnya) di workspace. Ini dilarang keras karena membuang resource dan kuota lokal.
  - Saat pengguna meminta "build", AI **WAJIB LANGSUNG** memvalidasi sintaks, membuat commit release berawalan `"Release v..."`, dan melakukan `git push` ke GitHub Actions CI. Jangan pernah berputar-putar di workspace lokal sebelum push.
  - Semua proses kompilasi didelegasikan penuh ke GitHub Actions CI.
- **DILARANG MEMBERIKAN DATA BOHONGAN / STATUS HALUSINASI:**
  - AI **DILARANG KERAS** mengklaim, menebak, atau berasumsi bahwa build CI sudah berhasil / APK rilis sudah terbit tanpa bukti nyata dari output perintah resmi (`gh run view`, `gh release view`, atau API GitHub).
  - Jika perintah status gagal dieksekusi (misal kendala PTY atau jaringan), AI wajib menyatakan secara transparan dan jujur bahwa status belum bisa diverifikasi, **BUKAN** mengarang bahwa build sudah sukses.
- **Pembaruan Versi (Auto-Bump):**
  - Setiap rilis baru, wajib menaikkan `versionCode` dan `versionName` di `app/build.gradle.kts`.
- **Git Push Aman Tanpa Password Prompt:**
  - Dorong perubahan menggunakan GitHub Token agar tidak tergantung pada prompt interaktif:
    ```bash
    git push "https://$(gh auth token)@github.com/<owner>/<repo>.git" main
    ```
- **Rilis Otomatis (Tanpa Double Build):**
  - **JANGAN PERNAH** menggunakan `git push origin main --tags` atau membuat tag git secara manual di lokal.
  - Cukup buat commit di branch `main` dengan pesan yang diawali kata `"Release v..."` (contoh: `git commit -m "Release v1.0.3 - Penambahan fitur..."`), lalu push ke `main`.
  - Workflow GitHub Actions akan mendeteksi pesan commit ini, membangun signed APK, dan otomatis membuat GitHub Release serta Git Tag dalam satu siklus build.
- **Pemantauan Proaktif CI dengan Interval Mutlak 1 Menit (Anti-Boncos API):**
  - **ATURAN WAJIB KUOTA:** Pantau workflow build GitHub Actions dengan **interval tepat 60 detik (1 menit)** agar tidak menguras kuota GitHub API:
    ```bash
    gh run watch <RUN_ID> --interval 60
    ```
  - **DILARANG KERAS** menggunakan interval cepat di bawah 60 detik (seperti `--interval 10` atau loop polling cepat).
  - Jika build CI gagal (X), gunakan `gh run view <RUN_ID> --log-failed` untuk membaca log error yang sesungguhnya, perbaiki kodenya langsung, lalu push perbaikan dengan commit release baru.
  - Hanya setelah output resmi menyatakan `completed with 'success'`, unduh release APK atau laporkan link rilis serta ukuran file riil kepada pengguna.

---

## 12. Manajemen Signing Keystore Release (Anti-Muter-Muter & Zero Hesitation)

- **LARANGAN KERAS BERPUTAR-PUTAR KETIKA KEYTOOL TIDAK TERPASANG:**
  - Jika AI memerlukan `keytool` namun perintah tidak ditemukan (`keytool: command not found`), **DILARANG KERAS** berputar-putar mencoba cara alternatif aneh (seperti menulis script openssl rumit, membuat fake certificate, menggunakan debug signing untuk rilis, atau bertanya bingung ke pengguna).
  - Cukup jalankan perintah instalasi paket headless dalam 1 baris:
    ```bash
    sudo apt-get update && sudo apt-get install -y openjdk-17-jre-headless
    ```
- **SOLUSI 1-BARIS OTOMATIS (SANGAT DIREKOMENDASIKAN):**
  - Gunakan skrip bawaan skill yang otomatis mengecek/menginstall `keytool`, membuat keystore non-interaktif, dan mengunggah 4 secret ke GitHub (`gh secret set`):
    ```bash
    python3 scripts/setup_release_keystore.py
    # Atau dari path global:
    python3 ~/.gemini/config/skills/android-compose-builder/scripts/setup_release_keystore.py
    ```
- **MANUAL NON-INTERAKTIF (JIKA DIPERLUKAN):**
  - **DILARANG KERAS** menjalankan `keytool -genkeypair` tanpa flag `-noprompt` dan `-dname` karena akan membekukan terminal dalam prompt interaktif ("What is your name?").
  - Perintah standar non-interaktif:
    ```bash
    keytool -genkeypair -v -keystore release.keystore -alias releaseKey -keyalg RSA -keysize 2048 -validity 10000 -storepass "$SECRET_PASS" -keypass "$SECRET_PASS" -dname "CN=Android App, OU=Mobile, O=Arbdev, C=ID" -noprompt
    ```
  - Unggah 4 rahasia ke GitHub Secrets:
    ```bash
    gh secret set KEYSTORE_BASE64 -b "$(base64 -w 0 release.keystore)"
    gh secret set KEYSTORE_PASSWORD -b "$SECRET_PASS"
    gh secret set KEY_ALIAS -b "releaseKey"
    gh secret set KEY_PASSWORD -b "$SECRET_PASS"
    ```
  - Pastikan `*.keystore` sudah terdaftar di `.gitignore` agar file fisik tidak bocor ke repositori publik.

---

## 13. Pre-Flight Linter & Memory-Safe Validator (Zero-CI-Failure & Anti-Leak)

Untuk mencegah kegagalan build di GitHub Actions dan kebocoran memori (Memory Leak) saat aplikasi berjalan:

### A. Aturan Wajib & Hard Errors (Memblokir CI Build - Exit 1):
- **Keseimbangan Tanda Kurung & Sintaks XML:**
  - Tokenizer kurung kurawal, kurung siku, dan kurung biasa dengan pemahaman literal string dan komentar.
  - File XML (res/drawables, values, AndroidManifest.xml) wajib well-formed.
- **Proteksi Listener & DisposableEffect:**
  - **DILARANG** memanggil `DisposableEffect` tanpa menyertakan blok pembersihan `onDispose { ... }`. Melewatkan `onDispose` adalah pelanggaran fatal yang membocorkan callback/listener di memori selamanya.
- **Verifikasi Coroutine Scope & Suspend Functions dalam Compose:**
  - **DILARANG** memanggil fungsi `suspend` (seperti `ScrollState.scrollTo`, `animateScrollTo`, `SnackbarHostState.showSnackbar`, dsb.) langsung di dalam regular non-suspending lambda (seperti `onValueChange`, `onClick`, `onKeyEvent`).
  - Semua fungsi `suspend` wajib dipanggil di dalam `LaunchedEffect` atau dibungkus `coroutineScope.launch { ... }` dari `rememberCoroutineScope()`.
- **Verifikasi Objek `kotlin.Result<T>`:**
  - **DILARANG** mengakses properti atau fungsi tipe yang dibungkus langsung pada variabel `Result<T>` (misal: `res.stdout` atau `res.exitCode`).
  - Wajib diekstrak melalui `.getOrNull()?.prop`, `.getOrThrow().prop`, atau `res.fold(...)`.
- **Verifikasi Import Ekstensi Modifier Compose:**
  - Fungsi ekstensi umum pada `Modifier` seperti `.border(...)`, `.clip(...)`, `.clickable(...)`, dan `.background(...)` wajib mengimpor paket `androidx.compose.foundation.*` atau `androidx.compose.ui.draw.*`.
- **Verifikasi Scope Variabel `it` dalam Lambda Berparameter:**
  - **DILARANG** menggunakan kata kunci `it` di dalam lambda yang sudah memiliki parameter bernama eksplisit (seperti `{ keyCode -> ... }`, `{ sess -> ... }`, atau `{ reader -> ... }`) kecuali di dalam inner lambda lokal.
- **Verifikasi Resolusi Referensi Class/Object Antar Package:**
  - Setiap pemanggilan nama class atau singleton object internal proyek antar-package wajib memiliki deklarasi import spesifik atau wildcard yang valid.

### B. Soft Warnings (Advisory Memory Leak & Lifecycle - Non-Blocking, Exit 0):
- **Pencegahan Kebocoran StateFlow di Background:**
  - Prioritaskan `collectAsStateWithLifecycle()` dari `androidx.lifecycle.compose` dibanding `collectAsState()` biasa agar pengumpulan Flow otomatis berhenti saat aplikasi berada di background.
- **Larangan Unmanaged Coroutines (`GlobalScope`):**
  - Hindari `GlobalScope.launch` / `GlobalScope.async` di luar scope terkontrol karena tidak terikat lifecycle Composable/ViewModel.
- **Pencegahan Activity Context Leak:**
  - Dilarang menyimpan referensi `Context`, `Activity`, atau `View` di dalam `companion object` / static `var`.
  - Di dalam ViewModel, gunakan `AndroidViewModel(application)` atau `context.applicationContext`, bukan instance `Activity` langsung.

### C. Sistem Pengecualian / Suppression (Anti-Membabi Buta):
Agar validator tidak merusak atau memblokir kode legacy / third-party / vendor yang kepemilikannya tidak jelas:
- **Auto-Ignore Direktori Khusus:**
  - Direktori `legacy/`, `vendor/`, `thirdparty/`, `third_party/`, `generated/`, `build/`, `.gradle/`, `.git/` otomatis diabaikan dari inspeksi.
- **Pengecualian Per Baris (Line-Level Ignore):**
  - Cukup tambahkan komentar `// @validator-ignore` (atau `// @validator-ignore: <tag>`) pada baris terkait atau baris di atasnya.
  - Mendukung juga anotasi Kotlin standar `@Suppress(...)`.
- **Pengecualian Satu File Penuh (File-Level Ignore):**
  - Letakkan `// @validator-ignore-file` pada baris atas file legacy / pihak ketiga.
  - **AI DILARANG** membabi buta mengubah kode warisan/third-party yang tidak jelas kepemilikannya; gunakan tag pengecualian jika kode tersebut memang sengaja dipertahankan.

### D. Eksekusi Validator Wajib:
- AI **WAJIB** menjalankan skrip validasi sintaks sebelum melakukan commit:
  ```bash
  python3 scripts/verify_kotlin_syntax.py .
  # Atau dari path global:
  python3 ~/.gemini/config/skills/android-compose-builder/scripts/verify_kotlin_syntax.py .
  ```
- Pastikan seluruh file lolos verifikasi sebelum menjalankan `git commit` dan `git push`.

---

## 14. 1-Click Starter Kit (Memulai Proyek Baru dari Nol)

Jika pengguna meminta inisiasi proyek Android baru di direktori kosong:
1. Jalankan skrip starter kit otomatis:
   ```bash
   # Menggunakan skrip lokal di dalam skill / repo:
   python3 scripts/init_compose_project.py --name "NamaAplikasi" --package "com.nama.app"
   # Atau dari konfigurasi global:
   python3 ~/.gemini/config/skills/android-compose-builder/scripts/init_compose_project.py --name "NamaAplikasi" --package "com.nama.app"
   ```
2. Buat repositori Git lokal (`git init`).
3. Buat repositori GitHub publik (`gh repo create <nama-repo> --public --source=. --remote=origin`).
4. Generate keystore & unggah GitHub Secrets secara otomatis dalam 3 detik:
   ```bash
   python3 scripts/setup_release_keystore.py
   # Atau: python3 ~/.gemini/config/skills/android-compose-builder/scripts/setup_release_keystore.py
   ```
5. Lakukan commit pertama berawalan `"Release v1.0.0 - Inisiasi Proyek"` dan push ke `origin main`.
6. Pantau build CI dengan interval 60 detik sampai signed APK release v1.0.0 selesai dan siap diunduh.
