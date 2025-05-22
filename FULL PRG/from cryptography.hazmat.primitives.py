from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def rc4_encrypt(plaintext, key):
  """
  Encrypts plaintext using RC4 stream cipher.

  Args:
      plaintext: The plaintext data to encrypt (bytes).
      key: The secret key (bytes).

  Returns:
      The ciphertext (bytes).
  """

  # Derive key and initialization vector (IV) using HKDF
  from cryptography.hazmat.primitives import hashes, hmac
  kdf = hmac.HMAC(hashes.SHA256(), key_size=16)
  kdf_derive = kdf.new(key)
  key = kdf_derive.derive(b"rc4-key")
  iv = kdf_derive.derive(b"rc4-iv")

  # Create cipher
  cipher = Cipher(algorithms.ARC4(key), modes.CTR(iv))
  encryptor = cipher.encryptor()

  # Encrypt plaintext
  ciphertext = encryptor.update(plaintext) + encryptor.finalize()
  return ciphertext

def rc4_decrypt(ciphertext, key):
  """
  Decrypts ciphertext using RC4 stream cipher.

  Args:
      ciphertext: The ciphertext to decrypt (bytes).
      key: The secret key (bytes).

  Returns:
      The decrypted plaintext (bytes).
  """

  # Derive key and IV using the same HKDF approach as in encryption
  kdf = hmac.HMAC(hashes.SHA256(), key_size=16)
  kdf_derive = kdf.new(key)
  key = kdf_derive.derive(b"rc4-key")
  iv = kdf_derive.derive(b"rc4-iv")

  # Create cipher
  cipher = Cipher(algorithms.ARC4(key), modes.CTR(iv))
  decryptor = cipher.decryptor()

  # Decrypt ciphertext
  plaintext = decryptor.update(ciphertext) + decryptor.finalize()
  return plaintext

# Example usage
plaintext = b"\x00\x11"  # Binary representation of "0011"
key = b"\x10\x10"  # Binary representation of "1010"

ciphertext = rc4_encrypt(plaintext, key)
decrypted_text = rc4_decrypt(ciphertext, key)

print("Plaintext:", plaintext.hex())
print("Ciphertext:", ciphertext.hex())
print("Decrypted Text:", decrypted_text.hex())
