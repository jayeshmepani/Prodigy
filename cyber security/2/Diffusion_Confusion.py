from PIL import Image
import numpy as np
import os

def diffusion_confusion(image_path, key, encrypt=True):
    image = Image.open(image_path)
    image_data = np.array(image)
    np.random.seed(key)
    
    if encrypt:
        # Diffusion: shuffle pixels
        shuffled_indices = np.random.permutation(image_data.size)
        flat_image_data = image_data.flatten()
        shuffled_data = flat_image_data[shuffled_indices]
        encrypted_data = shuffled_data.reshape(image_data.shape)
    else:
        # Reverse diffusion
        shuffled_indices = np.random.permutation(image_data.size)
        flat_image_data = image_data.flatten()
        unshuffled_data = np.empty_like(flat_image_data)
        unshuffled_data[shuffled_indices] = flat_image_data
        encrypted_data = unshuffled_data.reshape(image_data.shape)
    
    return Image.fromarray(encrypted_data)

def process_folder_diffusion_confusion(folder_path, key, encrypt=True):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            processed_image = diffusion_confusion(file_path, key, encrypt)
            processed_image.save(f"{file_name}_processed.png")

def main():
    choice = input("Select 1. Encrypt or 2. Decrypt: ")
    key = int(input("Enter the key (integer): "))
    
    path = input("Enter the image file or folder path: ")
    
    if os.path.isdir(path):
        process_folder_diffusion_confusion(path, key, encrypt=choice == '1')
    else:
        processed_image = diffusion_confusion(path, key, encrypt=choice == '1')
        if processed_image:
            processed_image.save("processed_image.png")
            print("Image processed and saved as 'processed_image.png'")
        else:
            print("Failed to process the image.")

if __name__ == "__main__":
    main()
