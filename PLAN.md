# Posture Degradation Analytics
## Pemanfaatan Deep Learning YOLOv8-Pose untuk Analisis Perubahan Sudut Postur Duduk Secara Longitudinal Berbasis Webcam

---

# 1. Latar Belakang

Aktivitas sedentary seperti belajar, bekerja di depan komputer, dan penggunaan perangkat digital dalam durasi panjang dapat menyebabkan penurunan kualitas postur tubuh secara bertahap akibat kelelahan otot (*muscle fatigue*). Kondisi ini dapat memicu gangguan *Musculoskeletal Disorders* (MSDs) seperti nyeri punggung bawah, forward head posture, kifosis, hingga skoliosis.

Sebagian besar sistem deteksi postur saat ini menggunakan pendekatan *real-time alerting*, yaitu memberikan notifikasi langsung ketika pengguna mulai membungkuk. Namun pendekatan tersebut cenderung mengganggu fokus pengguna saat belajar atau bekerja karena notifikasi muncul secara terus-menerus.

Proyek ini mengusulkan pendekatan berbeda berupa *silent longitudinal posture analytics*, yaitu sistem yang melakukan pemantauan postur secara pasif di background tanpa memberikan alarm real-time. Sistem akan merekam perubahan sudut postur pengguna secara berkala selama sesi belajar atau bekerja, kemudian menghasilkan insight ergonomi berdasarkan pola perubahan sudut tubuh pengguna.

---

# 2. Kebaruan (Novelty)

Kebaruan penelitian ini terletak pada perubahan paradigma dari:

"Real-time posture alert system"

menjadi:

"Longitudinal posture degradation analytics"

Sistem tidak berfokus pada pemberian alarm ketika postur salah, melainkan melakukan analisis perubahan sudut postur tubuh pengguna selama durasi aktivitas tertentu.

Contoh insight yang dihasilkan:

- Pengguna mulai mengalami penurunan kualitas postur pada menit ke-35
- Pengguna mampu mempertahankan postur optimal selama 35 menit
- Terjadi peningkatan sudut kemiringan tubuh secara signifikan setelah durasi tertentu

---

# 3. Tujuan Penelitian

1. Mengembangkan sistem analisis postur duduk berbasis YOLOv8-Pose.
2. Mengekstraksi keypoint tubuh manusia menggunakan pose estimation.
3. Menghitung perubahan sudut postur tubuh selama sesi belajar atau bekerja.
4. Memvisualisasikan data perubahan postur dalam bentuk tabel dan grafik longitudinal.
5. Memberikan insight ergonomi berdasarkan pola perubahan sudut tubuh pengguna.

---

# 4. Metodologi Penelitian

## A. Pengumpulan Dataset

Dataset yang digunakan merupakan dataset primer yang dikumpulkan secara mandiri menggunakan webcam atau kamera laptop.

Dataset terdiri dari:

- Posisi duduk tegak
- Sedikit membungkuk
- Membungkuk parah
- Sudut pengambilan kiri dan kanan
- Variasi pencahayaan
- Variasi jarak kamera

Jumlah dataset awal:

- 50–100 gambar original

---

## B. Anotasi Keypoint

Dataset dianotasi menggunakan Roboflow dengan metode auto-annotation berbasis pretrained human pose estimation model.

Langkah anotasi:

1. Upload dataset primer ke Roboflow
2. Menggunakan auto-label pose estimation
3. Sistem menghasilkan 17 keypoints format COCO
4. Melakukan koreksi manual terhadap keypoint yang kurang akurat
5. Export dataset ke format YOLOv8 Pose

Format keypoint mengikuti standar COCO 17 Keypoints:

- Nose
- Left Eye
- Right Eye
- Left Ear
- Right Ear
- Left Shoulder
- Right Shoulder
- Left Elbow
- Right Elbow
- Left Wrist
- Right Wrist
- Left Hip
- Right Hip
- Left Knee
- Right Knee
- Left Ankle
- Right Ankle

---

## C. Data Augmentation

Augmentasi dilakukan menggunakan Roboflow untuk meningkatkan variasi dataset dan meningkatkan robustness model terhadap kondisi lingkungan berbeda.

Teknik augmentasi yang digunakan:

1. Original Image
2. Brightness Increase
3. Brightness Decrease
4. Contrast Enhancement
5. Rotation +5 Degree
6. Rotation -5 Degree
7. Gaussian Noise
8. Gaussian Blur
9. Horizontal Flip

Vertical flip tidak digunakan karena menghasilkan pose manusia yang tidak realistis.

Seluruh transformasi augmentasi dilakukan secara otomatis dengan penyesuaian keypoint pose secara dinamis oleh sistem Roboflow.

---

## D. Training Model Deep Learning

Model utama yang digunakan adalah:

YOLOv8n-pose

Model digunakan untuk mendeteksi keypoint tubuh manusia berbasis format COCO 17 Keypoints.

Alasan pemilihan model:

- Lightweight
- Cepat untuk training
- Cocok untuk GPU RTX 3050
- Mendukung pose estimation COCO 17 Keypoints
- Cocok untuk dataset skala kecil hingga menengah

Training dilakukan menggunakan GPU NVIDIA RTX 3050 dengan framework Ultralytics YOLOv8.

---

## E. Feature Engineering

Sistem akan menghitung sudut postur tubuh berdasarkan koordinat keypoint hasil pose estimation.

Keypoint utama yang digunakan dalam analisis:

- Shoulder
- Hip
- Ear / Nose

Contoh analisis sudut:

- Neck Inclination Angle
- Torso Lean Angle
- Shoulder Slope

Perhitungan sudut dilakukan menggunakan pendekatan trigonometri dan komputasi vektor menggunakan NumPy.

---

## F. Longitudinal Posture Analytics

Sistem bekerja secara pasif di background tanpa memberikan notifikasi real-time.

Alur sistem:

User belajar / bekerja
↓
Webcam aktif di background
↓
Capture frame setiap 1 menit
↓
YOLOv8n-pose melakukan inference
↓
Ekstraksi keypoint tubuh
↓
Perhitungan sudut postur tubuh
↓
Penyimpanan data longitudinal
↓
Visualisasi grafik perubahan sudut
↓
Generate insight ergonomi pengguna

Data perubahan sudut postur akan disimpan secara periodik dan divisualisasikan dalam bentuk grafik longitudinal.

---

# 5. Output Sistem

Sistem menghasilkan:

1. Data tabel perubahan sudut postur
2. Grafik longitudinal perubahan postur
3. Insight ergonomi pengguna

Contoh output:

- "Postur mulai menurun pada menit ke-35"
- "Pengguna mempertahankan postur optimal selama 35 menit"
- "Terjadi peningkatan torso lean angle setelah 40 menit"

---

# 6. Kebutuhan Hardware

- GPU NVIDIA RTX 3050
- RAM minimal 8GB
- Webcam Laptop / External Camera

---

# 7. Environment dan Library

## Core Libraries

- ultralytics
- torch
- torchvision
- opencv-python
- numpy
- pandas
- matplotlib
- seaborn

## Install Dependencies

```bash
pip install ultralytics opencv-python numpy pandas matplotlib seaborn
```

## Install PyTorch CUDA

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

# 8. Struktur Direktori

```text
cv-posture/
│
├── data/
│   ├── train/
│   │   ├── images/
│   │   └── labels/
│   ├── valid/
│   │   ├── images/
│   │   └── labels/
│   ├── test/
│   │   ├── images/
│   │   └── labels/
│   └── data.yaml
│
├── notebooks/
│   └── main.ipynb
│
├── runs/
│
├── src/
│   ├── inference.py
│   ├── posture_angle.py
│   ├── tracker.py
│   └── visualization.py
│
├── README.md
├── PLAN.md
└── requirements.txt
```

---

# 9. Target Penelitian

Penelitian diharapkan mampu menghasilkan sistem monitoring postur berbasis AI yang:

- Tidak mengganggu fokus pengguna
- Mampu memvisualisasikan penurunan kualitas postur secara longitudinal
- Memberikan insight ergonomi personal berbasis data
- Dapat digunakan sebagai sistem preventif terhadap gangguan postur tubuh akibat aktivitas sedentary