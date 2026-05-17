# BAB I — PENDAHULUAN

## 1.1 Latar Belakang

Perkembangan teknologi digital menyebabkan meningkatnya aktivitas sedentary seperti belajar, bekerja, dan penggunaan komputer dalam durasi panjang. Mahasiswa, pekerja remote, programmer, dan pengguna komputer lainnya sering menghabiskan waktu berjam-jam dalam posisi duduk statis di depan layar. Kondisi tersebut dapat memicu penurunan kualitas postur tubuh secara bertahap akibat kelelahan otot (muscle fatigue).

Postur duduk yang buruk dalam jangka panjang dapat menyebabkan berbagai gangguan Musculoskeletal Disorders (MSDs) seperti nyeri punggung bawah, forward head posture, kifosis, hingga skoliosis. Salah satu penyebab utama gangguan tersebut adalah kurangnya kesadaran pengguna terhadap perubahan postur tubuh selama aktivitas berlangsung.

Sebagian besar sistem monitoring postur yang ada saat ini menggunakan pendekatan real-time alerting, yaitu memberikan notifikasi langsung ketika pengguna mulai membungkuk. Namun pendekatan tersebut sering kali mengganggu fokus pengguna saat belajar atau bekerja karena notifikasi muncul secara terus-menerus.

Berdasarkan permasalahan tersebut, penelitian ini mengusulkan pendekatan silent longitudinal posture analytics berbasis computer vision menggunakan YOLOv8-Pose. Sistem akan melakukan pemantauan postur tubuh secara pasif menggunakan webcam tanpa memberikan alarm real-time. Sistem akan merekam perubahan sudut postur tubuh pengguna secara berkala selama sesi belajar atau bekerja, kemudian menghasilkan visualisasi data longitudinal dan insight ergonomi berdasarkan perubahan sudut tubuh pengguna.

Penelitian ini diharapkan dapat memberikan solusi monitoring postur yang lebih nyaman, non-intrusif, dan mampu meningkatkan kesadaran pengguna terhadap kualitas postur tubuh mereka selama aktivitas sedentary.

---

## 1.2 Rumusan Masalah

Berdasarkan latar belakang yang telah dijelaskan, maka rumusan masalah pada penelitian ini adalah:

1. Bagaimana menerapkan YOLOv8-Pose untuk mendeteksi keypoint tubuh manusia pada posisi duduk?
2. Bagaimana menghitung perubahan sudut postur tubuh berdasarkan keypoint hasil pose estimation?
3. Bagaimana memvisualisasikan perubahan sudut postur tubuh secara longitudinal selama sesi belajar atau bekerja?
4. Bagaimana menghasilkan insight ergonomi berdasarkan pola perubahan sudut postur tubuh pengguna?

---

## 1.3 Tujuan Penelitian

Tujuan penelitian ini adalah:

1. Mengembangkan sistem analisis postur duduk berbasis YOLOv8-Pose.
2. Mengekstraksi keypoint tubuh manusia menggunakan pose estimation.
3. Menghitung perubahan sudut postur tubuh secara periodik.
4. Memvisualisasikan perubahan sudut postur dalam bentuk grafik longitudinal.
5. Memberikan insight ergonomi berdasarkan perubahan sudut postur tubuh pengguna.

---

## 1.4 Manfaat Penelitian

### 1.4.1 Manfaat Teoritis

Penelitian ini diharapkan dapat memberikan kontribusi dalam pengembangan penelitian computer vision, khususnya pada bidang human pose estimation dan analisis postur tubuh berbasis deep learning.

### 1.4.2 Manfaat Praktis

1. Membantu pengguna memahami perubahan kualitas postur tubuh selama aktivitas sedentary.
2. Memberikan monitoring postur tanpa mengganggu fokus pengguna.
3. Menjadi sistem preventif terhadap gangguan postur tubuh akibat kebiasaan duduk yang buruk.

---

## 1.5 Batasan Masalah

Batasan masalah pada penelitian ini adalah:

1. Sistem hanya digunakan untuk posisi duduk.
2. Input sistem berasal dari webcam laptop atau kamera komputer.
3. Model yang digunakan adalah YOLOv8n-pose.
4. Keypoint tubuh menggunakan standar COCO 17 Keypoints.
5. Analisis hanya berfokus pada perubahan sudut postur tubuh.
6. Sistem tidak memberikan diagnosis medis.
7. Sistem tidak melakukan real-time alerting.

---

# BAB II — KAJIAN TEORI

## 2.1 Computer Vision

Computer Vision merupakan cabang ilmu kecerdasan buatan yang memungkinkan komputer untuk memperoleh, memahami, dan menganalisis informasi visual dari gambar atau video. Dalam penelitian ini, computer vision digunakan untuk mendeteksi keypoint tubuh manusia menggunakan webcam.

---

## 2.2 Deep Learning

Deep Learning merupakan bagian dari machine learning yang menggunakan artificial neural network dengan banyak lapisan untuk mempelajari pola dari data. Deep learning banyak digunakan pada bidang computer vision karena mampu menghasilkan performa tinggi dalam tugas deteksi objek, segmentasi, dan pose estimation.

---

## 2.3 Human Pose Estimation

Human Pose Estimation merupakan teknik computer vision yang digunakan untuk mendeteksi posisi tubuh manusia berdasarkan titik-titik tubuh tertentu (keypoints). Keypoint tersebut meliputi kepala, bahu, siku, pinggul, lutut, dan bagian tubuh lainnya.

Pada penelitian ini, pose estimation digunakan untuk mendeteksi posisi tubuh pengguna saat duduk menggunakan standar COCO 17 Keypoints.

---

## 2.4 YOLOv8-Pose

YOLOv8-Pose merupakan pengembangan model YOLO (You Only Look Once) yang mendukung pose estimation berbasis keypoint detection. Model ini mampu mendeteksi posisi tubuh manusia secara real-time dengan performa yang ringan dan efisien.

Penelitian ini menggunakan YOLOv8n-pose karena memiliki ukuran model yang ringan dan cocok digunakan pada GPU kelas menengah seperti NVIDIA RTX 3050.

---

## 2.5 COCO 17 Keypoints

COCO Keypoints merupakan standar anotasi pose manusia yang terdiri dari 17 titik tubuh, yaitu:

1. Nose
2. Left Eye
3. Right Eye
4. Left Ear
5. Right Ear
6. Left Shoulder
7. Right Shoulder
8. Left Elbow
9. Right Elbow
10. Left Wrist
11. Right Wrist
12. Left Hip
13. Right Hip
14. Left Knee
15. Right Knee
16. Left Ankle
17. Right Ankle

Pada penelitian ini, keypoint utama yang digunakan untuk analisis postur adalah shoulder, hip, dan ear/nose.

---

## 2.6 Pose Analytics

Pose analytics merupakan proses analisis informasi geometris tubuh berdasarkan keypoint hasil pose estimation. Analisis dilakukan menggunakan perhitungan sudut tubuh seperti neck inclination angle dan torso lean angle.

Dalam penelitian ini, pose analytics digunakan untuk mengetahui perubahan kualitas postur tubuh pengguna selama aktivitas berlangsung.

---

## 2.7 Data Augmentation

Data augmentation merupakan teknik memperbanyak variasi dataset menggunakan transformasi citra seperti rotasi, brightness adjustment, blur, dan noise.

Penelitian ini menggunakan augmentasi:

- Brightness increase
- Brightness decrease
- Contrast enhancement
- Rotation ±5°
- Gaussian blur
- Gaussian noise
- Horizontal flip

---

## 2.8 Musculoskeletal Disorders (MSDs)

Musculoskeletal Disorders (MSDs) merupakan gangguan pada sistem otot dan rangka akibat aktivitas fisik tertentu atau postur tubuh yang buruk dalam jangka panjang. Duduk terlalu lama dengan posisi membungkuk dapat meningkatkan risiko MSDs seperti nyeri punggung bawah dan gangguan tulang belakang.

---

# BAB III — METODOLOGI PENELITIAN

## 3.1 Metode Penelitian

Penelitian ini menggunakan metode experimental research dengan pendekatan computer vision dan deep learning untuk menganalisis perubahan sudut postur tubuh manusia selama aktivitas duduk.

---

## 3.2 Tahapan Penelitian

Tahapan penelitian meliputi:

1. Pengumpulan dataset
2. Anotasi keypoint
3. Preprocessing dan augmentasi data
4. Training model YOLOv8n-pose
5. Ekstraksi keypoint tubuh
6. Perhitungan sudut postur tubuh
7. Analisis longitudinal
8. Visualisasi hasil

---

## 3.3 Pengumpulan Dataset

Dataset yang digunakan merupakan dataset primer yang dikumpulkan menggunakan webcam atau kamera laptop.

Dataset terdiri dari:

- Posisi duduk tegak
- Sedikit membungkuk
- Membungkuk parah
- Variasi sudut kamera
- Variasi pencahayaan
- Variasi posisi tubuh

Jumlah dataset original ditargetkan sebanyak 120–150 gambar.

---

## 3.4 Anotasi Dataset

Anotasi dataset dilakukan menggunakan Roboflow dengan metode auto-annotation berbasis pretrained pose estimation model.

Tahapan anotasi:

1. Upload dataset ke Roboflow
2. Auto-label keypoint tubuh
3. Koreksi manual keypoint
4. Export dataset ke format YOLOv8 Pose

---

## 3.5 Preprocessing Data

Tahap preprocessing dilakukan untuk meningkatkan kualitas dataset sebelum training model.

Tahapan preprocessing:

1. Resize image menjadi 640×640 pixel
2. Normalisasi citra
3. Data augmentation

Augmentasi yang digunakan:

- Brightness increase
- Brightness decrease
- Contrast enhancement
- Rotation ±5°
- Gaussian blur
- Gaussian noise
- Horizontal flip

---

## 3.6 Training Model

Model yang digunakan pada penelitian ini adalah YOLOv8n-pose.

Training dilakukan menggunakan framework Ultralytics YOLOv8 dengan GPU NVIDIA RTX 3050.

Parameter training meliputi:

- Epoch
- Batch size
- Learning rate
- Image size
- Optimizer

---

## 3.7 Ekstraksi Sudut Postur

Setelah model menghasilkan keypoint tubuh, dilakukan perhitungan sudut postur menggunakan pendekatan geometri dan trigonometri.

Sudut yang dianalisis meliputi:

- Neck inclination angle
- Torso lean angle
- Shoulder slope

Perhitungan dilakukan menggunakan koordinat keypoint tubuh hasil pose estimation.

---

## 3.8 Longitudinal Posture Analytics

Sistem akan mengambil frame webcam secara periodik setiap satu menit selama sesi belajar atau bekerja.

Data yang disimpan:

- Timestamp
- Nilai sudut postur
- Perubahan sudut tubuh

Data kemudian divisualisasikan dalam bentuk grafik longitudinal untuk melihat pola perubahan postur tubuh pengguna.

---

## 3.9 Output Sistem

Output sistem berupa:

1. Tabel perubahan sudut postur
2. Grafik longitudinal perubahan postur
3. Insight ergonomi pengguna

Contoh insight:

- Pengguna mulai membungkuk pada menit ke-35
- Terjadi peningkatan torso lean angle setelah 40 menit
- Pengguna mampu mempertahankan postur optimal selama 35 menit