# Template Kasir (Pro) — Aplikasi Kasir Offline Siap Rilis

Template aplikasi kasir offline lengkap berbasis Room + Jetpack Compose,
dibangun mengikuti semua aturan skill android-compose-builder (Gratis):
zero dummy data, skeleton shimmer, tanpa emoji, warna netral murni.

## Fitur

- **Produk**: tambah produk (nama, harga Rupiah, stok), hapus produk.
- **Keranjang**: tambah/kurangi jumlah, validasi stok, total otomatis.
- **Checkout atomik**: kurangi stok + simpan penjualan + simpan item dalam
  satu transaksi Room. Gagal bila stok tidak mencukupi — tidak ada
  penjualan setengah jadi.
- **Riwayat**: daftar transaksi + total pendapatan (SUM dari database).
- **Tema**: dark theme netral murni (`#121212` / `#1E1E1E`), tanpa navy kebiruan.

## Cara memakai

Gunakan script scaffold Pro (jangan salin manual):

```bash
python3 pro/scripts/scaffold_pro_template.py --template kasir \
  --dir /path/ke/proyek/baru --name "KasirKu" --package com.toko.kasirku
```

Script akan: membuat proyek dasar dengan generator Gratis, menempel template
ini, menambahkan dependensi Room + KSP ke `gradle/libs.versions.toml` dan
`app/build.gradle.kts`, lalu menjalankan `verify_kotlin_syntax.py`
(0 hard error sebelum selesai).

## Struktur

```text
app/src/main/java/<package>/
├── MainActivity.kt            # NavHost + bottom bar (Produk / Keranjang / Riwayat)
├── data/
│   ├── Product.kt             # @Entity produk
│   ├── Sale.kt                # @Entity penjualan + item penjualan
│   ├── KasirDao.kt            # DAO (suspend DELETE/UPDATE mengembalikan Int)
│   ├── KasirDatabase.kt       # RoomDatabase singleton
│   └── KasirRepository.kt     # Satu-satunya pintu ViewModel ke database
└── ui/
    ├── KasirViewModel.kt      # StateFlow + keranjang + checkout
    ├── ProductsScreen.kt      # Daftar produk + dialog tambah + skeleton
    ├── CartScreen.kt          # Keranjang + bayar
    ├── HistoryScreen.kt       # Riwayat + total pendapatan
    ├── Format.kt              # formatRupiah()
    └── theme/Theme.kt         # KasirTheme (dark netral murni)
```

## Catatan

- Database dimulai **kosong**. Tidak ada produk contoh — sesuai aturan
  zero dummy data. Tambahkan produk pertama dari layar Produk.
- Harga memakai `Long` dalam Rupiah (tanpa desimal).
- Versi Room yang ditambahkan scaffold: Room 2.7.0 + KSP (KSP1,
  `ksp.useKSP2=false`, sesuai standar skill).
