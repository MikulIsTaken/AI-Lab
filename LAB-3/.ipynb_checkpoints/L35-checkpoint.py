def common_elements_squared(set1, set2):
    common = []
    for x in set1:
        if x in set2:
            common.append(x * x)
    return common
set1 = list(map(int, input("Enter elements of the first set separated by spaces: ").split()))
set2 = list(map(int, input("Enter elements of the second set separated by spaces: ").split()))
result = common_elements_squared(set1, set2)
print("Common elements squared:", result)