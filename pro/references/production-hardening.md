# Production Hardening (Pro)

Checklist pengerasan aplikasi sebelum rilis production — hal yang membedakan
aplikasi demo dengan aplikasi yang tahan dipakai pengguna nyata.

## 1. R8 / Minify

- Aktifkan di `app/build.gradle.kts` untuk build release:

```kotlin
buildTypes {
    release {
        isMinifyEnabled = true
        isShrinkResources = true
        proguardFiles(
            getDefaultProguardFile("proguard-android-optimize.txt"),
            "proguard-rules.pro"
        )
    }
}
```

- Uji APK release (bukan debug) sebelum submit: minify bisa menghapus
  class yang dipakai via reflection (Room, serialization, dan library
  tertentu butuh `-keep` di `proguard-rules.pro`).
- Simpan mapping file tiap rilis — tanpa itu, stack trace production
  tidak bisa dibaca.

## 2. Crash reporting

- Pasang Firebase Crashlytics atau Sentry **sebelum** rilis pertama.
- Aturan: crash yang tidak dilaporkan = crash yang tidak pernah diperbaiki.
- Jangan log data pribadi (email, token, isi form) ke crash report.

## 3. Ukuran aplikasi

- Target: APK di bawah 20 MB bila memungkinkan; AAB di bawah 15 MB.
- Penyumbang terbesar biasanya: library native (per ABI), gambar, dan font.
- Gunakan App Bundle + split ABI (sudah diaktifkan generator skill) agar
  pengguna hanya mengunduh ABI perangkatnya.

## 4. Performa & ANR

- Ambang Play: ANR rate di atas 0,47% = buruk.
- Jangan lakukan I/O (database, jaringan, file) di main thread.
- Operasi berat pindahkan ke `Dispatchers.IO` / WorkManager.
- Uji di perangkat low-end (RAM 3-4 GB), bukan hanya flagship.

## 5. Keamanan data lokal

- Jangan simpan token/password di SharedPreferences biasa — pakai
  EncryptedSharedPreferences atau DataStore terenkripsi.
- Room database berisi data sensitif: aktifkan SQLCipher bila datanya
  sensitif (data pelanggan, transaksi).
- Jangan log token atau payload sensitif ke Logcat di build release.

## 6. Update & rollback

- In-app updater skill ini (direct OkHttp + validasi 4 lapis) hanya untuk
  distribusi di luar Play (GitHub Release). Untuk aplikasi Play, gunakan
  **Play In-App Updates API** (flexible/immediate) — jangan paksa
  pengguna mengunduh APK dari luar Play.
- Simpan `versionCode` lama yang stabil: bila rilis baru bermasalah,
  hentikan rollout di Play Console, jangan buru-buru rilis patch tanpa
  memahami penyebabnya.

## 7. Checklist pra-rilis (tandai satu per satu)

- [ ] Build release terpasang bersih di perangkat (uninstall dulu)
- [ ] Semua layar dibuka tanpa crash, termasuk setelah rotasi
- [ ] Mode offline diuji (matikan internet, buka semua layar)
- [ ] Izin ditolak satu per satu, aplikasi tetap jalan
- [ ] Update dari versi lama ke versi baru tidak menghapus data
- [ ] Tidak ada data dummy di layar mana pun
- [ ] Tidak ada log sensitif di Logcat build release
