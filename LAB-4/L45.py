def first_non_repeating_char(s):
    frequency_dict = {}
    for char in s:
        if char in frequency_dict:
            frequency_dict[char] += 1
        else:
            frequency_dict[char] = 1
    for char in s:
        if frequency_dict[char] == 1:
            return char
    return "None"

input_string = input("Enter a string: ")
result = first_non_repeating_char(input_string)
print("First non-repeating character:", result)