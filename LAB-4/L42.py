def rotate_list(lst, k):
    n = len(lst)
    k = k % n
    return lst[-k:] + lst[:-k]

user_input = input("Enter the list elements separated by spaces: ")
input_list = user_input.split()
k = int(input("Enter the value of k (number of positions to rotate): "))
output_list = rotate_list(input_list, k)
print("List after rotating to the right by", k, "positions:", output_list)