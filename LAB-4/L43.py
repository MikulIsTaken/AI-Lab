def calculate_average_scores(scores_dict):
    average_scores = {}
    for student, scores in scores_dict.items():
        if scores:
            average_scores[student] = sum(scores) / len(scores)
        else:
            average_scores[student] = 0
    return average_scores

n = int(input("Enter the number of students: "))
scores_dict = {}

for _ in range(n):
    student = input("Enter student name: ")
    scores = input("Enter scores separated by spaces: ").split()
    scores = [float(score) for score in scores]
    scores_dict[student] = scores
average_scores = calculate_average_scores(scores_dict)
print("Average scores:", average_scores)