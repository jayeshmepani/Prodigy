def encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def decrypt(text, shift):
    return encrypt(text, -shift)

# Example usage with user input
plaintext = input("Enter the plaintext: ")
shift = int(input("Enter the shift value: "))

ciphertext = encrypt(plaintext, shift)
decryptedtext = decrypt(ciphertext, shift)

print("Plaintext:", plaintext)
print("Encrypted:", ciphertext)
print("Decrypted:", decryptedtext)
