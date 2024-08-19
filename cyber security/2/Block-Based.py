from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from PIL import Image
import numpy as np
import os

def pad(data):
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    return padded_data

def unpad(data):
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(data) + unpadder.finalize()
    return unpadded_data

def aes_encrypt(image_data, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    padded_data = pad(image_data)
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_data

def aes_decrypt(encrypted_data, key):
    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
    decrypted_data = unpad(decrypted_padded_data)
    return decrypted_data

def process_image_aes(image_path, key, encrypt=True):
    if encrypt:
        image = Image.open(image_path)
        image_mode = image.mode
        image_data = np.array(image)
        
        if image_mode == 'RGBA':
            image_data = image_data[:, :, :3]
        elif image_mode == 'L':
            pass  # grayscale images
        elif image_mode == 'RGB':
            pass  # color images
        else:
            raise ValueError("Unsupported image format")

        flat_image_data = image_data.tobytes()
        
        # Store the image dimensions at the beginning of the data
        image_size = np.array(image_data.shape, dtype=np.int32)
        size_data = image_size.tobytes()
        processed_data = aes_encrypt(size_data + flat_image_data, key)
        
        return processed_data
    else:
        with open(image_path, "rb") as f:
            encrypted_data = f.read()
        
        decrypted_data = aes_decrypt(encrypted_data, key)
        
        # Read the dimensions from the start of the data
        image_size = np.frombuffer(decrypted_data[:12], dtype=np.int32)
        flat_image_data = decrypted_data[12:]
        processed_data = np.frombuffer(flat_image_data, dtype=np.uint8)
        processed_data = processed_data.reshape(tuple(image_size))
        
        return Image.fromarray(processed_data)

def process_folder_aes(folder_path, key, encrypt=True):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            if encrypt:
                processed_data = process_image_aes(file_path, key, encrypt=True)
                with open(f"{file_name}_processed.enc", "wb") as f:
                    f.write(processed_data)
            else:
                processed_image = process_image_aes(file_path, key, encrypt=False)
                processed_image.save(f"{file_name}_processed.png")

def main():
    choice = input("Select 1. Encrypt or 2. Decrypt: ")
    key = input("Enter the key (16, 24, or 32 bytes): ").encode()
    
    if len(key) not in [16, 24, 32]:
        print("Invalid key length. Must be 16, 24, or 32 bytes.")
        return
    
    path = input("Enter the image file or folder path: ")
    
    if os.path.isdir(path):
        process_folder_aes(path, key, encrypt=choice == '1')
    else:
        if choice == '1':
            processed_data = process_image_aes(path, key, encrypt=True)
            with open("processed_image.enc", "wb") as f:
                f.write(processed_data)
            print("Image encrypted and saved as 'processed_image.enc'")
        else:
            processed_image = process_image_aes(path, key, encrypt=False)
            processed_image.save("processed_image.png")
            print("Image decrypted and saved as 'processed_image.png'")

if __name__ == "__main__":
    main()
