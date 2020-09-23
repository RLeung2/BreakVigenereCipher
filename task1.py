import VigenereCipher

text = input()
key = input()
encrypted = VigenereCipher.encrypt(text, key)
print(encrypted)
