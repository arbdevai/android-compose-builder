# Native Development (C/C++ NDK & Rust) for Android

Panduan ini digunakan ketika aplikasi membutuhkan komputasi performa tinggi, pemrosesan media/audio *low-latency*, kriptografi, atau penggunaan pustaka native yang sudah ada.

---

## 1. Kapan Menggunakan Native Layer?

- **Komputasi Berat & Real-Time:** Audio DSP (Oboe/AAudio), pengolahan citra (OpenCV), kompresi data, dan machine learning on-device.
- **Kriptografi & Security:** Implementasi algoritma enkripsi/hashing yang membutuhkan proteksi terhadap *reverse-engineering* APK.
- **Pustaka Existing:** Mengintegrasikan library C/C++ atau Rust yang stabil tanpa perlu menulis ulang dalam Kotlin.
- **Prinsip Utama:** Jaga *surface area* JNI seminimal mungkin. Seluruh UI dan State Management tetap di Jetpack Compose; native layer hanya menangani komputasi murni.

---

## 2. Arsitektur C / C++ dengan Android NDK & CMake

### A. Konfigurasi `app/build.gradle.kts`
Tambahkan blok `externalNativeBuild` dan batasi arsitektur target (ABI) agar ukuran APK tidak membengkak:

```kotlin
android {
    defaultConfig {
        ndk {
            // Target arsitektur modern Android (64-bit wajib untuk Play Store / device modern)
            abiFilters.addAll(listOf("arm64-v8a", "armeabi-v7a", "x86_64"))
        }
    }

    externalNativeBuild {
        cmake {
            path = file("src/main/cpp/CMakeLists.txt")
            version = "3.22.1"
        }
    }
}
```

### B. Konfigurasi `src/main/cpp/CMakeLists.txt`
```cmake
cmake_minimum_required(VERSION 3.22.1)
project("native_engine")

add_library(
    native_engine
    SHARED
    native-lib.cpp
)

find_library(
    log-lib
    log
)

target_link_libraries(
    native_engine
    ${log-lib}
)
```

### C. Implementasi JNI C++ (`src/main/cpp/native-lib.cpp`)
```cpp
#include <jni.h>
#include <string>
#include <android/log.h>

#define TAG "NativeEngine"
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, TAG, __VA_ARGS__)

extern "C" JNIEXPORT jstring JNICALL
Java_com_example_app_core_NativeBridge_processPayload(
    JNIEnv* env,
    jobject /* this */,
    jstring input
) {
    const char* nativeString = env->GetStringUTFChars(input, nullptr);
    if (nativeString == nullptr) {
        return env->NewStringUTF("");
    }

    std::string result = "Processed: " + std::string(nativeString);
    env->ReleaseStringUTFChars(input, nativeString);

    return env->NewStringUTF(result.c_str());
}
```

### D. Jembatan Kotlin (`NativeBridge.kt`)
```kotlin
package com.example.app.core

object NativeBridge {
    init {
        System.loadLibrary("native_engine")
    }

    external fun processPayload(input: String): String
}
```

---

## 3. Arsitektur Rust di Android (Memory-Safe Core)

Rust sangat direkomendasikan untuk core logic modern karena menjamin *memory safety* tanpa overhead garbage collection (GC).

### Pendekatan yang Direkomendasikan: UniFFI (`mozilla/uniffi-rs`)
UniFFI menghasilkan binding Kotlin secara otomatis dan aman tanpa perlu menulis kode boilerplate JNI manual.

#### A. Konfigurasi `Cargo.toml` pada Crate Rust
```toml
[package]
name = "core_engine"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib", "staticlib"]

[dependencies]
uniffi = { version = "0.28", features = ["cli"] }

[build-dependencies]
uniffi = { version = "0.28", features = ["build"] }
```

#### B. Logika Rust (`src/lib.rs`)
```rust
uniffi::setup_scaffolding!();

#[uniffi::export]
pub fn encrypt_data(payload: String, secret_key: String) -> Result<Vec<u8>, String> {
    if secret_key.len() < 16 {
        return Err("Secret key too short".to_string());
    }
    // Lakukan komputasi/enkripsi
    Ok(payload.as_bytes().to_vec())
}
```

#### C. Kompilasi Target Android Menggunakan `cargo-ndk`
Kompilasi library `.so` untuk setiap target arsitektur:
```bash
# Pastikan toolchain rust android terpasang:
# rustup target add aarch64-linux-android armv7-linux-androideabi x86_64-linux-android

cargo ndk -t arm64-v8a -t armeabi-v7a -t x86_64 -o app/src/main/jniLibs build --release
```

Hasil kompilasi akan tersimpan rapi di:
- `app/src/main/jniLibs/arm64-v8a/libcore_engine.so`
- `app/src/main/jniLibs/armeabi-v7a/libcore_engine.so`
- `app/src/main/jniLibs/x86_64/libcore_engine.so`

Gradle secara otomatis memaketkan seluruh file di `src/main/jniLibs/` ke dalam APK release tanpa memerlukan konfigurasi tambahan.

---

## 4. Checklist Keamanan & Performa Native

1. **Pencegahan JNI Memory Leak:**
   - Selalu pasangkan `GetStringUTFChars` dengan `ReleaseStringUTFChars`.
   - Selalu lepaskan `GetByteArrayElements` dengan mode yang tepat (`JNI_ABORT` jika hanya dibaca, `0` jika dimodifikasi).
2. **Exception Handling:**
   - C++ dan Rust tidak boleh melempar unhandled exception / panic melintasi JNI boundary. Tangkap semua error dan kembalikan kode status atau string error terformat ke Kotlin.
3. **Ukuran Biner:**
   - Gunakan `strip` pada binary release untuk membuang simbol debug.
   - Di `Cargo.toml`:
     ```toml
     [profile.release]
     opt-level = "z"     # Optimalkan ukuran biner
     lto = true          # Link Time Optimization
     codegen-units = 1
     panic = "abort"
     ```
