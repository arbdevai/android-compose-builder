# Android Compose Builder — Pro

Paket berbayar di atas skill Gratis. Semua isi folder `pro/` dilisensikan
di bawah [LICENSE-COMMERCIAL.md](../LICENSE-COMMERCIAL.md) — **bukan MIT**,
dan **tidak boleh didistribusikan ulang**.

## Isi paket Pro

| Item | Lokasi | Keterangan |
| --- | --- | --- |
| Template Kasir | `templates/kasir/` | Aplikasi kasir offline lengkap: produk, keranjang, checkout atomik Room, riwayat + total pendapatan |
| Scaffold Pro | `scripts/scaffold_pro_template.py` | Buat proyek dari template Pro + tambah Room/KSP + linter pre-flight |
| Panduan Play Store & Monetisasi | `references/play-store-monetization.md` | AAB, checklist Play Console, jalur rilis bertahap, model monetisasi |
| Panduan Production Hardening | `references/production-hardening.md` | R8/minify, crash reporting, ukuran aplikasi, ANR, keamanan data lokal |
| Addendum skill Pro | `SKILL-PRO.md` | Instruksi agent untuk memakai template dan referensi Pro |

## Cara memakai (setelah membeli)

1. Unduh paket Pro (file ZIP) dari tautan pembelian.
2. Ekstrak di samping instalasi skill Gratis, atau jalankan scaffold
   langsung dari folder `pro/` hasil ekstrak:

```bash
python3 pro/scripts/scaffold_pro_template.py --template kasir \
  --dir /path/ke/proyek/baru --name "KasirKu" --package com.toko.kasirku
```

3. Lanjutkan seperti proyek skill biasa: commit `Release v1.0.0`, push,
   CI build APK.

## Distribusi

- Folder `pro/` **tidak** ikut terpasang oleh installer Gratis
  (`install.sh` / `install.py` mengecualikan `pro/`).
- File Pro hanya didistribusikan sebagai paket ZIP berbayar (Gumroad /
  Lemon Squeezy, lihat `PRICING.md`). Jangan commit folder `pro/` ke
  repositori publik tanpa lisensi komersial yang menyertainya.
- Pembeli mendapat update Pro selama 12 bulan sejak pembelian.
