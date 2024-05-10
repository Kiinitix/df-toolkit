import struct
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP

AES_BLOCK_SIZE = 16

def decrypt_aes_key(encrypted_aes_key, private_key):
    cipher_rsa = PKCS1_OAEP.new(private_key)
    aes_key = cipher_rsa.decrypt(encrypted_aes_key)
    return aes_key

def aes_decrypt(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext.rstrip(b'\0')

def decrypt_file(input_filename, output_filename, private_key):
    with open(input_filename, 'rb') as f:
        aes_key_length = struct.unpack('<Q', f.read(struct.calcsize('Q')))[0]
        encrypted_aes_key = f.read(aes_key_length)
        file_content_length = struct.unpack('<Q', f.read(struct.calcsize('Q')))[0]
        iv = f.read(AES_BLOCK_SIZE)
        encrypted_file_content = f.read()

    aes_key = decrypt_aes_key(encrypted_aes_key, private_key)
    plaintext = aes_decrypt(encrypted_file_content, aes_key, iv)

    with open(output_filename, 'wb') as f:
        f.write(plaintext)

    print("Decryption successful. Decrypted file:", output_filename)

def decrypt(input_filename, output_filename):
    passphrase = input("Enter passphrase used to protect private key: ")
    private_key = RSA.import_key(open('private_key.pem').read(), passphrase=passphrase)
    decrypt_file(input_filename, output_filename, private_key)
