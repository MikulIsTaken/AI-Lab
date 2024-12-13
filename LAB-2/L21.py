def add_numbers():
    num1=input("Enter the first number: ")
    num2=input("Enter the second number: ")
    try:
        result=float(num1)+float(num2)
        print(f"The result of addition is: {result}")
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
add_numbers()