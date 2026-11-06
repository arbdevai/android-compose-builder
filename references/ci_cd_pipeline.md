# CI/CD Pipeline & Chroot Workflow

Panduan kompilasi otomatis berbasis GitHub Actions, penomoran versi SemVer, dan otomatisasi rilis APK.

---

## 1. Prinsip Lingkungan Chroot: Zero Local Compilation

- **Dilarang Kompilasi Lokal:**
  Di lingkungan chroot / PRoot / Termux pada perangkat HP, jangan sekali-kali menjalankan `./gradlew assembleRelease` atau `./gradlew compileDebugKotlin`. Ini akan menghabiskan memori RAM, memicu thermal throttling, dan berujung *OOM crash*.
- **Pendelegasian Penuh ke Cloud Runner:**
  Semua proses kompilasi berat, pembuatan APK, dan signing didelegasikan ke runner GitHub Actions (`ubuntu-latest`).
- **Aturan Push:**
  Hanya lakukan `git push` ketika satu set fitur telah selesai dibuat secara tuntas dan lolos verifikasi pre-flight lokal (`verify_kotlin_syntax.py`). Jangan melakukan push untuk setiap edit 1-2 baris.

---

## 2. Standar Penomoran Versi (SemVer 2.0.0 & Canonical VersionCode)

### A. Aturan `versionName` (Semantic Versioning `MAJOR.MINOR.PATCH`)
- **MAJOR (X.0.0):** Perombakan arsitektur besar, perubahan paradigma, atau migrasi framework fundamental.
- **MINOR (1.X.0):** Penambahan fitur baru yang tetap kompatibel ke belakang.
- **PATCH (1.0.X):** Perbaikan bug, hotfix layout, atau optimasi internal.
- *Aturan:* Jangan menaikkan angka patch hingga puluhan (misal `1.0.95`). Jika fitur fungsional baru telah ditambahkan, segera naikkan ke versi Minor (`1.1.0`).

### B. Formula Canonical `versionCode`
Gunakan formula terprediksi agar `versionCode` selalu monoton naik (*strictly increasing*):
$$\text{versionCode} = \text{MAJOR} \times 10000 + \text{MINOR} \times 100 + \text{PATCH}$$

Contoh:
- `1.0.0` $\rightarrow$ `10000`
- `1.1.0` $\rightarrow$ `10100`
- `1.2.3` $\rightarrow$ `10203`

---

## 3. Ekstraksi Changelog Dinamis & Kebijakan Bebas Emoji

- **Dilarang Release Note Kosong / Hanya Link GitHub:** Release note tidak boleh hanya berisi link perbandingan commits.
- **Kebijakan Bebas Emoji (Zero-Emoji):** Dilarang menyematkan emoji dekoratif di dalam changelog atau release note. Gunakan tipografi Markdown teknis yang bersih.
- **Changelog Dinamis dari Git:**
  Gunakan skrip helper `.github/scripts/generate_release_notes.py` yang membaca riwayat commit aktual sejak tag sebelumnya untuk mengisi rilis GitHub dan dialog update in-app.

---

## 4. Pemantauan CI yang Aman (Interval 60 Detik)

Untuk menghindari pemblokiran kuota GitHub API:
- Pantau workflow run dengan interval tepat 60 detik:
  ```bash
  gh run watch <RUN_ID> --interval 60
  ```
- Jika build CI gagal, periksa log dengan:
  ```bash
  gh run view <RUN_ID> --log-failed
  ```
- Perbaiki kodenya secara tuntas, verifikasi lagi di lokal dengan Python, lalu push commit perbaikan.

---

## 5. Otomatisasi Keystore & Signing APK

Untuk menyiapkan signing rilis tanpa interaksi terminal:
- Jalankan skrip bawaan:
  ```bash
  python3 scripts/setup_release_keystore.py
  ```
- Skrip ini otomatis mengecek keberadaan `keytool` (atau menginstalnya jika diizinkan), membuat keystore 2048-bit RSA secara non-interaktif, dan mendaftarkan 4 GitHub Secret (`KEYSTORE_BASE64`, `KEYSTORE_PASSWORD`, `KEY_ALIAS`, `KEY_PASSWORD`) via `gh secret set`.

---

## 6. Pencegahan Kegagalan Build CI & Isolasi Tooling

Sebelum melakukan `git push` pertama kali ke repositori GitHub, pastikan 4 syarat infrastruktur berikut terpenuhi:

1. **Kelengkapan Gradle Wrapper:**
   - Berkas `gradlew` (dengan izin eksekusi `chmod +x`) dan folder `gradle/wrapper/` (`gradle-wrapper.jar` & `gradle-wrapper.properties`) wajib tersedia di root proyek.
2. **Konfigurasi `gradle.properties`:**
   - Wajib memuat `android.useAndroidX=true` dan `ksp.useKSP2=false`:
     ```properties
     org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
     android.useAndroidX=true
     android.nonTransitiveRClass=true
     kotlin.code.style=official
     ksp.useKSP2=false
     ```
3. **Aturan Room DAO vs KSP2 (`unexpected jvm signature V`):**
   - Pada Room Database, setiap fungsi `@Dao` dengan anotasi `@Query("DELETE ...")` atau `@Query("UPDATE ...")` yang menggunakan `suspend` **wajib** memiliki tipe kembalian `: Int` (jumlah baris terdampak), bukan `Unit` atau tanpa tipe kembalian.
4. **Isolasi Folder `scripts/` (Anti-Leak ke Git):**
   - Folder `scripts/` adalah tooling lokal chroot. Pastikan `scripts/` selalu berada di dalam `.gitignore` proyek agar tidak ikut ter-commit dan terunggah ke repositori GitHub aplikasi.
