def word_frequency(words):
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1
    return frequency
words = input("Enter words separated by spaces: ").split()
result = word_frequency(words)
print("Word frequency:", result)