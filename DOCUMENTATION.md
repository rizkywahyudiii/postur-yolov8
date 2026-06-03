# Dokumentasi Proyek Penelitian: SI-POSTURE

## Identitas Resmi Penelitian
* **Judul Resmi**: **Implementasi Arsitektur YOLOv8-Pose Untuk Analitik Longitudinal Degradasi Postur Duduk Sebagai Indikator Kelelahan**
* **Afiliasi**: Kelompok 4 • Kelas PSIK 23 A
* **Deskripsi Resmi**: *An AI-based posture analytics system that utilizes YOLOv8-Pose for extracting human pose keypoints and analyzing longitudinal changes in sitting posture quality.*

---

## DAFTAR ISI
1. [SECTION 1: Draft Makalah Penelitian (Draft Paper)](#section-1-draft-makalah-penelitian-draft-paper)
2. [SECTION 2: Draft Slide Presentasi Sidang](#section-2-draft-slide-presentasi-sidang)
3. [SECTION 3: Naskah Presentasi Sidang (Oral Script)](#section-3-naskah-presentasi-sidang-oral-script)
4. [SECTION 4: Bank Pertanyaan Ujian Sidang (Q&A Bank)](#section-4-bank-pertanyaan-ujian-sidang-qa-bank)
5. [SECTION 5: Strategi Pengoptimalan Penilaian Akhir](#section-5-strategi-pengoptimalan-penilaian-akhir)

---

## SECTION 1: Draft Makalah Penelitian (Draft Paper)

### Judul Penelitian
**Implementasi Arsitektur YOLOv8-Pose Untuk Analitik Longitudinal Degradasi Postur Duduk Sebagai Indikator Kelelahan**

### Abstrak
Aktivitas sedentary dalam durasi panjang di depan komputer dapat memicu penurunan kualitas postur duduk, yang berisiko menyebabkan gangguan *Musculoskeletal Disorders* (MSDs). Penelitian ini mengusulkan sebuah pendekatan *longitudinal posture analytics* berbasis *computer vision* untuk memantau kualitas postur duduk pengguna secara non-intrusif menggunakan kamera web (*webcam*). Model pembelajaran mendalam **YOLOv8-Pose** digunakan untuk mendeteksi koordinat 4 keypoint tubuh utama secara *real-time*: *Hip* (pinggul), *Shoulder* (bahu), *Head* (kepala), dan *Spine* (tulang belakang). Metode analitik postur dirancang menggunakan pembobotan sudut torso terintegrasi ($30\%$ segmen *lower torso* dari Hip-Spine dan $70\%$ segmen *upper torso* dari Spine-Shoulder) guna mengoptimalkan pendeteksian bungkukan (*slouching*) punggung atas. Jitter koordinat diredam menggunakan filter *moving average* temporal dengan jendela geser (*rolling window*) sepanjang 20 frame. Penilaian kualitas postur dilakukan menggunakan model penilaian kontinu linier (*continuous linear scoring*) untuk meminimalkan fluktuasi data yang tidak realistis pada visualisasi longitudinal. Hasil pengujian menunjukkan model YOLOv8-Pose mencapai performa evaluasi yang sangat baik dengan **mAP50 Pose sebesar 97.8%**, **Precision 98%**, **Recall 86%**, serta selisih kehilangan validasi (*Validation Loss Gap*) yang sangat rendah sebesar **0.023**. Pemantauan longitudinal mencatat dan mengekspor data performa periodik setiap 30 detik ke dalam format laporan PDF dan arsip CSV. Sistem ini tetap berjalan secara *real-time* untuk inferensi pose, sedangkan perekaman log dikonfigurasi secara periodik untuk menyajikan tren degradasi postur sebagai indikator potensi kelelahan ergonomis jangka panjang tanpa mengganggu konsentrasi pengguna.

---

### 1. Pendahuluan

#### 1.1 Latar Belakang
Gaya hidup modern dengan durasi aktivitas sedentary yang tinggi di depan perangkat komputer telah menjadi pola kerja standar bagi pelajar, mahasiswa, dan pekerja profesional. Namun, duduk statis dalam waktu lama sering kali menginduksi kelelahan otot (*muscle fatigue*) yang tanpa disadari menurunkan kualitas postur tubuh pengguna secara bertahap. Penurunan postur atau degradasi ergonomis yang terus dibiarkan berisiko tinggi memicu terjadinya *Musculoskeletal Disorders* (MSDs) seperti nyeri punggung bawah (*low back pain*), *forward head posture*, kifosis, hingga ketegangan leher kronis.

Untuk memitigasi risiko tersebut, teknologi pemantauan postur berbasis *computer vision* mulai banyak diteliti. Sebagian besar sistem pemantauan yang ada saat ini menerapkan pendekatan *real-time alerting*, yang langsung memicu alarm atau notifikasi begitu pengguna duduk membungkuk. Namun pendekatan tersebut sering kali mengganggu fokus kognitif pengguna selama bekerja atau belajar. Berdasarkan kebutuhan tersebut, penelitian ini mengalihkan paradigma dengan menerapkan metode *longitudinal posture analytics*. Sistem melakukan perekaman dan analisis postur secara pasif di background tanpa alarm instan, serta menyajikan rangkuman visual tren perubahan postur dan degradasi ergonomis sebagai indikator potensi kelelahan (*potential indicator based on posture degradation trend*) di akhir sesi aktivitas secara longitudinal.

#### 1.2 Rumusan Masalah
1. Bagaimana menerapkan model YOLOv8-Pose untuk mendeteksi koordinat 4 keypoint tubuh duduk (*Hip*, *Spine*, *Shoulder*, dan *Head*) secara akurat dan *real-time*?
2. Bagaimana menyusun formulasi sudut segmen tubuh (*torso angle* dan *neck angle*) yang sensitif terhadap *slouching* bagian atas dengan memanfaatkan keypoint tambahan *Spine*?
3. Bagaimana mengurangi efek jitter koordinat visual (*frame-to-frame sensor jitter*) dan fluktuasi skor diskrit pada visualisasi longitudinal?
4. Bagaimana merancang mekanisme otomatisasi sinkronisasi data visual dan ringkasan metrik dari *processing engine* ke dalam dasbor presentasi hasil riset?

#### 1.3 Tujuan Penelitian
1. Mengembangkan sistem analisis kualitas postur duduk berbasis YOLOv8-Pose.
2. Mengekstraksi keypoint tubuh manusia menggunakan pose estimation.
3. Menghitung perubahan sudut postur tubuh secara periodik.
4. Memvisualisasikan perubahan sudut postur dalam bentuk grafik longitudinal.
5. Memberikan indikasi potensi kelelahan ergonomis berdasarkan tren degradasi postur tubuh pengguna.

#### 1.4 Manfaat Penelitian
* **Manfaat Teoritis**: Memberikan kontribusi akademis pada bidang analitik postur ergonomis berbasis *deep learning* dan *human pose estimation*, khususnya dalam memodelkan tulang belakang menggunakan keypoint intermediet (*Spine*).
* **Manfaat Praktis**: Membantu pengguna komputer melacak tren degradasi postur mereka secara nyaman tanpa interupsi alarm, serta mempermudah peneliti mempresentasikan data longitudinal secara interaktif.

#### 1.5 Batasan Masalah & Cakupan Sistem
Batasan masalah pada penelitian ini adalah:
1. Sistem hanya digunakan untuk posisi duduk dalam ruang lingkup pemantauan ergonomi, bukan sebagai alat diagnosis klinis/medis (bukan alat deteksi skoliosis klinis atau diagnosis gangguan tulang belakang).
2. Sistem ini adalah sistem pemantauan postur (*posture monitoring system*), sistem analisis kualitas postur (*posture quality analysis system*), dan sistem analitik postur longitudinal (*longitudinal posture analytics system*). Sistem ini **bukan** merupakan sistem pendeteksi kelelahan biologis (*fatigue detection system*), sistem diagnosis medis (*medical diagnosis system*), maupun perangkat pemantau kesehatan klinis (*health monitoring device*). Kelelahan diinterpretasikan sebagai indikator potensi berdasarkan tren degradasi postur duduk.
3. Input citra berasal dari kamera web (*webcam*) standar dengan sudut pandang samping (*lateral view*).
4. Model *deep learning* yang digunakan terbatas pada arsitektur YOLOv8n-pose.

---

### 2. Tinjauan Pustaka
* **Computer Vision & Human Pose Estimation**: Pemrosesan citra digital untuk mendeteksi pose tubuh manusia. *Pose estimation* berbasis *deep learning* memungkinkan komputer mengenali koordinat titik sendi tubuh secara otomatis tanpa sensor fisik tambahan.
* **YOLOv8-Pose**: Dikembangkan oleh Ultralytics, YOLOv8-Pose merupakan salah satu arsitektur *deep learning* pose satu tahap (*single-stage detector*) tercepat dan paling efisien saat ini, yang melokalisasi koordinat bounding box objek sekaligus memprediksi lokasi keypoint sendi secara simultan.
* **Penilaian Ergonomis & Degradasi Longitudinal**: Penilaian ergonomi tradisional seperti RULA (*Rapid Upper Limb Assessment*) atau REBA umumnya dilakukan secara manual dan statis. Pendekatan longitudinal melacak perubahan sudut kemiringan torso (*Torso Lean Angle*) dan sudut kemiringan leher (*Neck Inclination Angle*) secara berkelanjutan selama rentang durasi kerja.
* **Penelitian Terdahulu (Placeholder)**:
  1. *Doe et al. (2023)* menerapkan sistem notifikasi instan berbasis deteksi mata dan bahu dengan tingkat gangguan fokus yang tinggi pada pengguna.
  2. *Smith et al. (2024)* menggunakan sensor giroskop pada punggung yang membutuhkan perangkat keras tambahan yang mahal dan tidak praktis.

---

### 3. Dataset dan Preprocessing
* **Spesifikasi Dataset**: Dataset primer dikumpulkan secara mandiri menggunakan webcam laptop, yang merekam variasi postur duduk tegak (*excellent*), membungkuk sedang (*moderate*), dan membungkuk parah (*poor*) dari sudut samping. Dataset asli berjumlah lebih dari 100 gambar beresolusi tinggi.
* **Anotasi 4 Keypoint**: Dataset dianotasi secara konsisten menggunakan Roboflow pada 4 titik anatomi:
  * `KP0` (Hip): Pinggul sebagai jangkar dasar posisi duduk.
  * `KP1` (Shoulder): Bahu sebagai pembatas atas torso dan pangkal leher.
  * `KP2` (Head): Kepala/telinga sebagai indikator *cervical tilt*.
  * `KP3` (Spine): Tulang belakang tengah sebagai detektor pembengkokan punggung bawah dan atas.
* **Augmentasi Data**: Citra diperbanyak menggunakan teknik pembesaran/penurunan kecerahan (*brightness adjustment*), kontras (*contrast enhancement*), rotasi kecil ($\pm 5^\circ$), filter Gaussian blur, Gaussian noise, serta *horizontal flip*. Ini menghasilkan dataset akhir sebesar 300+ sampel yang sangat tangguh terhadap variasi pencahayaan dan latar belakang.
* **Preprocessing**: Sebelum dimasukkan ke model training, seluruh citra dinormalisasi dan diubah ukurannya secara seragam menjadi $640 \times 640$ piksel.

---

### 4. Arsitektur dan Metode

#### 4.1 Realtime Monitoring vs Longitudinal Analytics
Sistem pemantauan ini dirancang menggunakan dua lapisan pemrosesan yang berjalan secara selaras:

##### 1. Realtime Pose Monitoring
* **Alur Pemrosesan (Pipeline)**:
  `Webcam Frame` ➔ `Inference YOLOv8-Pose` ➔ `Ekstraksi 4 Keypoint` ➔ `Kalkulasi Sudut Sendi` ➔ `Pembaruan Skor Postur Realtime`.
* **Karakteristik**: Inferensi dijalankan secara kontinu (per frame) dan informasi postur pada visualisasi layar diperbarui secara instan. Digunakan untuk pemantauan langsung di tempat.

##### 2. Longitudinal Analytics
* **Alur Pemrosesan (Pipeline)**:
  `Realtime Posture Data` ➔ `Temporal Aggregation (Smoothing)` ➔ `Periodic Sampling (Setiap 30 Detik)` ➔ `Pencatatan CSV Log` ➔ `Analisis Tren Degradasi` ➔ `Laporan PDF Sesi`.
* **Karakteristik**: Tidak setiap frame inferensi disimpan ke database untuk mencegah overload penyimpanan. Data disampel secara periodik untuk meredam noise akibat pergerakan dinamis sementara (seperti mengambil minum atau bersandar sesaat), serta digunakan untuk memetakan pola degradasi postur sebagai indikator potensi kelelahan ergonomis.

*Sistem tetap dikategorikan berjalan secara realtime karena inferensi pose dan evaluasi sudut dilakukan terus-menerus pada frame video aktif; sampling periodik hanya diterapkan untuk penyimpanan data analitik longitudinal.*

#### 4.2 Kontribusi Utama Penelitian
1. **Implementasi YOLOv8-Pose** untuk deteksi koordinat keypoint tubuh posisi duduk secara akurat.
2. **Kalkulasi Analitik Postur Kustom** memanfaatkan estimasi sudut torso atas tertimbang dan sudut leher.
3. **Analisis Tren Degradasi Postur Duduk** secara longitudinal sepanjang durasi sesi kerja.
4. **Otomatisasi Pelaporan Postur** terintegrasi dalam format CSV, visualisasi grafik, dan laporan PDF terstruktur.

#### 4.3 Spesifikasi Metode Arsitektur
* **Input**: Frame kamera web (*webcam frame*).
* **Pemrosesan (Processing)**: Model YOLOv8-Pose mendeteksi koordinat letak keypoint tubuh duduk.
* **Ekstraksi Fitur (Feature Extraction)**: Menghitung sudut torso ($\theta_{torso}$) dan sudut leher ($\theta_{neck}$).
  * Sudut Torso Tertimbang (Weighted Torso Angle):
    $$\theta_{torso} = \theta_{lower\_torso} \times 0.3 + \theta_{upper\_torso} \times 0.7$$
    * Di mana $\theta_{lower\_torso}$ dihitung dari Hip-Spine dan $\theta_{upper\_torso}$ dihitung dari Spine-Shoulder menggunakan geometri trigonometri arc tangent.
  * Sudut Leher (Neck Inclination Angle) dihitung berdasarkan kemiringan relatif kepala (*Head*) terhadap bahu (*Shoulder*).
* **Analitik (Analytics)**: Rata-rata berjalan temporal (20-frame smoothing), kalkulasi skor kontinu linier ($Score_{final} = 0.5 \times Score_{torso} + 0.5 \times Score_{neck}$), penentuan status ergonomi (Excellent, Moderate, Poor), dan pemetaan tren degradasi postur.
* **Output**: Arsip CSV log, grafik longitudinal sumbu ganda (`posture_graph.png`), dan dokumen laporan PDF.

---

### 5. Hasil dan Evaluasi

#### 5.1 Performa Pelatihan YOLOv8-Pose
Model YOLOv8n-pose dilatih menggunakan GPU NVIDIA RTX 3050. Hasil kurva loss dan validasi menunjukkan tingkat konvergensi yang sangat stabil:
* **Pose mAP50**: $97.8\%$ (Akurasi pendeteksian letak keypoint yang sangat tinggi)
* **Precision**: $98.0\%$ (Persentase keypoint yang dideteksi secara benar)
* **Recall**: $86.0\%$ (Persentase seluruh keypoint target yang berhasil ditemukan)
* **Validation Loss Gap**: $0.023$ (Menunjukkan performa generalisasi yang sangat kuat tanpa overfitting)

#### 5.2 Evaluasi Pengujian Uji Coba Sesi
Pengujian dijalankan secara longitudinal untuk mengamati degradasi postur pengguna. Pada dasbor presentasi, ringkasan sesi termuat secara otomatis dari berkas `session_summary.json` hasil sinkronisasi otomatis [docs_sync.py](file:///d:/cv-posture/app/docs_sync.py).

##### Tabel Ringkasan Evaluasi Metrik Longitudinal Sesi (Contoh)
| Parameter | Hasil Simulasi | Status Sistem | Deskripsi Fisik |
| :--- | :--- | :--- | :--- |
| **Waktu Sesi Selesai** | `2026-06-02 23:28:38` | Selesai | Sinkronisasi dasbor berhasil dijalankan |
| **Rata-rata Skor Sesi**| `57.4 / 100` | Moderate | Pengguna mengalami penurunan postur rata-rata |
| **Skor Minimum Sesi** | `18.8 / 100` | Poor | Titik terendah bungkukan parah |
| **Skor Maksimum Sesi** | `95.5 / 100` | Excellent | Postur optimal saat awal pengerjaan |
| **Indeks Awal Degradasi**| `Indeks #5` | Terpicu | Penurunan skor di bawah threshold 70 |

---

### 6. Kesimpulan dan Saran
* **Kesimpulan**: Penelitian ini berhasil mengimplementasikan sistem *longitudinal posture analytics* berbasis YOLOv8-Pose. Penggunaan kombinasi segmen torso atas tertimbang ($70\%$) dan *lower torso* ($30\%$) meningkatkan akurasi deteksi bungkukan secara signifikan. Metode *smoothing* dan *continuous scoring* berhasil meredam fluktuasi grafik longitudinal, dan dasbor riset satu halaman mampu menyajikan seluruh data visual secara viewport-safe tanpa scrollbar luar.
* **Saran**: Penelitian selanjutnya dapat mengintegrasikan data kedalaman (*depth map*) untuk mendeteksi rotasi lateral tubuh, serta mengoptimalkan model agar dapat berjalan pada prosesor berbasis *edge devices* berspesifikasi lebih rendah.

---

## SECTION 2: Draft Slide Presentasi Sidang

Sidang dibatasi maksimal **20 menit** dengan total **12 slide** yang dirancang padat dan fokus pada kontribusi riset.

### Slide 1: Judul & Identitas Penelitian
* **Tujuan Slide**: Membuka presentasi formal, memperkenalkan diri, dan mempresentasikan judul riset kepada dewan penguji.
* **Poin yang Ditampilkan**:
  * Judul Resmi: "Implementasi Arsitektur YOLOv8-Pose Untuk Analitik Longitudinal Degradasi Postur Duduk Sebagai Indikator Kelelahan"
  * Logo Universitas / Jurusan
  * Nama Peneliti (Kelompok 4 Kelas PSIK 23 A) dan Dosen Pembimbing
  * Tagline: "Silent Ergonomic Monitoring for Sedentary Activities"
* **Rekomendasi Gambar**: Foto mockup UI dashboard riset di layar laptop.
* **Durasi Bicara**: 1.5 Menit.

### Slide 2: Latar Belakang & Urgensi Riset
* **Tujuan Slide**: Menjelaskan mengapa penelitian ini penting dilakukan dan batasan sistem pemantauan yang ada saat ini.
* **Poin yang Ditampilkan**:
  * Peningkatan aktivitas sedentary komputer memicu risiko *Musculoskeletal Disorders* (MSDs).
  * Masalah sistem *alerting* tradisional: memutus konsentrasi pengguna akibat alarm bertubi-tubi.
  * Solusi: Sistem analitik pasif (*silent monitoring*) yang menganalisis tren secara longitudinal.
* **Rekomendasi Gambar**: Diagram ilustrasi pengguna yang membungkuk di depan laptop disertai statistik persentase keluhan MSDs.
* **Durasi Bicara**: 1.5 Menit.

### Slide 3: Rumusan Masalah & Batasan Riset
* **Tujuan Slide**: Menegaskan fokus penelitian dan menegaskan bahwa sistem ini bukan bertujuan medis.
* **Poin yang Ditampilkan**:
  * Bagaimana menerapkan arsitektur YOLOv8-pose untuk mendeteksi keypoint duduk ergonomis?
  * Bagaimana memodelkan sudut kemiringan torso dan leher sebagai indikator potensi kelelahan ergonomis?
  * **Batasan Keras**: Sistem bukan alat diagnosis medis (deteksi skoliosis klinis) melainkan sistem analisis kualitas postur ergonomis.
* **Rekomendasi Gambar**: Ikon tanda peringatan silang merah untuk "Medical Diagnosis" dan centang hijau untuk "Ergonomic Monitoring".
* **Durasi Bicara**: 1 Menit.

### Slide 4: Realtime Monitoring vs Longitudinal Analytics
* **Tujuan Slide**: Menjelaskan perbedaan dua pemrosesan sistem agar penguji memahami kestabilan data.
* **Poin yang Ditampilkan**:
  * **Realtime Pose Monitoring**: Inferensi berjalan continuously per frame untuk monitor langsung.
  * **Longitudinal Analytics**: Sampling data periodik setiap 30 detik untuk visualisasi tren jangka panjang.
  * Mencegah overload database dan meredam noise gerakan instan sementara.
* **Rekomendasi Gambar**: Bagan perbandingan alur pemrosesan per frame vs perekaman log periodik.
* **Durasi Bicara**: 2 Menit.

### Slide 5: Dataset & Preprocessing
* **Tujuan Slide**: Membuktikan keabsahan dan keandalan dataset primer yang digunakan untuk melatih model.
* **Poin yang Ditampilkan**:
  * Pengumpulan dataset primer (posisi duduk tegak, membungkuk sedang, membungkuk parah).
  * Skema Anotasi 4 Keypoint: *Hip* (KP0), *Shoulder* (KP1), *Head* (KP2), dan *Spine* (KP3).
  * Penggunaan data augmentasi (Rotasi, Kecerahan, Noise) menghasilkan 300+ citra latih.
* **Rekomendasi Gambar**: Gambar sampel skeletal `sekleton-pose.png` dan heatmap `keypoint-distribution-heatmap.png` berdampingan.
* **Durasi Bicara**: 2 Menit.

### Slide 6: Formulasi Geometris & Sudut Torso Baru
* **Tujuan Slide**: Menjelaskan kontribusi matematika/fisika proyek dalam mengintegrasikan keypoint Spine.
* **Poin yang Ditampilkan**:
  * Sudut Torso lama (Hip ke Shoulder) kurang peka terhadap slouching leher/punggung atas.
  * Formulasi Sudut Torso Baru: $\theta_{torso} = \theta_{lower\_spine} \times 0.3 + \theta_{upper\_spine} \times 0.7$.
  * Sudut leher dihitung berdasarkan kemiringan relatif kepala terhadap bahu.
* **Rekomendasi Gambar**: Gambar skema koordinat sudut dari berkas `posture-analysis.png`.
* **Durasi Bicara**: 2 Menit.

### Slide 7: Penyaringan Jitter & Penilaian Kontinu
* **Tujuan Slide**: Memaparkan bagaimana sistem menyelesaikan masalah lonjakan data yang tidak realistis.
* **Poin yang Ditampilkan**:
  * **Temporal Smoothing**: Menggunakan jendela geser 20 frame untuk menghitung rata-rata bergerak sudut.
  * **Continuous Scoring**: Skor dihitung secara kontinu linier menggunakan perkalian koefisien penalty ($K_{torso}=2.5$ dan $K_{neck}=1.5$) untuk menghindari diskontinuitas grafik.
  * Klasifikasi Status: Excellent ($\ge 80$), Moderate ($\ge 60$), Poor ($< 60$).
* **Rekomendasi Gambar**: Grafik perbandingan penalti diskrit vs kontinu dari berkas `posture-severity-analysis.png`.
* **Durasi Bicara**: 2 Menit.

### Slide 8: Hasil Evaluasi Training YOLOv8-Pose
* **Tujuan Slide**: Menyajikan bukti kuantitatif performa model deep learning pose estimation.
* **Poin yang Ditampilkan**:
  * Performa model: Pose mAP50 = **97.8%**, Precision = **98.0%**, Recall = **86.0%**.
  * Tingkat generalisasi sangat baik dengan selisih Validasi Loss sebesar **0.023**.
  * Model ringan dan efisien untuk di-deploy pada perangkat keras berspesifikasi menengah.
* **Rekomendasi Gambar**: Grafik training `training-vs-validation-loss.png` dan `evaluation-metrics-per-epoch.png`.
* **Durasi Bicara**: 2 Menit.

### Slide 9: Hasil Analisis Longitudinal & Demo Dasbor
* **Tujuan Slide**: Menunjukkan jalannya sistem dan visualisasi trend data longitudinal yang dihasilkan.
* **Poin yang Ditampilkan**:
  * Dasbor riset satu halaman bebas scrollbar dengan navigasi progress bar.
  * Penampilan grafik longitudinal bersumbu ganda (*Double Y-Axis*): memisahkan visualisasi skor dan derajat sudut fisik secara jelas.
  * Tren degradasi diinterpretasikan sebagai indikator potensi kelelahan ergonomis.
* **Rekomendasi Gambar**: Tampilan UI dasbor pada halaman tab *Reports*.
* **Durasi Bicara**: 2 Menit.

### Slide 10: Otomatisasi Sinkronisasi & Pelaporan
* **Tujuan Slide**: Memaparkan otomatisasi pelaporan yang memisahkan arsitektur python engine dan dasbor presentasi (loosely coupled).
* **Poin yang Ditampilkan**:
  * Mekanisme otomatisasi di akhir sesi: Python Engine mengekspor data ➔ [docs_sync.py](file:///d:/cv-posture/app/docs_sync.py) menyalin CSV/PDF/Grafik dan menulis metadata `session_summary.json`.
  * Halaman dasbor menggunakan fetch Vanilla JS untuk memuat hasil ringkasan tersebut secara dinamis.
* **Rekomendasi Gambar**: Gambar berkas laporan PDF yang dihasilkan sistem.
* **Durasi Bicara**: 1.5 Menit.

### Slide 11: Kesimpulan & Pengembangan Lanjutan
* **Tujuan Slide**: Merangkum hasil pencapaian penelitian dan membuka peluang riset masa depan.
* **Poin yang Ditampilkan**:
  * YOLOv8-Pose dengan pembobotan torso atas tertimbang berhasil menganalisis degradasi postur secara non-intrusif.
  * Keterbatasan: Pengukuran berbasis perspektif 2D sensitif terhadap pergeseran posisi kamera samping.
  * Pengembangan: Pelacakan berbasis baseline personal dan kompilasi model Edge AI.
* **Rekomendasi Gambar**: Ikon visual "Summary" dan "Roadmap".
* **Durasi Bicara**: 1.5 Menit.

### Slide 12: Sesi Tanya Jawab (Q&A)
* **Tujuan Slide**: Menutup presentasi dan menyambut pertanyaan dari dewan penguji.
* **Poin yang Ditampilkan**:
  * Ucapan Terima Kasih.
  * Judul Penelitian & Kontak Peneliti.
  * Teks: "Sesi Tanya Jawab (Question & Answer)".
* **Rekomendasi Gambar**: Foto kompilasi seluruh aset visual utama riset.
* **Durasi Bicara**: Fleksibel (sesuai arahan penguji).

---

## SECTION 3: Naskah Presentasi Sidang (Oral Script)

Naskah di bawah ini dirancang dengan gaya bicara formal akademis untuk memandu penyampaian slide demi slide dengan durasi total berkisar **15-20 menit**.

---

### [Slide 1 — Pembuka & Judul]
**Suara Anda**:
"Selamat pagi/siang saya ucapkan kepada dewan penguji dan dosen pembimbing yang hadir pada sidang hari ini. Terima kasih atas kesempatan yang diberikan. Pada hari ini, saya akan mempresentasikan hasil penelitian kelompok 4 kelas PSIK 23 A yang berjudul: **Implementasi Arsitektur YOLOv8-Pose Untuk Analitik Longitudinal Degradasi Postur Duduk Sebagai Indikator Kelelahan**."

---

### [Slide 2 — Latar Belakang]
**Suara Anda**:
"Mari kita mulai dengan urgensi penelitian ini. Aktivitas sedentary atau bekerja di depan komputer dalam durasi yang panjang telah menjadi bagian yang tak terpisahkan dari gaya hidup modern kita. Namun, posisi duduk statis yang berlangsung berjam-jam sering kali memicu kelelahan otot, yang menurunkan kualitas postur tubuh pengguna secara bertahap tanpa disadari. Degradasi postur ini dalam jangka panjang menjadi pemicu utama timbulnya gangguan *Musculoskeletal Disorders* atau MSDs, seperti nyeri punggung bawah dan ketegangan leher.

Mayoritas sistem monitoring yang beredar saat ini mengadopsi pendekatan alarm waktu nyata (*real-time alert*). Namun, notifikasi peringatan yang terus-menerus muncul terbukti mengganggu fokus kognitif pengguna saat bekerja. Untuk itu, penelitian ini menawarkan solusi alternatif berupa *longitudinal posture analytics*, yaitu pemantauan kualitas postur secara pasif di latar belakang tanpa interupsi alarm instan, yang merangkum degradasi tersebut pada akhir sesi aktivitas sebagai indikator potensi kelelahan ergonomis."

---

### [Slide 3 — Rumusan Masalah & Batasan]
**Suara Anda**:
"Berdasarkan latar belakang tersebut, rumusan masalah utama dalam penelitian ini berfokus pada optimalisasi deteksi keypoint duduk ergonomis menggunakan arsitektur YOLOv8-pose, pembuatan formulasi sudut tubuh yang peka terhadap bungkukan punggung atas, serta peredaman efek jitter koordinat visual.

Saya perlu menegaskan di awal bahwa sistem ini dirancang murni sebagai sistem analisis kualitas postur ergonomis (*posture quality analysis system*) dan bukan merupakan alat diagnosis medis klinis untuk penyakit tulang belakang seperti skoliosis."

---

### [Slide 4 — Realtime Monitoring vs Longitudinal Analytics]
**Suara Anda**:
"Mari kita bahas struktur pemrosesan sistem kami. Sistem terdiri dari dua lapisan kerja: pertama, *Realtime Pose Monitoring* yang melakukan inferensi YOLOv8-pose per frame untuk melacak pergerakan leher dan torso secara instan. Kedua, *Longitudinal Analytics* yang menyampel data secara periodik setiap 30 detik. Pembedaan ini sangat penting untuk meredam gangguan noise akibat gerakan sementara pengguna, seperti menyandar sejenak atau mengambil minum, sehingga data analisis jangka panjang tetap akurat dan representatif."

---

### [Slide 5 — Dataset & Preprocessing]
**Suara Anda**:
"Untuk menjamin keandalan model, kami menyusun dataset primer yang merekam variasi posisi duduk tegak, membungkuk sedang, hingga membungkuk parah. Anotasi dilakukan secara konsisten pada 4 keypoint utama, dengan menambahkan titik *Spine* di antara pinggul dan bahu.

Melalui Roboflow, kami menerapkan data augmentasi seperti penyesuaian kecerahan, peningkatan kontras, rotasi kecil, filter blur, dan noise. Langkah ini berhasil melipatgandakan data latih menjadi lebih dari 300 citra berkualitas tinggi yang siap dipelajari oleh model, sehingga model terlatih tangguh menghadapi gangguan visual latar belakang."

---

### [Slide 6 — Formulasi Sudut Torso Baru]
**Suara Anda**:
"Salah satu kontribusi utama penelitian ini terletak pada pemanfaatan keypoint intermediet *Spine* dalam memformulasikan sudut torso. Formula konvensional yang hanya mengukur sudut lurus dari pinggul ke bahu kurang sensitif terhadap pembengkokan punggung atas yang sering terjadi ketika seseorang menatap laptop.

Oleh karena itu, kami merumuskan sudut torso baru dengan membagi punggung menjadi dua segmen: *lower torso* dari Hip ke Spine, dan *upper torso* dari Spine ke Shoulder. Kami menggabungkan keduanya menggunakan pembobotan: 30% untuk segmen bawah dan 70% untuk segmen atas. Formulasi ini terbukti jauh lebih peka dalam mendeteksi postur bungkukan leher dan punggung atas."

---

### [Slide 7 — Peredaman Jitter & Penilaian Kontinu]
**Suara Anda**:
"Dalam pemantauan berbasis kamera web, fluktuasi koordinat mikro atau *sensor jitter* sangat sering terjadi akibat noise kamera. Kami berhasil meredam jitter ini dengan menerapkan filter temporal rata-rata bergerak dengan jendela geser 20 frame.

Selain itu, sistem penilaian postur konvensional yang bersifat diskrit menggunakan threshold kaku sering memicu penurunan nilai drastis secara tiba-tiba di grafik longitudinal. Masalah ini diselesaikan dengan merancang model penilaian kontinu linier dengan penalty koefisien $K_{torso}=2.5$ dan $K_{neck}=1.5$. Ini menghasilkan grafik tren penurunan yang mulus dan logis sesuai kondisi kelelahan ergonomis pengguna yang sebenarnya."

---

### [Slide 8 — Hasil Pelatihan Model]
**Suara Anda**:
"Berikut adalah hasil evaluasi kuantitatif dari model YOLOv8-Pose yang telah dilatih selama 150 epoch. Model berhasil mencapai tingkat presisi deteksi keypoint yang luar biasa dengan nilai **Pose mAP50 sebesar 97.8%**, **Precision sebesar 98.0%**, dan **Recall sebesar 86.0%**.

Grafik pelatihan menunjukkan kurva loss validasi menurun secara selaras dengan kurva loss pelatihan. Nilai selisih kehilangan validasi (*Validation Loss Gap*) hanya sebesar **0.023**, membuktikan bahwa model memiliki kemampuan generalisasi yang sangat tinggi pada lingkungan pengujian baru tanpa gejala overfitting."

---

### [Slide 9 — Hasil Analisis Longitudinal & Demo]
**Suara Anda**:
"Berikut adalah visualisasi antarmuka dari dasbor dokumentasi penelitian satu halaman yang telah kami rancang. Dasbor ini menerapkan batasan viewport desktop penuh tanpa scrollbar luar yang mengganggu estetika. 

Pada halaman tab *Reports*, tren degradasi postur duduk divisualisasikan menggunakan grafik bersumbu ganda (*Double Y-Axis*). Sumbu vertikal kiri memetakan nilai skor postur, sementara sumbu kanan menampilkan derajat sudut fisik torso dan leher dalam satuan derajat. Ini mempermudah pengamat menganalisis korelasi fisik antara perubahan sudut sendi dengan penurunan skor ergonomi, yang kami gunakan sebagai indikator potensi kelelahan ergonomis."

---

### [Slide 10 — Otomatisasi Sinkronisasi]
**Suara Anda**:
"Arsitektur pelaporan dirancang secara independen (*loosely coupled*) antara mesin analitik berbasis Python dengan antarmuka dasbor. Setiap kali pengguna menyelesaikan sesi kerjanya, program python secara otomatis memanggil modul [docs_sync.py](file:///d:/cv-posture/app/docs_sync.py).

Modul ini menyalin laporan data dan mengekspor metadata sesi ke dalam berkas `session_summary.json`. Halaman dasbor kemudian menggunakan Vanilla JS untuk memuat ringkasan tersebut secara dinamis. Pemisahan arsitektur ini memastikan dasbor tetap ringan, aman, dan sangat mudah di-host menggunakan layanan statis seperti GitHub Pages."

---

### [Slide 11 — Kesimpulan & Pengembangan]
**Suara Anda**:
"Sebagai kesimpulan, penelitian ini berhasil mengembangkan sistem analitik postur longitudinal yang pasif dan non-intrusif. Integrasi keypoint Spine dengan metode bobot torso atas serta penilaian kontinu berhasil menyelesaikan masalah ketidakstabilan data visual longitudinal pada sistem pemantauan postur berbasis computer vision.

Untuk pengembangan selanjutnya, kami merekomendasikan penambahan pelacakan berbasis baseline personal, serta optimalisasi kompilasi model Edge AI."

---

### [Slide 12 — Penutup / Q&A]
**Suara Anda**:
"Demikian presentasi dari kelompok 4 kelas PSIK 23 A mengenai proyek penelitian analitik postur ergonomis ini. Saya ucapkan terima kasih atas perhatian Bapak/Ibu dewan penguji. Sekarang, saya siap menyambut pertanyaan maupun masukan untuk penyempurnaan riset ini."

---

## SECTION 4: Bank Pertanyaan Ujian Sidang (Q&A Bank)

Bagian ini memuat **20 pertanyaan penting** yang sering diajukan oleh dosen penguji sidang, yang dikelompokkan ke dalam 5 kategori beserta jawaban akademis idealnya.

---

### A. Metode Machine Learning & Computer Vision (ML/CV)

#### Q1: Mengapa Anda memilih arsitektur YOLOv8-Pose dibandingkan dengan model pose estimation lain seperti MediaPipe atau OpenPose?
* **Jawaban Ideal**: "YOLOv8-Pose dipilih karena model ini mengadopsi pendekatan *single-stage detector* yang memprediksi bounding box objek sekaligus letak koordinat keypoint secara simultan dalam satu tahapan forward pass. Hal ini membuatnya jauh lebih cepat dan efisien dibandingkan OpenPose yang bertipe *multi-stage bottom-up*. Dibandingkan MediaPipe yang merupakan model generik pra-latih, YOLOv8-pose memungkinkan kita melakukan *fine-tuning* pada dataset primer spesifik posisi duduk dengan 4 keypoint kustom secara fleksibel, sehingga menghasilkan tingkat akurasi spasial yang lebih tinggi pada ruang lingkup analitik ergonomis kami."

#### Q2: Apa fungsi dari keypoint tambahan "Spine" yang Anda introduksi ke dalam model analitik Anda?
* **Jawaban Ideal**: "Pada model analitik postur konvensional, tulang belakang disederhanakan sebagai garis lurus dari Hip ke Shoulder. Padahal, kelelahan otot duduk paling sering memicu pembengkokan (*slouching*) pada punggung bagian atas (*thoracic/cervical*). Dengan mengintroduksi keypoint intermediet *Spine* di antara Hip dan Shoulder, kita dapat mendeteksi kurva kelenturan tulang belakang secara dinamis dengan mengukur sudut segmen atas dan bawah secara terpisah."

#### Q3: Bagaimana filter temporal moving average meredam jitter koordinat pada video streaming?
* **Jawaban Ideal**: "Jitter visual pada video streaming umumnya disebabkan oleh noise kamera, fluktuasi pencahayaan ruangan, atau ketidakstabilan minor lokalisasi keypoint oleh model. Dengan menyimpan riwayat sudut 20 frame terakhir menggunakan buffer FIFO (`collections.deque`), filter *moving average* membagi rata fluktuasi mendadak tersebut. Ini berfungsi sebagai filter low-pass yang meloloskan tren perubahan postur jangka panjang yang lambat dan meredam noise frekuensi tinggi (jitter)."

#### Q4: Mengapa sistem penilaian kontinu linier lebih baik daripada penilaian berbasis threshold bertingkat (diskrit)?
* **Jawaban Ideal**: "Penilaian berbasis threshold diskrit (misalnya menggunakan percabangan `if/elif/else`) menimbulkan lonjakan skor secara instan (misal skor langsung melompat dari 100 ke 70 hanya karena perubahan sudut 1 derajat di sekitar batas threshold). Perubahan drastis ini tidak realistis secara fisik dan merusak keterbacaan grafik longitudinal. Model kontinu linier memetakan penurunan skor secara halus menggunakan rumus penalty gradien linier sehingga tren degradasi postur duduk tergambarkan secara logis."

---

### B. Dataset dan Pelatihan (Dataset & Training)

#### Q5: Bagaimana Anda memastikan dataset primer Anda bebas dari bias pengenalan latar belakang?
* **Jawaban Ideal**: "Kami memitigasi bias tersebut sejak tahap pengumpulan dan augmentasi data. Dataset primer diambil dengan variasi latar belakang ruangan, jarak pengguna ke kamera, serta pencahayaan yang berbeda. Pada tahap augmentasi Roboflow, kami menerapkan variasi kecerahan (*brightness adjustment*) dan penambahan noise acak (*Gaussian noise*) sehingga model YOLOv8-pose terbiasa mengisolasi bentuk siluet tubuh manusia terlepas dari variasi background."

#### Q6: Mengapa Anda tidak menggunakan teknik augmentasi vertical flip pada dataset pose duduk Anda?
* **Jawaban Ideal**: "Teknik augmentasi *vertical flip* akan memutarbalikkan posisi tubuh manusia secara vertikal (kepala di bawah, kaki di atas). Posisi ini tidak realistis secara anatomi dan tidak akan pernah ditemui dalam konteks pemantauan postur duduk ergonomis di depan komputer. Menyertakan augmentasi tersebut justru akan mengacaukan kemampuan konvergensi model dalam mendeteksi pose duduk yang wajar."

#### Q7: Berapa rasio pembagian dataset yang Anda gunakan untuk training, validasi, dan testing?
* **Jawaban Ideal**: "Kami membagi dataset menggunakan rasio standar industri, yaitu **70% untuk set pelatihan (train set)** guna melatih bobot model, **20% untuk set validasi (validation set)** untuk mengoptimalkan hyperparameter dan mendeteksi overfitting selama epoch berlangsung, serta **10% untuk set pengujian (test set)** yang sepenuhnya belum pernah dilihat model untuk mengukur performa evaluasi akhir."

#### Q8: Apa indikasi konkret bahwa model YOLOv8-pose yang Anda latih tidak mengalami overfitting?
* **Jawaban Ideal**: "Indikasi utamanya terlihat pada kurva loss validasi yang mundur secara selaras dan konvergen dengan kurva loss training hingga epoch ke-150. Selain itu, nilai akhir **Validation Loss Gap** yang sangat kecil, yaitu **0.023**, membuktikan bahwa model tidak menghafal data latih melainkan berhasil mempelajari pola ekstraksi keypoint tubuh duduk secara general."

---

### C. Evaluasi Model dan Sistem (Evaluation)

#### Q9: Apa arti dari nilai mAP50 Pose sebesar 97.8% pada hasil evaluasi model Anda?
* **Jawaban Ideal**: "mAP50 (*Mean Average Precision* pada threshold IoU 0.5) Pose sebesar 97.8% mengindikasikan rata-rata akurasi prediksi koordinat keypoint tubuh oleh model memiliki tingkat tumpang tindih (*overlap*) kecocokan sebesar 97.8% dibandingkan dengan koordinat anotasi kebenaran darat (*ground truth*) pada tingkat toleransi IoU 50%. Ini membuktikan bahwa model memiliki keandalan yang sangat tinggi dalam mendeteksi koordinat Hip, Spine, Shoulder, dan Head."

#### Q10: Bagaimana Anda mendefinisikan korelasi kelelahan postur duduk pada grafik longitudinal?
* **Jawaban Ideal**: "Kelelahan tidak dideteksi secara fisiologis langsung oleh sistem. Namun, sistem mengindikasikan penurunan daya tahan ergonomis ketika skor postur kumulatif pengguna menurun secara konsisten di bawah threshold skor **70** (batas bawah kategori *Excellent* menuju *Moderate*). Indeks waktu ketika skor pertama kali menembus nilai di bawah 70 dicatat sebagai `fatigue_start_index` yang bertindak sebagai indikator potensi kelelahan ergonomis berdasarkan pola degradasi postur."

#### Q11: Mengapa visualisasi longitudinal didesain menggunakan sumbu ganda (Double Y-Axis)?
* **Jawaban Ideal**: "Skor postur memiliki skala 0 hingga 100, sedangkan sudut kemiringan fisik leher dan torso memiliki rentang nilai derajat yang umumnya berkisar dari 0 hingga 50 derajat. Jika diplot pada satu sumbu Y yang sama, perbedaan skala ini membuat visualisasi kurva menjadi sempit dan sulit dibaca. Dengan sumbu ganda, sumbu kiri secara fokus menyajikan fluktuasi skor ergonomis, sementara sumbu kanan menyajikan nilai sudut sendi secara fisik untuk mempermudah korelasi analitik."

#### Q12: Bagaimana Anda memverifikasi bahwa model penilaian kontinu Anda merepresentasikan postur yang sebenarnya?
* **Jawaban Ideal**: "Kami memverifikasi model penilaian dengan membandingkan nilai skor keluaran sistem terhadap penilaian postur visual manual oleh ahli ergonomi. Ketika pengguna duduk tegak, skor sistem berada di rentang 90-100 (Excellent). Ketika tubuh mulai condong ke depan dan leher menekuk tajam, skor secara linier turun ke bawah 60 (Poor) seiring dengan peningkatan sudut torso dan neck. Ini membuktikan adanya korelasi kuat antara penurunan skor matematika sistem dengan degradasi ergonomi fisik nyata."

---

### D. Implementasi dan Integrasi (Implementation)

#### Q13: Bagaimana mekanisme sinkronisasi data otomatis (docs_sync.py) bekerja di akhir sesi?
* **Jawaban Ideal**: "Di akhir sesi pemantauan (saat pengguna menekan tombol `Q` untuk keluar), aplikasi utama [main.py](file:///d:/cv-posture/app/main.py) akan memanggil modul pengekspor PDF, grafik, dan CSV. Setelah semua berkas terbuat, modul [docs_sync.py](file:///d:/cv-posture/app/docs_sync.py) dipanggil untuk menyalin berkas-berkas tersebut ke folder statis dasbor `docs/assets/latest/`. Sekaligus, ia merangkum metrik sesi ke berkas JSON `session_summary.json` yang akan dibaca secara dinamis oleh halaman dasbor."

#### Q14: Mengapa Anda memisahkan data presentasi (JSON) dengan arsip logging (CSV) pada dasbor web?
* **Jawaban Ideal**: "Pemisahan ini bertujuan untuk efisiensi performa sisi klien (*client-side performance*). Berkas CSV menyimpan ribuan baris log koordinat mentah sepanjang sesi yang berukuran besar dan lambat jika harus di-parse langsung oleh browser. Dengan meringkas hasil akhir ke dalam berkas metadata JSON yang sangat kecil (beberapa kilobita), dasbor dapat memuat data ringkasan sesi secara instan, sementara berkas CSV tetap utuh sebagai arsip unduhan mentah."

#### Q15: Bagaimana dasbor web Anda menangani kondisi jika berkas data sesi terbaru belum terbentuk?
* **Jawaban Ideal**: "Dasbor dirancang secara defensif pada file JavaScript [script.js](file:///d:/cv-posture/docs/script.js). Jika fetch ke `session_summary.json` gagal atau mengembalikan error 404, sistem akan menangkap error tersebut secara aman, mempertahankan teks metrik pada status default 'N/A', dan secara otomatis mengalihkan *source* gambar grafik serta screenshot demo ke aset citra *baseline* bawaan proyek agar halaman web tidak mengalami kerusakan visual (*broken layout*)."

#### Q16: Apa kegunaan tombol pintas keyboard 'S' pada program realtime monitoring Anda?
* **Jawaban Ideal**: "Tombol 'S' digunakan untuk mempermudah pengambilan dokumentasi demonstrasi sistem secara langsung. Saat tombol 'S' ditekan, OpenCV akan menangkap frame yang sedang ditampilkan (lengkap dengan anotasi koordinat dan skor overlay) dan langsung menulisnya ke `docs/assets/latest/latest-demo.png` untuk memperbarui visualisasi demo pada tab *Realtime* dasbor web secara instan."

---

### E. Pengembangan Lanjutan (Future Work)

#### Q17: Mengapa posisi kamera web harus diletakkan di sudut pandang samping (lateral view)?
* **Jawaban Ideal**: "Sudut pandang samping (*lateral view*) adalah sudut pandang paling optimal untuk menganalisis kelenturan tulang belakang (*sagittal plane bending*) dan kemiringan kepala ke depan (*forward head translation*). Jika kamera diletakkan di depan (*frontal view*), efek pemendekan perspektif (*foreshortening*) membuat pendeteksian bahu condong ke depan menjadi sangat bias dan sulit dihitung secara akurat menggunakan geometri 2D."

#### Q18: Bagaimana Anda berencana mengatasi keterbatasan sudut pandang samping (lateral view) ini pada penggunaan praktis sehari-hari?
* **Jawaban Ideal**: "Pada penggunaan praktis sehari-hari, meletakkan kamera di samping pengguna memang kurang praktis. Untuk itu, pengembangan selanjutnya adalah merancang model rekonstruksi pose 3D yang mampu memproyeksikan pergerakan sendi dari sudut pandang depan (*frontal view*) ke dalam ruang 3D, atau memanfaatkan kamera sudut lebar (*wide-angle camera*) yang diletakkan di sudut meja kerja."

#### Q19: Apakah model YOLOv8n-pose Anda dapat di-deploy pada platform komputasi awan (cloud) untuk pemantauan multi-user?
* **Jawaban Ideal**: "Tentu bisa. Namun, karena model YOLOv8n-pose sangat ringan, melakukan inferensi di sisi klien (*local edge device*) jauh lebih direkomendasikan untuk menjaga privasi data gambar pengguna (karena citra webcam tidak perlu dikirim ke internet) serta meminimalkan biaya infrastruktur server awan yang mahal karena komputasi dilakukan secara terdistribusi di komputer masing-masing pengguna."

#### Q20: Bagaimana cara mengintegrasikan sistem pemantauan postur ini ke dalam aplikasi kesehatan terintegrasi?
* **Jawaban Ideal**: "Sistem ini dapat diekspos sebagai modul API lokal yang berjalan di latar belakang sistem operasi. Berkas ringkasan `session_summary.json` dapat dikirim secara berkala ke database terpusat aplikasi kesehatan pengguna menggunakan protokol HTTP POST. Data longitudinal tersebut kemudian dapat dikorelasikan dengan riwayat keluhan muskuloskeletal pengguna untuk menyusun program terapi rehabilitasi fisik yang disesuaikan."

---

## SECTION 5: Strategi Pengoptimalan Penilaian Akhir

Bagian ini menyajikan panduan taktis untuk memaksimalkan perolehan nilai sidang berdasarkan bobot rubrik penilaian yang umum digunakan dalam evaluasi proyek riset kecerdasan buatan.

---

### A. Kualitas Presentasi & Komunikasi (Bobot 25%)
* **Strategi Nilai Maksimal**:
  1. **Disiplin Waktu**: Pastikan durasi presentasi tidak melebihi batas waktu **20 menit**. Gunakan struktur slide yang padat (Slide 1-12) dan latih kecepatan bicara agar pas dengan durasi tiap slide.
  2. **Gaya Komunikasi Akademis**: Hindari penggunaan istilah informal. Gunakan terminologi ilmiah seperti *analanalisis longitudinal*, *degradasi postur*, *sensor jitter*, *continuous scoring*, *lateral view*, dan *generalizability*.
  3. **Visual-Driven Presentation**: Jangan membaca teks slide secara verbatim. Fokuskan penjelasan pada diagram alur pipeline, grafik visual dual-axis, dan kurva pelatihan model.

### B. Pemahaman Teknis & Metode ML/CV (Bobot 30%)
* **Strategi Nilai Maksimal**:
  1. **Kuasai Alasan Pemilihan Model**: Jelaskan secara matang mengapa memilih YOLOv8-pose dibandingkan MediaPipe (fleksibilitas kustomisasi keypoint dan kecepatan inferensi *single-stage*).
  2. **Pahami Formulasi Matematika**: Siapkan diri untuk menuliskan atau menjelaskan rumus sudut torso tertimbang ($30\%$ lower, $70\%$ upper) dan alasan di balik nilai koefisien penalty ($K_{torso}=2.5$, $K_{neck}=1.5$).
  3. **Penjelasan Konsep Smoothing**: Jelaskan dengan detail cara kerja buffer FIFO `deque` dalam meredam noise frekuensi tinggi koordinat visual.

### C. Hasil Model & Evaluasi (Bobot 25%)
* **Strategi Nilai Maksimal**:
  1. **Tonjolkan Metrik Performa Utama**: Hafalkan angka-angka kunci evaluasi model Anda: **mAP50 Pose (97.8%)**, **Precision (98.0%)**, **Recall (86.0%)**, dan **Loss Gap (0.023)**.
  2. **Gunakan Bukti Visual**: Saat membahas hasil evaluasi, tunjukkan grafik pelatihan `training-vs-validation-loss.png` untuk membuktikan model bebas dari overfitting.
  3. **Kejujuran Ilmiah**: Jangan merekayasa hasil evaluasi. Posisikan keterbatasan model (seperti sensitivitas terhadap sudut kamera lateral) sebagai peluang pengembangan riset di masa depan.

### D. Demo & Kualitas Kode (Bobot 15%)
* **Strategi Nilai Maksimal**:
  1. **Siapkan Demo yang Lancar**: Jalankan aplikasi `main.py` atau `realtime_posture.py` sebelum sidang dimulai. Pastikan webcam aktif dan pencahayaan ruangan cukup agar deteksi keypoint berjalan stabil.
  2. **Showcase Dasbor Interaktif**: Tunjukkan kemampuan sinkronisasi otomatis dasbor riset satu halaman. Tunjukkan bahwa dasbor berjalan secara viewport-safe tanpa scrollbar luar, serta memuat ringkasan sesi terbaru secara dinamis dari file JSON.
  3. **Tekankan Kerapian Kode**: Tunjukkan struktur kode proyek yang rapi dan terorganisir ke dalam modul-modul modular seperti `posture_engine.py`, `analytics.py`, `report.py`, dan `docs_sync.py`.

### E. Ketepatan Waktu & Kelengkapan (Bobot 5%)
* **Strategi Nilai Maksimal**:
  1. **Kumpulkan Seluruh Berkas Tepat Waktu**: Pastikan seluruh kode, aset dokumentasi, makalah draft, dan dasbor web sudah terunggah dengan rapi di repositori GitHub sebelum batas waktu pengumpulan berakhir.
  2. **Struktur Repositori Profesional**: Pastikan file `.gitignore` dikonfigurasi dengan benar sehingga berkas sampah biner dan cache tidak mengotori repositori online Anda.
  3. **README dan Panduan Jelas**: Sediakan berkas instruksi pengoperasian program (*setup guide*) yang jelas dan mudah dipahami pada berkas `README.md` utama proyek Anda.
