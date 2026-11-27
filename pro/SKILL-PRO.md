# Android Compose Builder — Pro Addendum

Dokumen ini adalah tambahan untuk `SKILL.md` (Gratis). Agent WAJIB membaca
`SKILL.md` dan semua aturannya terlebih dahulu — semua aturan Gratis
(zero local build, zero dummy data, anti-AI-slop, skeleton shimmer,
pre-flight linter) berlaku penuh untuk pekerjaan Pro.

## 1. Apa itu Pro

Pro adalah paket berbayar di atas skill Gratis: template aplikasi lengkap
siap rilis + panduan production + script scaffold. Lisensi Pro diatur di
`LICENSE-COMMERCIAL.md` — Pro **bukan** MIT dan **tidak boleh**
didistribusikan ulang.

## 2. Template yang tersedia

| Template | Lokasi | Deskripsi |
| --- | --- | --- |
| kasir | `pro/templates/kasir/` | Aplikasi kasir offline: produk, keranjang, checkout atomik Room, riwayat + total pendapatan |

Scaffold template Pro:

```bash
python3 pro/scripts/scaffold_pro_template.py --template kasir \
  --dir /path/ke/proyek/baru --name "KasirKu" --package com.toko.kasirku
```

JANGAN salin file template manual — script scaffold juga menambahkan
dependensi Room + KSP dan menjalankan `verify_kotlin_syntax.py` (0 hard
error) sebelum selesai.

## 3. Referensi Pro (baca sesuai kebutuhan)

| Kebutuhan | Dokumen |
| --- | --- |
| Rilis ke Play Store + monetisasi | `pro/references/play-store-monetization.md` |
| Pengerasan production (R8, crash, ANR, keamanan) | `pro/references/production-hardening.md` |

## 4. Aturan tambahan Pro

- Template Pro adalah titik awal, bukan hasil akhir. Sesuaikan nama,
  warna, dan alur dengan PRD pengguna — tetap lewat wawancara PRD
  (`docs/PRD.md`) seperti aturan skill Gratis.
- Jangan menambahkan data dummy ke template (produk contoh, transaksi
  contoh). Database template dimulai kosong.
- Bila pengguna meminta fitur di luar template (mis. printer thermal,
  barcode scanner), kombinasikan dengan referensi Gratis yang relevan
  (`references/hardware_and_iot.md`).
