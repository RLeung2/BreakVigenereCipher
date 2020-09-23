from collections import deque


#
#
# Main code for Encrypt Task
#
#
def is_alphabet(character):
    code = ord(character)

    if (65 <= code <= 90) or (97 <= code <= 122):
        return True
    return False


def set_key(string, key):
    new_key = []
    index_offset = 0  # offset due to non_alphabetic characters

    for i in range(0, len(string)):
        if not is_alphabet(string[i]):
            index_offset += 1
            new_key.append(string[i])
        else:
            new_key.append(key[(i - index_offset) % len(key)])
    return "".join(new_key)


def encrypt(plaintext, key):
    # If the input key is blank, simply return the plaintext
    if key == "":
        return plaintext

    fixed_key = set_key(plaintext, key)

    cipher_text = []
    lower_case = False
    for i in range(0, len(plaintext)):

        if not is_alphabet(plaintext[i]):
            cipher_text.append(plaintext[i])
            continue

        char_code = ord(plaintext[i])

        if plaintext[i].islower():
            lower_case = True
            char_code -= 32

        unicode = (char_code + ord(fixed_key[i])) % 26
        unicode += ord('A')

        if lower_case:
            unicode += 32
            lower_case = False

        cipher_text.append(chr(unicode))

    return "".join(cipher_text)


#
#
# Main code for Decrypt Task
#
#
def decrypt(cipher_text, key):
    # If the input key is blank, simply return the cipher text
    if key == "":
        return cipher_text

    fixed_key = set_key(cipher_text, key)

    original_text = []
    lower_case = False
    for i in range(0, len(cipher_text)):

        if not is_alphabet(cipher_text[i]):
            original_text.append(cipher_text[i])
            continue

        char_code = ord(cipher_text[i])

        if cipher_text[i].islower():
            lower_case = True
            char_code -= 32

        unicode = (char_code - ord(fixed_key[i]) + 26) % 26
        unicode += ord('A')

        if lower_case:
            unicode += 32
            lower_case = False

        original_text.append(chr(unicode))

    return "".join(original_text)


#
#
# Main code for Task 3: Break the Vigenere cipher, knowing the key length
#
#
def alphabet_only(text):
    new_text = ""
    for x in text:
        if (65 <= ord(x) <= 90) or (97 <= ord(x) <= 122):
            new_text += x
    return new_text


def create_coset(text, index, key_length):
    coset = [text[i] for i in range(index, len(text), key_length)]
    return coset


# summation of every letter: (f - F)^2 / F
def chi_squared_test(actual_frequencies, observed_frequencies):
    total = 0
    for i in range(len(actual_frequencies)):
        current = ((observed_frequencies[i] - actual_frequencies[i]) ** 2) / actual_frequencies[i]
        total += current

    return total


def find_smallest_chi_squared(cipher_text, index, key_length):
    alphabet_only_text = alphabet_only(cipher_text)
    coset = create_coset(alphabet_only_text, index, key_length)

    actual_frequencies = [.082, .015, .028, .043, .13, .022, .02, .061, .07, .0015, .0077, .04, .024, .067, .075,
                          .019, .00095, .06, .063, .091, .028, .0098, .024, .0015, .02, .00075]
    observed_frequencies = deque([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

    # Keep track of the lowest chi squared value and the corresponding letter
    minimum = (float("inf"), '')

    # Check all 26 possible shifts
    for i in range(0, 26):
        if i == 0:
            for letter in coset:
                upper_case = letter.upper()
                index = ord(upper_case) - 65
                observed_frequencies[index] += 1

            for x in range(0, len(observed_frequencies)):
                observed_frequencies[x] = observed_frequencies[x] / len(coset)

            chi_squared_value = chi_squared_test(actual_frequencies, observed_frequencies)
            if chi_squared_value < minimum[0]:
                minimum = (chi_squared_value, chr(i + 65))

        else:
            # Rotate the frequencies left every iteration to get the new frequencies after every letter is shifted once
            observed_frequencies.rotate(-1)
            chi_squared_value = chi_squared_test(actual_frequencies, observed_frequencies)
            if chi_squared_value < minimum[0]:
                minimum = (chi_squared_value, chr(i + 65))

    return minimum


def break_with_key_length(cipher_text, key_length):
    # It doesnt make sense to find a key with key length greater than the cipher text length
    if key_length > len(cipher_text):
        key_length = len(cipher_text)

    keyword = ""
    for i in range(0, key_length):
        lowest_chi_squared = find_smallest_chi_squared(cipher_text, i, key_length)
        keyword += lowest_chi_squared[1]

    return keyword


#
#
# Main code for Task 4: Completely break the Vigenere cipher
#
#


# Apple index of coincidence equation on a coset
def calculate_index_of_coincidence(coset):
    letter_occurrences = [0] * 26  # number of occurrences of each letter in the coset

    for letter in coset:
        upper_case = letter.upper()
        index = ord(upper_case) - 65
        letter_occurrences[index] += 1

    summation = 0
    for occurrences in letter_occurrences:
        summation += (occurrences * (occurrences - 1))

    index_of_coincidence = summation / (len(coset) * (len(coset) - 1))
    return index_of_coincidence


def find_repeated_substrings(text):
    distance_mappings = {}  # maps repeated substring to a list of distances between them
    # Find repeated substrings of length 3 to 10
    for substring_length in range(3, 11):
        # Loop through entire text for repeats
        for start_index in range(0, len(text) - substring_length):
            substring = text[start_index: start_index + substring_length]

            for i in range(start_index + substring_length, len(text) - substring_length):
                # If a match is found
                if text[i: i + substring_length] == substring:
                    distance_mappings.setdefault(substring, [])  # Set empty list if first repeat is found
                    distance_mappings[substring].append(i - start_index)  # Append distance to repeat to the list

    return distance_mappings


# Get factors up to 100 because max key length was said to be 100 on Piazza
def get_factors_up_to_100(num):
    factors = []

    # 100 is max key length
    for i in range(2, 100 + 1):
        if num % i == 0:
            factors.append(i)

    return set(factors)


# Using the mappings of repeated substrings to distances,
# Keeps counts of all factors up to 100 and returns a sorted list of tuples: [(factor, frequency)]
def get_factor_frequencies(distance_mappings):
    factor_frequencies = {}
    sorted_frequencies = []

    for substring in distance_mappings:
        # For each distance, get its factors up to 100 and add their counts to the dictionary
        for distance in distance_mappings[substring]:
            factors = get_factors_up_to_100(distance)
            for factor in factors:
                factor_frequencies.setdefault(factor, 0)
                factor_frequencies[factor] += 1

    # Convert the dictionary to a sorted list of tuples
    for factor in factor_frequencies:
        sorted_frequencies.append((factor, factor_frequencies[factor]))
    sorted_frequencies.sort(key=lambda x: x[1], reverse=True)

    return sorted_frequencies


# Given a sorted list of (factor, frequency) tuples, return a list of most common factors that should be useful
# I take the top 3 frequencies under the condition that the 2nd and 3rd highest frequencies are not 1
# If the highest frequency is 1, then all of the factors will be returned
# If the second highest frequency is 1, only the top frequency will be considered
# If the third highest frequency is 1, only the top 2 frequencies will be considered
# If the top 3 frequencies are not 1, then the top 3 will be considered
# Example tuple structure: (2, 6) where 2 is the factor and 6 is the number of times it occurs
def get_most_common_factors(factor_frequencies):
    if not factor_frequencies:
        return []

    most_common_factors = []
    highest_count = factor_frequencies[0][1]  # The first tuple will have the highest count
    second_highest_count = 1  # I want to check the 2nd highest count as well as long as it is not 1
    third_highest_count = 1  # I want the 3rd highest count as long as it is not 1

    index = 0
    # for pair in factor_frequencies:
    while index < len(factor_frequencies):
        # If there are ties for the highest count, add those factors to be checked later
        if factor_frequencies[index][1] == highest_count:
            most_common_factors.append(factor_frequencies[index][0])
            index += 1

        # If the second highest count is not 1, we check for those factors as well
        # I don't want factors that occur once because chances are they are not as useful as the factors
        # that occur multiple times
        elif factor_frequencies[index][1] != 1:
            second_highest_count = factor_frequencies[index][1]
            break

        else:
            break

    # If the second highest count is not 1, add those factors to the list
    if second_highest_count != 1:
        while index < len(factor_frequencies):
            if factor_frequencies[index][1] == second_highest_count:
                most_common_factors.append(factor_frequencies[index][0])
                index += 1

            # If the third highest count is not 1, we check for those factors as well
            # Same reasons stated above
            elif factor_frequencies[index][1] != 1:
                third_highest_count = factor_frequencies[index][1]
                break

            else:
                break

    # If the third highest count is not 1, add those factors to the list
    if third_highest_count != 1:
        while index < len(factor_frequencies):
            if factor_frequencies[index][1] == third_highest_count:
                most_common_factors.append(factor_frequencies[index][0])
                index += 1
            else:
                break

    return most_common_factors


# A pseudo implementation of the kasiski method to fit this problem
def kasiski_method(text):
    alphabet_only_text = alphabet_only(text)

    distance_mappings = find_repeated_substrings(alphabet_only_text)  # Maps all repeated strings to the distances
    factor_frequencies = get_factor_frequencies(distance_mappings)  # Sorted counts of all factor occurrences
    most_common_factors = get_most_common_factors(factor_frequencies)  # List of most common factors

    return most_common_factors


# Applies Kasiski's method and the Index of Coincidence in order to find the most likely key length
def complete_break(cipher_text):
    alphabet_only_text = alphabet_only(cipher_text)
    greatest_average_ic = (0, 0)

    # This implementation of Kasiski's method returns a list of likely key lengths based on repeated substrings
    # found in the cipher text
    possible_key_lengths = kasiski_method(cipher_text)

    # If there are no repeated substrings of length 3 to 10, kasiski_method() will return an empty list
    # If this is the case, then just check all possible key lengths from 1 to 100 at most
    # Or at most the max key length checked is half the length of the cipher text
    if not possible_key_lengths:
        possible_key_lengths = [i for i in range(1, min(100, len(cipher_text) // 2))]

    # Use the Index of Coincidence equation to find the most likely key length out of all the given possibilities
    for key_length in possible_key_lengths:

        sum_of_ic = 0

        # Loop through every coset and calculate the IC of each to find the average
        for x in range(0, key_length):
            coset = create_coset(alphabet_only_text, x, key_length)
            current_ic = calculate_index_of_coincidence(coset)
            sum_of_ic += current_ic

        average_ic = sum_of_ic / key_length
        if average_ic > greatest_average_ic[0]:
            greatest_average_ic = (average_ic, key_length)

    # The key length with the greatest IC is likely to be the correct key length
    found_key_length = greatest_average_ic[1]
    key = break_with_key_length(cipher_text, found_key_length)

    return key
