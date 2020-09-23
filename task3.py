import VigenereCipher

text = input()
key_length = int(input())
decrypted_key = VigenereCipher.break_with_key_length(text, key_length)
print(decrypted_key)
decrypted_text = VigenereCipher.decrypt(text, decrypted_key)
print(decrypted_text)
