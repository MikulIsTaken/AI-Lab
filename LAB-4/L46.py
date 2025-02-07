def top_3_employees_by_salary(salary_dict):
    sorted_employees = sorted(salary_dict.items(), key=lambda x: (-x[1], x[0]))
    top_3 = sorted_employees[:3]
    return top_3

n = int(input("Enter the number of employees: "))
salary_dict = {}

for _ in range(n):
    employee = input("Enter employee name: ")
    salary = float(input(f"Enter salary for {employee}: "))
    salary_dict[employee] = salary

top_3_employees = top_3_employees_by_salary(salary_dict)
print("Top 3 employees with the highest salaries:")
for employee, salary in top_3_employees:
    print(f"{employee}: {salary}")
