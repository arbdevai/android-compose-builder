# Android Compose UI/UX & Design System

Panduan standar antarmuka Jetpack Compose Material3: bebas *AI Slop*, bebas emoji dekoratif, performan, dan berorientasi produksi profesional.

---

## 1. Kebijakan Anti "AI Slop" & Standar Desain Visual

- **DILARANG ELEMEN DEKORATIF TIDAK PENTING:**
  - **Dilarang** menyematkan efek *pulsing green dot* (titik hijau berkedip/berdenyut seperti template web), glowing borders, atau animasi tanpa tujuan fungsional.
  - Setiap animasi harus memiliki tujuan UX yang jelas (misalnya umpan balik sentuhan/ripple, transisi layar, atau progres muat data).
- **DILARANG EMOJI DEKORATIF:**
  - **Jangan pernah** menempatkan emoji (seperti 🚀, ✨, 📦, 🛠️, 🎉) di judul halaman, tombol aksi, dialog, maupun label form.
  - Selalu gunakan **Vector Icon** resmi dari `androidx.compose.material.icons.filled.*` / `outlined.*` atau resource XML Vector Drawable di `res/drawable/`.
- **DILARANG POLA "TAILWIND / SAAS TINT SLOP" (LARANGAN HITAM KEBIRUAN & TINT TRANSPARAN):**
  - **Latar Belakang Netral Murni (Zero Color Tint):** Dilarang memakai warna hitam kebiruan/navy gelap (seperti `#0F172A`, `#111622`, `#1E293B`, atau sejenisnya) untuk dark mode aplikasi maupun ikon launcher. Gunakan skala abu-abu/hitam murni di mana nilai R=G=B: `#000000` (True OLED), `#121212` (Google Material Dark), atau `#181818`.
  - **Larangan Kartu Berwarna Transparan (Anti-Glassmorphism Sirup):** Jangan pernah membungkus kartu status/alert dengan background warna hijau/merah/kuning transparan (contoh: `Color(0xFF10B981).copy(alpha = 0.12f)` + border hijau transparan). Ini adalah pola web micro-SaaS murahan. Di Android native, gunakan warna permukaan solid Material 3 (`surfaceVariant` / `surfaceContainer`) dan nyatakan status melalui teks atau ikon aksen kecil yang proporsional.
- **Adaptive Vector Icon untuk Launcher:**
  - Ikon aplikasi wajib mengikuti spesifikasi Android Adaptive Icon di `res/mipmap-anydpi-v26/ic_launcher.xml`.
  - Pisahkan background dan foreground bersih (kanvas 108dp dengan safe zone 72dp).
  - Background ikon launcher wajib berwarna solid murni (misal `#000000` atau `#121212`), tanpa campuran saturasi biru/cyan atau gradasi artificial.

---

## 2. Skeleton Screen (Shimmer Effect) & Anti-Loading Spinner

### A. Larangan Layar Kosong dengan Spinner
- **DILARANG SPINNER LAYAR PENUH:** Jangan pernah menampilkan `CircularProgressIndicator` besar di tengah layar kosong saat memuat konten awal. Ini membuat aplikasi terkesan usang dan memicu *content jumping* saat data muncul.
- **Gunakan Skeleton Shimmer:** Gantikan layar loading dengan kerangka tata letak (*skeleton*) yang meniru bentuk konten asli yang sedang dimuat.

### B. Implementasi Murni Jetpack Compose (Zero External Dependency)
Gunakan ekstensi modifier berikut:

```kotlin
import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.material3.MaterialTheme
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.composed
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.layout.onGloballyPositioned
import androidx.compose.ui.unit.IntSize

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

### C. Komponen Skeleton Standar (`ui/components/SkeletonComponents.kt`)
Sediakan komponen dasar:
- `SkeletonBox(modifier, shape)`: Placeholder teks atau tombol.
- `SkeletonCard(modifier)`: Placeholder kartu ringkasan/metrik.
- `SkeletonListItem()`: Placeholder baris data dalam `LazyColumn`.

*Catatan:* `CircularProgressIndicator` kecil (16dp–20dp) hanya diizinkan di dalam tombol aksi saat proses submit/saving sedang berlangsung.

---

## 3. Transisi Layar & Penanganan Tombol Kembali

- **Transisi Halus (`AnimatedContent`):**
  - Hindari pergantian layar instan tanpa transisi.
  - Gunakan directional slide + fade:
    ```kotlin
    AnimatedContent(
        targetState = currentScreen,
        transitionSpec = {
            (slideInHorizontally { width -> width } + fadeIn()).togetherWith(
                slideOutHorizontally { width -> -width } + fadeOut()
            )
        },
        label = "screenTransition"
    ) { screen ->
        // Render Screen
    }
    ```
- **Aturan Navigasi & BackHandler:**
  - Sub-halaman wajib menangani `BackHandler { ... }` untuk kembali ke dashboard sebelum keluar aplikasi.
  - **Jangan pernah** menaruh tombol "Keluar" atau "Exit" di `TopAppBar` pada aplikasi standar mobile, kecuali secara eksplisit diminta untuk mode Kiosk/POS.

---

## 4. Keyboard & Soft Input Handling

Cegah keyboard menutupi input field atau tombol submit:
- Pada formulir input, pasang modifier:
  ```kotlin
  Modifier
      .fillMaxSize()
      .imePadding()
      .verticalScroll(rememberScrollState())
  ```
- Di `AndroidManifest.xml` pada activity utama:
  ```xml
  android:windowSoftInputMode="adjustResize"
  ```
- Tutup keyboard saat menyentuh area luar input menggunakan `LocalFocusManager.current.clearFocus()`.

---

## 5. Standar Bahasa & Microcopy Profesional (Anti-Alay)

Bahasa antarmuka wajib lugas, to-the-point, dan sopan:

| Konteks | ❌ Dilarang (Alay / Lebay / Khas AI) | ✅ Standar Profesional |
| :--- | :--- | :--- |
| **Teks Tombol** | "Yuk Bayar Sekarang Juga Kakak Sayang ✨" | "Bayar Sekarang", "Konfirmasi" |
| **Error Server** | "Aduh maaf servernya lagi bobo cantik nih 💔" | "Server sedang dalam pemeliharaan." |
| **Error Jaringan**| "Koneksi internetmu hilang ditelan bumi..." | "Koneksi terputus. Periksa sinyal internet Anda." |
| **Input/Hint** | "Ketik nomor tercintamu di sini ya..." | "Masukkan Nomor Pelanggan" |
| **Status Berhasil**| "Horeee berhasil banget dong kak! 🎉" | "Transaksi Berhasil" |
| **Konfirmasi** | "Yakin nih mau ninggalin aplikasi yang unyu?"| "Konfirmasi: Lanjutkan tindakan ini?" |
