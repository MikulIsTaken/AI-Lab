def longest_increasing_subsequence(nums):
    max_len = 0
    curr_len = 0
    subsequence = []
    temp_subseq = []
    for i in range(len(nums)):
        if i == 0 or nums[i] > nums[i-1]:
            curr_len += 1
            temp_subseq.append(nums[i])
        else:
            if curr_len > max_len:
                max_len = curr_len
                subsequence = temp_subseq[:]
            curr_len = 1
            temp_subseq = [nums[i]]
    if curr_len > max_len:
        max_len = curr_len
        subsequence = temp_subseq[:]
    return max_len, subsequence
nums = list(map(int, input("Enter the numbers separated by spaces: ").split()))
length, subsequence = longest_increasing_subsequence(nums)
print("Longest Increasing Subsequence Length:", length)
print("Longest Increasing Subsequence:", subsequence)