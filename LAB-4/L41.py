def remove_duplicates(lst):
    result = []
    for item in lst:
        if item not in result:
            result.append(item)
    return result

user_input = input("Enter the list elements separated by spaces: ")
input_list = user_input.split()
output_list = remove_duplicates(input_list)
print("List after removing duplicates:", output_list)