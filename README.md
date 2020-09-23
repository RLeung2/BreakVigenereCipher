# BreakVigenereCipher
Implementing and breaking the Vigenere cipher

Task 1: Implement the Vigenère cipher encoder

	To implement the encoder, I first converted the given key into a new key based on the plaintext. If the plaintext is longer than the key, then the key must be repeated for how many iterations necessary in the new key to match the length of the plaintext. Since only the alphabet is considered, spaces and special characters must be accounted for when creating the new key by simply adding that character to the new key for easy reference later. 
	To encrypt the plaintext, I looped through every character of the plaintext. In each loop, I first check if the current character is special. If so, I simply append it to the new encrypted text. If the character is of the alphabet, I convert the character to its Unicode integer equivalent. Then, I check if the character is lower case. If so, I subtract 32 from the code to get its upper case equivalent in order to calculate the encryption based on upper case characters for the time being. The encryption of each character is calculated by adding the code of the plaintext character to the code of the corresponding character in the new key, then modulo 26. After, I add the code for the letter ‘A’ to this value to get the encrypted letter. If the original letter was lower case, then I add 32 back to the value as well. This letter is then appended to the new encrypted text.

Task 2: Implement the Vigenère cipher decoder

	To implement the decoder, I first converted the given key into the new key based on the cipher text the same way described in Task 1.
	In the decryption loop, I did the same process described for encryption in Task 1 except for the code calculation. To go from an encrypted character to its original, I subtract the encrypted character code by the corresponding character code in the new key, add 26, then modulo 26. Special characters and lower case characters are handled the same way as in Task 1.

Task 3: Break the Vigenère cipher, knowing the key length

	To accomplish this task, I utilized the chi-squared method. The idea of this method is to break the cipher text into different cosets based on the key length, k. The first letter of the key would correspond with the first coset, which contains every kth letter in the cipher text starting at the first index. Repeating this for every position in the key gives you a total of k cosets. Each coset contains all the letters that would be shifted by its corresponding letter in the key. 
	For each coset, I first obtain the number of occurrences of each letter and divide each one by the length of the coset. This gives me the frequency of each letter in the coset, which will be used in my chi-squared calculation. I then perform the chi-squared calculation on it 26 different times. The chi-squared equation is a method in statistics to measure goodness-of-fit. I use the known frequencies of the alphabet in general English text to calculate the chi-squared value along with the frequencies in a coset. I must calculate this on a given coset 26 times for each shift possible due to a key letter. There are 26 letters in the alphabet, so there are 26 possibilities. The shift on a coset that provides the smallest chi-squared value is the most likely shift to have occurred from the original text, and the corresponding letter to that shift is likely to be part of the key.
	By doing this for every generated coset, I get a letter for each coset and append that to my key to be returned in the end.

Function descriptions:

alphabet_only(text) – Takes a given text and returns the text without any non-alphabetic characters. This returns a string.
create_coset(text, index, key_length) – Creates a coset of a given text by first starting on the index given, and then using the key length as steps to take on the text. This returns a list of characters.

chi_squared_test(actual_frequencies, observed_frequencies) – Calculates the chi-squared value using the frequencies of a given coset (observed_frequencies) and the known frequencies in English text (actual_frequencies). This returns a float.

 find_smallest_chi_squared(cipher_text, index, key_length) – Finds the smallest chi-squared value found for a given coset and returns the corresponding letter. Passing all three parameters into the create_coset() method provides the desired coset to observe. The known letter frequencies in English text are kept in a list variable called actual_frequencies. A double ended queue (deque) is used to represent the observed frequencies in the coset (observed_frequencies). The minimum variable holds a tuple to keep track of the lowest chi-squared value and its corresponding letter. The for loop runs 26 times, once for each letter in the alphabet. In the first loop, the frequency of each letter in the coset is recorded and added to their corresponding positions in the deque. Then, the chi-squared value is calculated for those frequencies. If that value is smaller than this current minimum value, the minimum tuple variable is replaced with the new minimum and new corresponding letter. For every loop after the first, instead of recalculating the frequencies after shifting every letter once to the left, I just rotate the deque once to the left. This is equivalent because every ‘A’ will become a ‘Z’, and the frequency for ‘A’ will just rotate one spot over to the ‘Z’ position. This returns a tuple.
break_with_key_length(cipher_text, key_length) – Generates the key based on the smallest chi-squared value of each coset. Loops through the key length, and for each coset appends the letter returned in the tuple from the find_smallest_chi_squared() method each loop to the result. This returns a string.


Task 4: Completely break the Vigenère cipher

	To break the cipher without knowing the key length, I utilized two methods: Kasiski’s method and the index of coincidence. Kasiski’s method attempts to find the most likely key lengths based on repeated substrings in the cipher text. For any repeated substring, the distance between the duplicates is likely to be a multiple of the actual key length. So, after finding all distances of repeated substrings, we can break each distance into its factors. The factors that occur the most often are likely candidates for the actual key length. Out of these possible candidates, I then utilize the idea of the index of coincidence to choose the most likely key length.
	Given a text string, the index of coincidence (IC) is the probability of two randomly selected letters being equal. The IC of general English text is 0.066332. The IC of randomly generated text would be 0.038466. We can apply this to out problem by calculating IC’s for given cosets. For any given key length, we can generate all the cosets that would result and find the IC for each coset. Then, we can take the average IC of all the cosets and use that to represent the IC of a given key length. The key length that provides the highest average IC is most likely to be the actual key length of the cipher.
	After finding the key length, we can just run the break_with_key_length() method in Task 3 to find the actual key. The Vigenère cipher has now been broken.

Function descriptions:
calculate_index_of_coincidence(coset) – Calculates the average index of coincidence of a given coset. This returns a float.
find_repeated_substrings(text) – Finds all repeated substrings and maps them to the distances between matches in a dictionary variable. Only substrings of length 3 to 10 are checked for. This returns a dictionary of strings mapped to integers.

get_factors_up_to_100(num) – Generates all the factors up to 100 for a given number. No factors above 100 are considered because the max key length for this task is said to be 100. This returns a list of integers.

get_factor_frequencies(distance_mappings) - Using the mappings of repeated substrings to distances, keeps counts of all factors up to 100 and returns a sorted list of tuples. Each tuple contains the substring and its number of occurrences. This returns a list of tuples.
get_most_common_factors(factor_frequencies) - Given a sorted list of (factor, frequency) tuples, return a list of most common factors that should be useful. This method takes the top 3 highest number of occurrences as long as the second or third highest number is not 1. If there are factors that occur multiple times, it should not be useful to check for a bunch of factors that occur once. This returns a list of integers.

kasiski_method(text) – Implements Kasiski’s method by calling previous methods to obtain the most common factors, which are likely to be the key length. This returns a list of integers.

complete_break(cipher_text) – Implements both Kasiski’s method and the index of coincidence. First, kasiski_method() is called to obtain a list of likely key lengths to be checked. Then, we loop through these key lengths and calculate the index of coincidence each one would produce. The key length that results in the highest IC is the key length to be selected. The break_with_key_length() is then called to find the actual key.
