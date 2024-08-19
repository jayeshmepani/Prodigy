import os
from PIL import Image

def process_image(image_path, output_path, key, mode):
    image = Image.open(image_path)
    pixels = image.load()

    for i in range(image.width):
        for j in range(image.height):
            r, g, b = pixels[i, j]
            r = r ^ key
            g = g ^ key
            b = b ^ key
            pixels[i, j] = (r, g, b)

    image.save(output_path)
    print(f"Image {'encrypted' if mode == 'e' else 'decrypted'} and saved as {output_path}")

def process_folder(folder_path, key, mode):
    for filename in os.listdir(folder_path):
        if filename.endswith(('png', 'jpg', 'jpeg', 'bmp', 'tiff', 'gif')):
            file_path = os.path.join(folder_path, filename)
            output_path = os.path.join(folder_path, f"{mode}_{filename}")
            process_image(file_path, output_path, key, mode)

def main():
    # Get user inputs
    path = input("Input img (single file or folder path): ")
    mode_input = input("Select 1. encrypt or 2. decrypt: ")
    key = int(input("Enter the key: "))

    # Validate mode
    mode = 'e' if mode_input == '1' else 'd' if mode_input == '2' else None
    if not mode:
        print("Invalid selection for mode. Please enter 1 for encrypt or 2 for decrypt.")
        return

    if os.path.isfile(path):
        output_path = f"{mode}_{os.path.basename(path)}"
        process_image(path, output_path, key, mode)
    elif os.path.isdir(path):
        process_folder(path, key, mode)
    else:
        print(f"Invalid path: {path}")

if __name__ == '__main__':
    main()
