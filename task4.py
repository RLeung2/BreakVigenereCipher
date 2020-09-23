import VigenereCipher

text = input()
decrypted_key = VigenereCipher.complete_break(text)
print(decrypted_key)
decrypted_text = VigenereCipher.decrypt(text, decrypted_key)
print(decrypted_text)
