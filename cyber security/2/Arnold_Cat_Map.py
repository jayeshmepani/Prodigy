from PIL import Image
import numpy as np
import os

def arnold_cat_map(image, iterations=1):
    n = image.shape[0]
    transformed_image = np.copy(image)
    for _ in range(iterations):
        new_image = np.copy(transformed_image)
        for x in range(n):
            for y in range(n):
                new_x = (x + y) % n
                new_y = (x + 2 * y) % n
                new_image[new_x, new_y] = transformed_image[x, y]
        transformed_image = new_image
    return transformed_image

def inverse_arnold_cat_map(image, iterations=1):
    n = image.shape[0]
    transformed_image = np.copy(image)
    for _ in range(iterations):
        new_image = np.copy(transformed_image)
        for x in range(n):
            for y in range(n):
                new_x = (2 * x - y) % n
                new_y = (-x + y) % n
                new_image[new_x, new_y] = transformed_image[x, y]
        transformed_image = new_image
    return transformed_image

def arnold_encrypt_decrypt(image_path, iterations, encrypt=True):
    image = Image.open(image_path)
    image_data = np.array(image)
    
    if encrypt:
        processed_data = arnold_cat_map(image_data, iterations)
    else:
        processed_data = inverse_arnold_cat_map(image_data, iterations)
    
    return Image.fromarray(processed_data)

def process_folder_arnold(folder_path, iterations, encrypt=True):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            processed_image = arnold_encrypt_decrypt(file_path, iterations, encrypt)
            processed_image.save(f"{file_path}_processed.png")

def main():
    choice = input("Select 1. Encrypt or 2. Decrypt: ")
    iterations = int(input("Enter the number of iterations: "))
    
    path = input("Enter the image file or folder path: ")
    
    if os.path.isdir(path):
        process_folder_arnold(path, iterations, encrypt=choice == '1')
    else:
        processed_image = arnold_encrypt_decrypt(path, iterations, encrypt=choice == '1')
        if processed_image:
            processed_image.save("processed_image.png")
            print("Image processed and saved as 'processed_image.png'")
        else:
            print("Failed to process the image.")

if __name__ == "__main__":
    main()
