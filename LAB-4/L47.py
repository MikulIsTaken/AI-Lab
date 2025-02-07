def longest_unique_substring(s):
    start = 0
    max_len = 0
    max_substr = ""
    char_map = {}

    for end in range(len(s)):
        char = s[end]

        if char in char_map and char_map[char] >= start:
            start = char_map[char] + 1

        char_map[char] = end

        if end - start + 1 > max_len:
            max_len = end - start + 1
            max_substr = s[start:end + 1]

    return max_substr, max_len

input_string = input("Enter a string: ")

substring, length = longest_unique_substring(input_string)
print("Longest substring with all unique characters:", substring)
print("Length of the substring:", length)