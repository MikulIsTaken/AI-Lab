def fibonacci_series():
    try:
        terms=int(input("Enter the number of terms: "))
        a,b=0,1
        count=0
        print("Fibonacci series:")
        while count<terms:
            print(a,end=" ")
            a,b=b,a+b
            count+=1
        print()
    except ValueError:
        print("Invalid input. Please enter an integer.")
fibonacci_series()