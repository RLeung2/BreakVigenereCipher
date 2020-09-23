import VigenereCipher

text = input()
key = input()
decrypted = VigenereCipher.decrypt(text, key)
print(decrypted)