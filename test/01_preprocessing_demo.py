import os
import random
import torch
from torchvision import transforms
from PIL import Image

def demo_preprocessing(dataset_dir):
    print("=== TAHAP 1: INPUT GAMBAR DARI DATASET ASLI ===")
    
    try:
        # Cek apakah folder ada
        if not os.path.exists(dataset_dir):
            print(f"Error: Folder '{dataset_dir}' nggak ketemu. Cek lagi path-nya ya!")
            return

        # Ambil semua file gambar di dalam folder
        valid_extensions = ('.jpg', '.jpeg', '.png')
        image_files = [f for f in os.listdir(dataset_dir) if f.lower().endswith(valid_extensions)]
        
        if not image_files:
            print(f"Waduh, nggak nemu file gambar di folder {dataset_dir}")
            return
            
        # Pilih satu gambar secara acak buat di-demo-in
        sample_file = random.choice(image_files)
        image_path = os.path.join(dataset_dir, sample_file)
        
        print(f"Membaca file dari folder train: {sample_file}")
        
        # Load gambar pake PIL
        img = Image.open(image_path).convert("RGB")
        print(f"Status: Gambar berhasil di-load!")
        print(f"Ukuran asli (Lebar x Tinggi): {img.size}")
        print(f"Mode Warna: {img.mode}")
    except Exception as e:
        print(f"Error loading gambar: {e}")
        return

    print("\n=== TAHAP 2: PREPROCESSING (RESIZE, TENSOR, NORMALIZE) ===")
    # Bikin pipeline preprocessing persis kayak format dosen
    # Walau udah 224x224, Resize tetep dipasang sebagai standar safety pipeline
    preprocess_pipeline = transforms.Compose([
        transforms.Resize((224, 224)), 
        transforms.ToTensor(),         
        transforms.Normalize(          
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    # Eksekusi gambar ke dalam pipeline
    img_tensor = preprocess_pipeline(img)
    
    # Tambahin dimensi batch (B, C, H, W) biar formatnya siap masuk ke model
    img_tensor_batch = img_tensor.unsqueeze(0) 

    print(f"Bentuk Tensor Asli (C, H, W): {list(img_tensor.shape)}")
    print(f"Total Nilai (Pixels x Channels): {img_tensor.numel():,}")
    print(f"Bentuk Tensor Siap Model (Batch, C, H, W): {list(img_tensor_batch.shape)}")
    print(f"Tipe Data: {img_tensor.dtype}")
    
    print("\n=== CEK NILAI CHANNEL RGB (SAMPLE) ===")
    print(f"Channel Merah (R) max/min : {img_tensor[0].max().item():.2f} / {img_tensor[0].min().item():.2f}")
    print(f"Channel Hijau (G) max/min : {img_tensor[1].max().item():.2f} / {img_tensor[1].min().item():.2f}")
    print(f"Channel Biru  (B) max/min : {img_tensor[2].max().item():.2f} / {img_tensor[2].min().item():.2f}")
    
    print("\n[PROGRESS DONE] Gambar dari dataset sukses dikonversi menjadi matrix angka dan siap diproses GPU!")

if __name__ == "__main__":
    # Path langsung diarahkan ke folder dataset train kamu
    # Pastikan file script ini posisinya sejajar dengan folder "data" ya
    folder_dataset = "data/train/SittingPosture-train"
    demo_preprocessing(folder_dataset)