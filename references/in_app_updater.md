# In-App Updater & APK Integrity System

Panduan implementasi modul pembaruan aplikasi langsung (*in-app updater*) tanpa mengandalkan Google Play Store.

---

## 1. Arsitektur Pengunduhan: Direct OkHttp Streaming

- **Dilarang Android `DownloadManager`:**
  - `DownloadManager` berjalan di proses sistem luar, rentan terhenti saat sinyal lemah, gagal mengikuti redirect bertingkat (GitHub Release ke S3/Azure CDN), dan sering dibunuh oleh pembatasan baterai OEM (MIUI, OneUI, ColorOS).
- **Gunakan OkHttp Streaming Terisolasi:**
  - Unduh langsung ke file sementara (`.part`) dengan buffer 64 KB.
  - Jangan pernah menulis langsung ke file `.apk` sebelum verifikasi selesai.
  - Jika koneksi terputus di tengah jalan, hapus file `.part` seketika untuk mencegah file setengah jadi tertinggal di memori HP.

```kotlin
val httpClient = OkHttpClient.Builder()
    .connectTimeout(30, TimeUnit.SECONDS)
    .readTimeout(60, TimeUnit.SECONDS)
    .writeTimeout(60, TimeUnit.SECONDS)
    .followRedirects(true)
    .followSslRedirects(true)
    .build()
```

---

## 2. Verifikasi Integritas APK 4 Lapis (`isApkValid`)

Jangan hanya mengecek ukuran file seadanya (`length > 5MB`). Gunakan verifikasi 4 lapis untuk mencegah pesan error sistem *"There was a problem parsing the package"*:

1. **Ukuran Fisik Minimum & Exact Match:** Ukuran minimal > 10 MB dan (jika ukuran aset dari release API diketahui) selisih tidak boleh lebih dari 2 KB.
2. **Deep Archive & DEX Parsing:** Panggil `packageManager.getPackageArchiveInfo` dengan flag `GET_ACTIVITIES or GET_SIGNING_CERTIFICATES`. Ini memaksa sistem membaca tabel DEX dan sertifikat. Jika file rusak/terpotong, fungsi ini menghasilkan `null`.
3. **Strict Package Name Match:** Nama package APK hasil unduhan harus cocok persis dengan `context.packageName`.
4. **Monotonic Version Progression:** Pastikan `remoteVersionCode > BuildConfig.VERSION_CODE`.

```kotlin
fun isApkValid(context: Context, apkFile: File, expectedBytes: Long = 0L): Boolean {
    if (!apkFile.exists() || !apkFile.isFile || apkFile.length() < 10_000_000) return false
    if (expectedBytes > 0L && Math.abs(apkFile.length() - expectedBytes) > 2048L) return false
    return try {
        val flags = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            PackageManager.GET_SIGNING_CERTIFICATES or PackageManager.GET_ACTIVITIES
        } else {
            @Suppress("DEPRECATION")
            PackageManager.GET_SIGNATURES or PackageManager.GET_ACTIVITIES
        }
        val pkg = context.packageManager.getPackageArchiveInfo(apkFile.absolutePath, flags) ?: return false
        if (pkg.packageName != context.packageName) return false
        val remoteVersionCode = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
            pkg.longVersionCode
        } else {
            @Suppress("DEPRECATION")
            pkg.versionCode.toLong()
        }
        remoteVersionCode > BuildConfig.VERSION_CODE
    } catch (_: Exception) {
        false
    }
}
```

---

## 3. Pemicuan Instalasi & Izin Sumber Tak Dikenal

Pada Android 8.0+ (API 26+), periksa izin `canRequestPackageInstalls()` sebelum memicu intent instalasi:

```kotlin
fun installApk(context: Context, apkFile: File) {
    if (!apkFile.exists() || apkFile.length() < 10_000_000) return
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O && !context.packageManager.canRequestPackageInstalls()) {
        val settingsIntent = Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES).apply {
            data = Uri.parse("package:${context.packageName}")
            flags = Intent.FLAG_ACTIVITY_NEW_TASK
        }
        context.startActivity(settingsIntent)
        return
    }

    val authority = "${context.packageName}.provider"
    val contentUri = FileProvider.getUriForFile(context, authority, apkFile)
    val installIntent = Intent(Intent.ACTION_VIEW).apply {
        setDataAndType(contentUri, "application/vnd.android.package-archive")
        flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_GRANT_READ_URI_PERMISSION
    }
    context.startActivity(installIntent)
}
```

---

## 4. Pembersihan File Sampah & Komparasi Versi SemVer

- **Pembersihan Otomatis Saat Cek Update:**
  Sebelum mengunduh file baru, pindai direktori unduhan (`downloadDir`) dan hapus seluruh file `.apk` serta sisa `.part` versi lama agar tidak memakan ruang penyimpanan pengguna.
- **Komparasi Versi Numerik:**
  Dilarang membandingkan versi sebagai string biasa (karena `"1.10.0" < "1.9.0"` bernilai `true` pada perbandingan string leksikografis). Pecah string SemVer berdasarkan tanda titik (`.`), konversi ke integer, dan bandingkan secara hierarkis (`Major -> Minor -> Patch`).
