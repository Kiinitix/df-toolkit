import struct
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes

AES_KEY_LENGTH = 32
AES_BLOCK_SIZE = 16

def encrypt_aes_key(aes_key, public_key):
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    return encrypted_aes_key

def aes_encrypt(plaintext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_plaintext = plaintext + (AES_BLOCK_SIZE - len(plaintext) % AES_BLOCK_SIZE) * \
                       bytes([AES_BLOCK_SIZE - len(plaintext) % AES_BLOCK_SIZE])
    ciphertext = cipher.encrypt(padded_plaintext)
    return ciphertext


def generate_rsa_key(passphrase):
    key = RSA.generate(2048)
    private_key = key.export_key(passphrase=passphrase, pkcs=8, protection="scryptAndAES128-CBC")
    public_key = key.publickey().export_key()
    return private_key, public_key

def save_key_to_file(key, filename):
    with open(filename, 'wb') as f:
        f.write(key)

def encrypt_file(input_filename, output_filename, public_key):
    with open(input_filename, 'rb') as f:
        file_content = f.read()

    aes_key = get_random_bytes(AES_KEY_LENGTH)
    encrypted_aes_key = encrypt_aes_key(aes_key, public_key)

    iv = get_random_bytes(AES_BLOCK_SIZE)
    encrypted_file_content = aes_encrypt(file_content, aes_key, iv)

    with open(output_filename, 'wb') as f:
        f.write(struct.pack('<Q', len(encrypted_aes_key)))
        f.write(encrypted_aes_key)
        f.write(struct.pack('<Q', len(encrypted_file_content)))
        f.write(iv + encrypted_file_content)

    print("Encryption successful. Encrypted file:", output_filename)

def mainMenu(input_filename, output_filename):
    passphrase = input("Enter passphrase to protect private key: ")
    private_key, public_key = generate_rsa_key(passphrase)

    save_key_to_file(private_key, "private_key.pem")
    save_key_to_file(public_key, "public_key.pem")

    encrypt_file(input_filename, output_filename, RSA.import_key(public_key))
