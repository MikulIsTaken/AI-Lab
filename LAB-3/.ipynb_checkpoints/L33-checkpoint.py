def second_largest(numbers):
    unique_numbers = []
    for num in numbers:
        if num not in unique_numbers:
            unique_numbers.append(num)
    if len(unique_numbers) < 2:
        return None
    unique_numbers.sort()
    return unique_numbers[-2]
numbers = list(map(int, input("Enter numbers separated by spaces: ").split()))
result = second_largest(numbers)
if result is None:
    print("There is no second largest element.")
else:
    print("Second largest element:", result)