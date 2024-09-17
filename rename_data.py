import os

def rename_files(folder_path, prefix):
    files = sorted([f for f in os.listdir(folder_path) if f.endswith('.tif')])
    
    for i, filename in enumerate(files, start=1):
        new_filename = f"{prefix}{i:04d}.tif"
        src = os.path.join(folder_path, filename)
        dst = os.path.join(folder_path, new_filename)
        os.rename(src, dst)
        print(f"Renamed: {filename} -> {new_filename}")

def main():
    images_folder = 'data/data_2/images'
    masks_folder = 'data/data_2/masks'

    # Renomear os arquivos na pasta de imagens
    rename_files(images_folder, '')

    # Renomear os arquivos na pasta de máscaras
    rename_files(masks_folder, '')

if __name__ == "__main__":
    main()
