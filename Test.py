import VigenereCipher

encrypted = VigenereCipher.encrypt("hell-o wor ld!", "SECURITY")
print(encrypted)

new_key = VigenereCipher.set_key("hell-o wor ld!", "SECURITY")
print(new_key)

original = VigenereCipher.decrypt(encrypted, "SECURITY")
print(original)

#coset = VigenereCipher.find_smallest_chi_squared(alphabet_only_text, 0, 3)
#print(coset)

encrypted2 = VigenereCipher.encrypt("MICHIGAN TECHNOLOGICAL UNIVERSITY", "BOY")
print(encrypted2)

original2 = VigenereCipher.decrypt(encrypted2, "BOY")
print(original2)

broken = VigenereCipher.break_with_key_length(encrypted2, 3)
print(broken)

encrypted3 = VigenereCipher.encrypt("My father was born at the height of clouds. He entered the world wailing, "
                                    "lungs pumping the mountain air and desperate for oxygen. He lived because he had "
                                    "the breath of a Kalenjin, as had his father and his grandfather before, "
                                    "a long line of proud and noble descendants from the ancient tribe of highlanders "
                                    "from the hills of the Great Rift Valley. "
                                    "He grew up at an altitude where visiting relatives from the lowlands fainted and "
                                    "had to sit and take a rest from the sky. A village where the rhythm of life was "
                                    "set by the stars and the moon, the sun and the rain, a village where horseless "
                                    "cowboys herded the cattle, and my father and his brothers ran down the strays "
                                    "barefoot. "
                                    "Like all Kalenjin boys he ran everywhere. He ran to school. He ran home from "
                                    "school. He ran to gather firewood. He ran to the river to fetch water and spilt "
                                    "none running back. He ran but did not race. Running was not a sport. It was a "
                                    "way of life.", "SECURITY")
print(encrypted3)

#broken = VigenereCipher.break_with_key_length(encrypted3, 8)
#print(broken)

original3 = VigenereCipher.decrypt(encrypted3, "SECURITY")
print(original3)

broken2 = VigenereCipher.complete_break(encrypted3)
print(broken2)

broken3 = VigenereCipher.complete_break("NWAIWEBB RFQFOCJPUGDOJ VBGWSPTWRZ")
print(broken3)
