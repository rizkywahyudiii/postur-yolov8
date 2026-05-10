# Dokumen Perencanaan Penelitian: Posture Degradation Analytics
**Pemanfaatan Deep Learning (YOLOv8-Pose) untuk Analisis Kelelahan Postur Berbasis Web**

---

## 1. Latar Belakang & Urgensi Singkat
Gaya hidup *sedentary* (banyak duduk) telah menjadi rutinitas utama bagi mahasiswa dan pekerja digital. Duduk statis berjam-jam sering kali memicu penurunan kualitas postur secara tidak sadar akibat kelelahan otot inti (*muscle fatigue*), yang berujung pada masalah *Musculoskeletal Disorders* (MSDs) seperti nyeri punggung kronis, kifosis, hingga skoliosis. 

Urgensi dari penelitian ini terletak pada keterbatasan sistem deteksi postur yang ada saat ini. Mayoritas sistem di pasaran bertindak sebagai "alarm" yang memberi peringatan *real-time* saat pengguna membungkuk. Alih-alih membantu, notifikasi konstan ini mendisrupsi fokus (*deep work*) dan sering kali berakhir dimatikan oleh pengguna. Diperlukan pendekatan analitik yang bekerja secara sunyi (*silent background tracking*) untuk mengevaluasi kebiasaan duduk pengguna secara longitudinal tanpa mengganggu produktivitas mereka.

## 2. Kebaruan (Novelty)
Kebaruan penelitian ini adalah pergeseran paradigma dari **"Real-time Alerting System"** menjadi **"Longitudinal Degradation Analytics"**. 
Alih-alih mengeluarkan peringatan biner (Bungkuk/Tegak), sistem mengekstrak data geometris (sudut tulang belakang/leher) secara periodik (misal: 1 frame per menit) selama satu sesi belajar/kerja. Output akhirnya adalah sebuah kurva kelelahan (*fatigue curve*) dan *insight* personal (contoh: "Postur Anda konsisten menurun drastis setelah menit ke-40").

## 3. Target Pengguna & Dampak Temuan (Impact)
* **Target Pengguna:** Mahasiswa, pekerja *remote*, *programmer*, dan individu dengan gaya hidup duduk berjam-jam di depan komputer.
* **Impact:** 1. **Preventif Medis:** Mencegah kelainan bentuk tulang punggung dan nyeri punggung bawah dalam jangka panjang.
  2. **Edukasi Ergonomi:** Memberikan *self-awareness* berbasis data kepada pengguna tentang ketahanan otot mereka sendiri.
  3. **Low-Cost Tech:** Karena beroperasi melalui kamera laptop standar tanpa perangkat IoT atau sensor tambahan, solusi ini sangat *scalable* dan dapat diakses siapa saja secara gratis atau *low-cost*.

---

## 4. Metodologi Penelitian

### A. Tahapan Penelitian
1. **Pengumpulan & Persiapan Data:** Menggunakan dataset *Sitting Posture* beranotasi dari sumber terbuka (seperti Roboflow atau Kaggle).
2. **Preprocessing:** *Resizing* gambar, augmentasi data (rotasi ringan, penyesuaian kecerahan) untuk mensimulasikan kondisi pencahayaan kamar yang berbeda.
3. **Training Model Deep Learning:** Melakukan *fine-tuning* pada pre-trained model **YOLOv8-Pose** menggunakan GPU RTX 3050 untuk mendeteksi *keypoints* tubuh (mata, telinga, bahu, pinggul) pada posisi duduk.
4. **Feature Engineering (Ekstraksi Geometris):** Menulis algoritma (menggunakan Trigonometri/Numpy) untuk menghitung sudut postur leher dan punggung berdasarkan koordinat *keypoints* dari keluaran YOLO.
5. **Klasifikasi Analitik:** Menentukan *threshold* (ambang batas) sudut untuk mengklasifikasikan tingkat keparahan postur (Tegak, Kelelahan Ringan, Bungkuk Parah).
6. **Integrasi & Visualisasi Sistem:** Membangun *dashboard* web untuk memvisualisasikan data sesi menjadi grafik tren (*timeline graph*) dan kesimpulan analitik.

### B. Alur Sistem (System Flow)
`Mulai Sesi (User)` 
-> `Webcam aktif di background` 
-> `Capture 1 Frame per 60 detik` 
-> `Inference YOLOv8 (Ekstraksi Titik Sendi)` 
-> `Kalkulasi Sudut Kemiringan Tubuh` 
-> `Simpan Data (Timestamp, Derajat Sudut)` 
-> `Sesi Selesai` 
-> `Generate Laporan Grafik Penurunan Postur` 
-> `Tampilkan Insight & Saran Ergonomi`

---

## 5. Kebutuhan Library & Hardware

**Hardware:**
* GPU: NVIDIA GeForce RTX 3050 (Digunakan penuh untuk akselerasi *training* CUDA).
* RAM: Min. 8GB/16GB.

**Environment & Core Libraries (Python):**
* `ultralytics` : Framework utama untuk menjalankan dan mentraining YOLOv8.
* `torch` & `torchvision` : Harus versi yang mendukung CUDA (PyTorch with CUDA 11.x/12.x) agar RTX 3050 terbaca.
* `opencv-python` (cv2) : Untuk manipulasi *frame* gambar/webcam.
* `numpy` : Untuk komputasi matematis menghitung sudut antar titik (*keypoints*).
* `pandas` : Untuk menyimpan *log* data (menit ke-X, sudut Y) menjadi format tabular (CSV) sebelum diolah menjadi grafik.
* `matplotlib` / `seaborn` : Untuk memvisualisasikan grafik *fatigue curve* (jika dilakukan di Python/Jupyter Notebook).

---

## 6. Setup Environment & Struktur Direktori (VSCode)

### Perintah Setup Virtual Environment (Terminal VSCode):
1. Buat Virtual Environment: `python -m venv venv`
2. Aktivasi venv (Windows): `.\venv\Scripts\activate`
3. Install PyTorch untuk RTX 3050 (contoh CUDA 11.8): `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`
4. Install Ultralytics & dependensi: `pip install ultralytics opencv-python numpy pandas matplotlib`

### Struktur Direktori Proyek:
```text
posture-analytics-project/
│
├── venv/                   # Folder Virtual Environment (Jangan di-commit ke Git)
├── data/                   # Dataset lokal
│   ├── raw/                # Dataset asli (gambar + label YOLO)
│   └── processed/          # Dataset yang sudah di-preprocess/augmentasi
│
├── notebooks/              # Jupyter notebooks untuk eksperimen & testing algoritma sudut
│   └── 01_yolo_testing.ipynb
│
├── src/                    # Source code utama
│   ├── detect_pose.py      # Script untuk inference YOLO
│   ├── calc_angle.py       # Script hitungan matematika sudut leher/punggung
│   └── tracker.py          # Script simulasi sesi (ngambil frame per menit)
│
├── models/                 # Tempat menyimpan file model hasil training (.pt atau .onnx)
│   └── best_yolov8_posture.pt
│
├── .gitignore              # Mengabaikan venv, data/, dan __pycache__
├── requirements.txt        # Daftar library (pip freeze > requirements.txt)
└── README.md               # Dokumentasi utama proyek