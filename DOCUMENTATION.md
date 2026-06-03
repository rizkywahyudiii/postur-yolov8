# Project Documentation

## AI-Based Sitting Posture Analytics Using YOLOv8-Pose

* **Project Type**: Final Project Mata Kuliah
* **Category**: Computer Vision / Machine Learning
* **Team**: Kelompok 4 • Kelas PSIK 23 A
* **Description**: *An AI-based posture analytics system that utilizes YOLOv8-Pose for extracting human pose keypoints and analyzing longitudinal changes in sitting posture quality.*

---

## Project Overview

Project ini merupakan implementasi sistem analisis postur duduk menggunakan YOLOv8-Pose untuk membantu melakukan monitoring kualitas postur selama aktivitas belajar atau bekerja. 

Project ini bertujuan untuk merekam dan menyajikan informasi tren perubahan posisi duduk secara longitudinal (sepanjang waktu sesi). Dengan menggunakan kamera web (*webcam*) standar, sistem dapat melacak pergeseran posisi leher dan punggung secara pasif (*silent tracking*) tanpa interupsi alarm yang dapat mendisrupsi konsentrasi pengguna.

---

## Background

Aktivitas belajar atau bekerja di depan komputer dalam durasi lama sering kali menyebabkan perubahan postur secara tidak sadar akibat kelelahan otot. Pengguna cenderung membungkuk (*slouching*) atau memajukan kepala (*forward head posture*) seiring berjalannya waktu.

Pemeriksaan kualitas postur duduk secara manual sulit dilakukan secara terus-menerus dan bersifat subjektif. Pemanfaatan teknologi *computer vision* berbasis estimasi pose tubuh (*human pose estimation*) dapat digunakan untuk membantu melakukan monitoring postur duduk secara otomatis, objektif, dan non-intrusif.

---

## System Goal

Tujuan utama dari sistem ini adalah:
1. Mendeteksi keypoint tubuh duduk utama menggunakan model pembelajaran mendalam YOLOv8-Pose.
2. Menghitung fitur sederhana seperti kemiringan sudut dari segmen posisi tubuh (*torso* dan *neck*).
3. Memberikan estimasi kualitas postur pengguna berbasis skor ergonomis numerik.
4. Menyimpan riwayat perubahan postur duduk secara berkala untuk dianalisis sebagai grafik longitudinal di akhir sesi.

---

## Model Pipeline

Sistem memproses gambar dari kamera hingga menghasilkan visualisasi grafik dan laporan terstruktur dengan alur kerja berikut:

```
[ Input: Webcam / Gambar ]
           ↓
    [ YOLOv8-Pose ]
           ↓
[ Keypoint Extraction ]
(Head, Shoulder, Spine, Hip)
           ↓
[ Posture Feature Calculation ]
(Torso Angle & Neck Angle)
           ↓
   [ Posture Score ]
(Continuous Linear Penalty)
           ↓
  [ Analytics Report ]
(CSV, PNG Chart, & PDF Document)
```

---

## Dataset & Preprocessing

Project ini menggunakan dataset sekunder publik untuk melatih model pendeteksian letak keypoint tubuh.

* **Dataset**: Sitting Posture - 4 Keypoint
* **Source**: Roboflow Universe (`ikornproject/sitting-posture-rofqf`)
* **Dataset Type**: Public secondary dataset
* **Rasio Data (Split)**:
  * **Train**: 573 gambar
  * **Validation**: 55 gambar
  * **Test**: 27 gambar
  * **Total**: 655 gambar

### Preprocessing (Roboflow)
Pra-pemrosesan data dilakukan secara otomatis sebelum training untuk menyeragamkan dimensi:
* **Auto Orient**: Menormalisasi orientasi sudut gambar agar seragam antar sampel.
* **Resize Stretch**: Mengubah resolusi gambar secara konsisten menjadi $640 \times 640$ piksel untuk menyesuaikan masukan arsitektur YOLOv8.

### Augmentasi Data (Augmentation)
Untuk memperbanyak variabilitas gambar latih karena ukuran dataset yang terbatas:
* **Outputs per training example**: 3
* **Grayscale**: Diterapkan pada 15% gambar latih untuk melatih ketahanan model terhadap warna pakaian atau background.
* **Noise**: Penambahan noise hingga batas 1.53% dari piksel untuk mensimulasikan noise sensor kamera web berkualitas rendah.

*Catatan: Efek noise yang terlihat pada beberapa citra sampel pengujian merupakan hasil augmentasi dataset yang disengaja untuk melatih model, dan bukan merupakan error pada pra-pemrosesan.*

---

## Keypoint Analysis

Sistem mendeteksi koordinat $(x, y)$ untuk 4 keypoint utama yang merepresentasikan posisi duduk:
* **Head** (Kepala): Titik acuan kepala atas/telinga.
* **Shoulder** (Bahu): Titik acuan batas atas torso.
* **Spine** (Tulang Belakang): Titik intermediet kelenturan punggung tengah.
* **Hip** (Pinggul): Titik tumpu bawah pantat pada kursi.

Keempat keypoint tersebut digunakan untuk menghitung fitur kemiringan tubuh:
1. **Torso Angle**: Dihitung tertimbang menggunakan kombinasi segmen bawah (Hip ke Spine) sebesar 30% dan segmen atas (Spine ke bahu) sebesar 70% agar peka mendeteksi bungkukan punggung atas.
2. **Neck Angle**: Dihitung berdasarkan kemiringan sudut kepala terhadap bahu.

Nilai sudut kemiringan ini kemudian dikonversi menjadi draf penalti skor postur kontinu (*Posture Score*) untuk menentukan klasifikasi status: *Excellent* (skor $\ge 80$), *Moderate* (skor $\ge 60$), dan *Poor* (skor $< 60$).

---

## Realtime Monitoring vs Analytics Logging

Sistem dirancang dengan memisahkan fungsi visualisasi langsung dengan fungsi penyimpanan riwayat:

### 1. Realtime Monitoring
* Inferensi pose tubuh berjalan secara *realtime* (per frame) menggunakan umpan video dari webcam.
* Setiap frame diproses secara langsung untuk mengekstraksi koordinat sendi.
* Nilai sudut leher/torso serta indikator status diperbarui secara instan pada tampilan monitor.

### 2. Analytics Logging (Sampling Periodik)
* Untuk tujuan penyimpanan, tidak setiap frame inferensi ditulis ke dalam log database karena akan memakan ruang penyimpanan dan mengandung noise gerakan dinamis instan.
* Sistem melakukan sampling data periodik (misalnya mencatat satu snapshot postur setiap 30 detik untuk produksi).
* **Tujuan Sampling**:
  * Mengurangi noise sensor visual dari gerakan sesaat (misalnya saat merapikan rambut atau memutar tubuh sejenak).
  * Mengurangi ukuran file CSV database penyimpanan.
  * Mendapatkan ringkasan grafik longitudinal yang bersih dan merepresentasikan tren postur sesi belajar/kerja sesungguhnya.

---

## Demo Result & Analysis

Bagian ini menyajikan hasil training dan pengujian sistem yang diintegrasikan ke dalam dasbor website satu halaman:

1. **Training Visualization**: Metrik performa YOLOv8-pose yang dilatih selama 150 epoch mencapai **mAP50 Pose 97.8%**, **Precision 98%**, dan **Recall 86%** dengan selisih validasi loss gap yang rendah sebesar **0.023**.
2. **Realtime Detection Overlay**: Jendela visualisasi penangkap webcam berhasil melacak keypoint dan menampilkan data numerik sudut sendi secara stabil berkat filter rata-rata berjalan 20 frame.
3. **Posture Graph**: Grafik visual longitudinal sumbu ganda (*Double Y-Axis*) memisahkan sumbu skor ergonomis di kiri dan derajat sudut fisik di kanan untuk kemudahan pembacaan data tren degradasi.
4. **PDF Report**: Menghasilkan berkas laporan ringkas sesi yang siap cetak berisi data rata-rata, skor minimum/maksimum, dan indikator awal degradasi postur.

---

## Limitations

* **Dataset Masih Terbatas**: Menggunakan dataset sekunder publik Roboflow sebesar 655 gambar duduk terkontrol, sehingga memerlukan pengujian lebih lanjut untuk skenario duduk luar yang bervariasi.
* **Kondisi Kamera & Lingkungan**: Akurasi pendeteksian dapat terganggu oleh variasi intensitas pencahayaan ruangan, jarak antara pengguna ke kamera, dan pakaian yang terlalu longgar.
* **Ketergantungan Posisi Kamera**: Sudut kamera web harus diposisikan tegak lurus dari arah samping (*lateral view*) pengguna agar estimasi sudut sendi tetap akurat.
* **Bukan Diagnosis Medis**: Skor postur dan tren degradasi yang dihasilkan sistem merupakan estimasi visual ergonomis berbasis keypoint, bukan penilaian klinis atau alat diagnosis medis.

---

## Suggested Presentation Flow (20 Minutes)

Berikut rancangan draf slide presentasi sidang kelompok dengan durasi total maksimal **20 menit**:

* **Slide 1: Problem Introduction (2 Menit)**
  * Menjelaskan bahaya posisi duduk statis yang terlalu lama di depan komputer dan penurunan postur secara tidak sadar.
* **Slide 2: Project Overview & Objectives (2 Menit)**
  * Memaparkan judul proyek final, kontributor kelompok 4 kelas PSIK 23 A, serta tujuan utama pembuatan asisten *silent posture monitoring* longitudinal.
* **Slide 3: Dataset & Preprocessing (2.5 Menit)**
  * Memaparkan penggunaan dataset sekunder publik Roboflow (655 citra), konfigurasi Auto-Orient, Resize 640x640, serta strategi augmentasi grayscale (15%) dan penambahan piksel noise (1.53%).
* **Slide 4: YOLOv8-Pose Pipeline (2.5 Menit)**
  * Menjelaskan pemrosesan inferensi pose *realtime* (per frame) dan layer pencatatan log analitik periodik (setiap 30 detik).
* **Slide 5: Posture Analytics Formulation (2.5 Menit)**
  * Menunjukkan formula perhitungan sudut torso tertimbang ($30\%$ lower, $70\%$ upper), sudut leher, filter smoothing FIFO 20 frame, dan model penilaian kontinu.
* **Slide 6: Demo System (3 Menit)**
  * Menunjukkan jalannya aplikasi python secara langsung menggunakan webcam serta pengoperasian dasbor dokumentasi satu halaman.
* **Slide 7: Result & Discussion (3.5 Menit)**
  * Memaparkan pencapaian metrik latih model YOLOv8 (mAP50 97.8%, Precision 98%), visual grafik longitudinal Double Y-Axis, dan hasil unduhan laporan PDF.
* **Slide 8: Conclusion & Future Work (2 Menit)**
  * Merangkum pencapaian proyek tugas akhir mata kuliah dan rencana pengembangan lebih lanjut (Edge AI dan baseline postur personal).

---

## Team Project Note

This project was developed collaboratively as a team project by Kelompok 4 Kelas PSIK 23 A. 

Each component consists of:
* **Dataset preparation**: Roboflow dataset acquisition, splitting, and augmentation configurations.
* **Model training**: Training YOLOv8n-pose models on PyTorch CUDA with RTX 3050 GPUs.
* **Backend processing**: Managing loop videocapture OpenCV frame feeds, keypoint coordinate parsing, and smoothing filter queues.
* **Analytics module**: Generating dual-axis trend graphs, calculating session stats, exporting PDF/CSV reports, and synchronization controls.
* **Documentation**: Developing the static fullscreen glassmorphism web dasbor presentation and drafting documentations.
