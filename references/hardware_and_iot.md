# Hardware, Embedded Devices & IoT Integration

Panduan integrasi perangkat keras, embedded gateway (router, modem GPON/EPON), printer termal POS, dan komunikasi jaringan lokal pada Android.

---

## 1. Otentikasi Atomik & Pencegahan Deadlock

Perangkat keras embedded biasanya memiliki sumber daya terbatas dan membatasi sesi login aktif (misal hanya 1 sesi admin sekaligus):

### A. Otentikasi Atomik Menggunakan `Mutex`
Gunakan `kotlinx.coroutines.sync.Mutex` untuk mengunci proses login:
```kotlin
private val authMutex = Mutex()

suspend fun authenticate(): Result<SessionToken> = authMutex.withLock {
    // Jalankan otentikasi sekuensial aman
}
```
Jangan izinkan coroutine paralel memicu login secara bersamaan yang dapat membatalkan token yang sedang aktif (*session thrashing*).

### B. Larangan Re-entrancy pada Semaphore (Anti-Deadlock)
Jika menggunakan `Semaphore` untuk membatasi laju request ke router (misal `Semaphore(2)`):
- **Dilarang memanggil fungsi yang meminta permit semaphore dari dalam blok yang sedang memegang permit semaphore tersebut.**
- Pemanggilan bersarang (*nested permit acquisition*) akan menyebabkan kebuntuan permanen (**Deadlock**), membuat aplikasi macet selamanya.

### C. Pre-Authentication Sebelum Request Paralel
Sebelum memanggil banyak endpoint secara paralel menggunakan `async { ... }`, pastikan token sesi sudah diperoleh terlebih dahulu secara sekuensial.

---

## 2. Reverse-Engineering & Parser Toleran (Robust DTO)

- **Dekode Skema Otentikasi Nyata:**
  Catat endpoint dan skema otentikasi nyata (enkripsi AES, cookie, header unik) ke dalam dokumentasi proyek.
- **Konfigurasi JSON Toleran:**
  Firmware perangkat embedded sering menambahkan atau mengubah field respons secara mendadak:
  ```kotlin
  val tolerantJson = Json {
      ignoreUnknownKeys = true  // Abaikan field baru
      isLenient = true          // Fleksibel terhadap kuotasi longgar
      encodeDefaults = true
      coerceInputValues = true  // Fallback ke default jika tipe tidak cocok
  }
  ```
- **Fallback Halaman HTML:**
  Jika perangkat sedang restart atau maintenance, respons yang dikembalikan sering kali berupa halaman HTML, bukan JSON. Periksa apakah respons diawali `<` sebelum melakukan parsing deserialisasi untuk mencegah crash `SerializationException`.

---

## 3. Komunikasi Jaringan Lokal & Printer POS

- **Cleartext HTTP Traffic:**
  Untuk mengizinkan koneksi HTTP ke gateway IP lokal (seperti `192.168.1.1` atau server lokal), pastikan atribut ini terpasang di `AndroidManifest.xml`:
  ```xml
  <application
      android:usesCleartextTraffic="true"
      ... >
  ```
- **Printer Termal POS (ESC/POS):**
  Untuk komunikasi via Bluetooth SPP (Serial Port Profile) atau soket RAW port 9100, kelola koneksi soket di dalam background dispatcher (`Dispatchers.IO`) dan selalu pastikan soket ditutup dalam blok `finally`.
