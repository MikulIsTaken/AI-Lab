def rotate_matrix(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(i, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()
    return matrix
n = int(input("Enter the size of the square matrix (NxN): "))
matrix = []
for _ in range(n):
    matrix.append(list(map(int, input().split())))
print("Original Matrix:")
for row in matrix:
    print(row)
rotated_matrix = rotate_matrix(matrix)
print("Rotated Matrix:")
for row in rotated_matrix:
    print(row)