# Image Processor Application

Aplikasi pengolahan gambar sederhana yang dibuat menggunakan PyQt5 dan OpenCV. Aplikasi ini memungkinkan pengguna untuk meng-upload gambar, menampilkan histogram warna gambar, melakukan histogram equalization, dan menampilkan hasil equalization serta histogramnya.

## Fitur

- **Upload Image:** Upload gambar dari sistem file.
- **Histogram Warna:** Tampilkan histogram warna untuk gambar yang di-upload.
- **Histogram Equalization:** Terapkan histogram equalization pada gambar dan tampilkan histogram hasilnya.
- **Gambar Equalized:** Tampilkan gambar setelah proses equalization.

## Prerequisites

Pastikan Python 3 sudah terinstall di sistem Anda. Selain itu, Anda memerlukan beberapa paket Python yang harus diinstal:

- `PyQt5`
- `opencv-python`
- `matplotlib`

## Instalasi

1. **Clone repository:**
   ```bash
   git clone histogram_equalizer
   cd histogram_equalizer

2. **Buat dan aktifkan virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Untuk Windows: venv\Scripts\activate

3. **Install dependencies:**
    ```bash
    pip install PyQt5 opencv-python matplotlib


## Menjalankan Aplikasi

1. **Navigasikan ke direktori yang berisi file main.py:**
    ```bash
    cd histogram_equalizer

2. **Jalankan aplikasi:**
    ```bash
    python main.py

3. **Gunakan aplikasi:**
    - Klik tombol Upload Image untuk memilih gambar dari file system Anda.
    - Aplikasi akan menampilkan gambar yang di-upload, histogram warna, gambar hasil equalization, dan histogram equalization.

## Struktur Proyek
    - `main.py`: Script utama yang menjalankan aplikasi.
    - `requirements.txt`: Daftar dependensi (jika ada).
## Catatan
    - Pastikan Anda memiliki hak akses untuk membaca gambar dari direktori yang Anda pilih saat melakukan upload.
    - Gambar yang di-upload harus dalam format yang didukung oleh OpenCV (.png, .jpg, .jpeg, .bmp).

## Penulis
    affan-ai