def count_char_frequency(s):
    frequency_dict = {}
    for char in s:
        if char in frequency_dict:
            frequency_dict[char] += 1
        else:
            frequency_dict[char] = 1
    return frequency_dict

input_string = input("Enter a string: ")
frequency = count_char_frequency(input_string)
print("Character frequencies:", frequency)