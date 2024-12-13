def rectangle_vs_square():
    try:
        length=float(input("Enter the length of the rectangle: "))
        width=float(input("Enter the width of the rectangle: "))
        rectangle_area=length*width
        square_side=width/2
        square_area=square_side**2
        print(f"Area of the rectangle: {rectangle_area}")
        print(f"Area of the square: {square_area}")
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
rectangle_vs_square()