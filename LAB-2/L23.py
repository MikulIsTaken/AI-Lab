def check_even_odd():
    try:
        num=int(input("Enter an integer: "))
        if num%2==0:
            print(f"{num} is even.")
        else:
            print(f"{num} is odd.")
    except ValueError:
        print("Invalid input. Please enter an integer.")
check_even_odd()