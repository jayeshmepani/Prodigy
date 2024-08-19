from PIL import Image
import numpy as np
import os

def logistic_map(x, r=3.99):
    return r * x * (1 - x)

def chaos_encrypt_decrypt(image_path, key, encrypt=True):
    try:
        image = Image.open(image_path)
        image_data = np.array(image).flatten()

        # Generate chaotic sequence
        chaotic_sequence = np.empty_like(image_data, dtype=np.float64)
        chaotic_sequence[0] = key
        for i in range(1, len(chaotic_sequence)):
            chaotic_sequence[i] = logistic_map(chaotic_sequence[i - 1])

        # Scale chaotic sequence to pixel values
        chaotic_sequence = (chaotic_sequence * 255).astype(np.uint8)

        # Encrypt or decrypt
        if encrypt:
            processed_data = np.bitwise_xor(image_data, chaotic_sequence)
        else:
            processed_data = np.bitwise_xor(image_data, chaotic_sequence)

        processed_image = processed_data.reshape(image.size[1], image.size[0], -1)
        processed_image = Image.fromarray(processed_image)
        return processed_image
    except Exception as e:
        print(f"Error processing image: {e}")
        return None

def process_folder_chaos(folder_path, key, encrypt=True):
    try:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                processed_image = chaos_encrypt_decrypt(file_path, key, encrypt)
                if processed_image:
                    processed_image.save(f"{file_path}_processed.png")
    except Exception as e:
        print(f"Error processing folder: {e}")

def main():
    try:
        choice = input("Select 1. Encrypt or 2. Decrypt: ")
        key = float(input("Enter the key (a float between 0 and 1): "))
        path = input("Enter the image file or folder path: ")

        if os.path.isdir(path):
            process_folder_chaos(path, key, encrypt=choice == '1')
        else:
            processed_image = chaos_encrypt_decrypt(path, key, encrypt=choice == '1')
            if processed_image:
                processed_image.save("processed_image.png")
                print("Image processed and saved as 'processed_image.png'")
            else:
                print("Failed to process the image.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
