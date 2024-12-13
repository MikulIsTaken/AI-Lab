def advanced_calculator():
    expression = input("Enter a mathematical expression: ")
    try:
        result = eval(expression)
        print(f"The result is: {result}")
    except Exception as e:
        print(f"Error evaluating expression: {e}")
advanced_calculator()