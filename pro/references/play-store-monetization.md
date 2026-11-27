# Play Store & Monetisasi (Pro)

Panduan rilis aplikasi Android ke Google Play dan menghasilkan uang dari
aplikasi — checklist yang dipakai saat merilis aplikasi Pro.

## 1. Format rilis: AAB, bukan APK

- Google Play **wajib** menerima Android App Bundle (`.aab`), bukan APK.
- Workflow CI di skill ini build APK untuk GitHub Release. Untuk Play,
  tambahkan job kedua di `.github/workflows/build-apk.yml`:

```yaml
bundleRelease:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-java@v4
      with:
        distribution: temurin
        java-version: 17
    - name: Build AAB
      run: ./gradlew bundleRelease
```

- Aktifkan signing yang sama dengan APK (keystore dari
  `setup_release_keystore.py`). **Satu keystore untuk satu aplikasi,
  selamanya.** Kehilangan keystore = tidak bisa update aplikasi lagi.
- Aktifkan Play App Signing di Play Console (Google yang menyimpan kunci
  upload; kunci signing asli tetap di tanganmu).

## 2. Checklist Play Console sebelum submit

1. **Nama paket final** — tidak bisa diubah setelah rilis pertama.
2. **versionCode monotonik** — rumus skill: `MAJOR * 10000 + MINOR * 100 + PATCH`.
3. **Ikon + feature graphic** — ikon adaptif dari
   `generate_launcher_icons.py`; feature graphic 1024x500 tanpa teks kecil.
4. **Screenshot** — minimal 2 (ponsel), tampilkan layar utama + satu fitur
   kunci. Tanpa data dummy di screenshot.
5. **Deskripsi** — kalimat pertama menjelaskan manfaat, bukan fitur.
   Contoh: "Kasir offline untuk toko kelontong: catat penjualan tanpa internet."
6. **Kategori + tag** — pilih kategori yang paling dekat; jangan asal.
7. **Kebijakan privasi** — wajib bila aplikasi meminta izin apa pun atau
   memakai iklan/analytics. Tulis halaman sederhana, host di GitHub Pages
   atau situsmu.
8. **Data safety** — isi formulir dengan jujur: data apa yang dikumpulkan,
   apakah dibagikan ke pihak ketiga.
9. **Target audiens + rating konten** — isi kuesioner dengan benar.
10. **Internal testing dulu** — rilis ke internal track (maks 100 tester),
    perbaiki crash, baru naik ke production.

## 3. Jalur rilis bertahap

Internal track -> Closed testing -> Open testing -> Production bertahap
(10% -> 50% -> 100%). Jangan langsung 100% di rilis pertama.

## 4. Monetisasi — pilih SATU dulu

| Model | Cocok untuk | Catatan |
| --- | --- | --- |
| Sekali bayar | Aplikasi utilitas | Paling sederhana, tanpa server |
| In-app purchase (consumable) | Fitur/konten tambahan | Pakai Google Play Billing Library |
| Langganan | Konten/layanan berkelanjutan | Butuh backend verifikasi; jangan simpan status langganan hanya di lokal |
| Iklan (AdMob) | Aplikasi gratis bervolume | Jangan pasang iklan di layar bayar/checkout; patuhi kebijakan keluarga bila audiens anak |

### Aturan monetisasi

- **Jangan** meminta pembayaran di luar Play Billing untuk konten digital
  di dalam aplikasi — melanggar kebijakan Play.
- Harga dalam Rupiah: uji di beberapa titik harga (mis. Rp15.000 vs
  Rp29.000) sebelum menetap.
- Untuk aplikasi kasir/toko: model sekali bayar atau langganan tahunan
  lebih diterima daripada iklan.

## 5. Setelah rilis

- Pantau **Android Vitals** (crash rate, ANR) setiap hari di minggu pertama.
- Crash rate di atas 1,09% (ambang buruk Play) menurunkan visibilitas.
- Balas ulasan bintang 1-2 dalam 24 jam; perbaiki, lalu minta update ulasan.
- Rilis perbaikan kecil cepat (patch version) lebih baik daripada menunda
  satu rilis besar.
