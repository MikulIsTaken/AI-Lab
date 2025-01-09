def calculate_area(shape, *dimensions):
    if shape == "triangle":
        base, height = dimensions
        return 0.5 * base * height
    elif shape == "square":
        side, = dimensions
        return side * side
    elif shape == "rectangle":
        length, width = dimensions
        return length * width
    elif shape == "circle":
        radius, = dimensions
        return 3.14159 * radius * radius
    else:
        return "Invalid shape."
shape = input("Enter the shape (triangle, square, rectangle, circle): ").lower()
if shape == "triangle":
    base = float(input("Enter the base of the triangle: "))
    height = float(input("Enter the height of the triangle: "))
    print("Area:", calculate_area(shape, base, height))
elif shape == "square":
    side = float(input("Enter the side of the square: "))
    print("Area:", calculate_area(shape, side))
elif shape == "rectangle":
    length = float(input("Enter the length of the rectangle: "))
    width = float(input("Enter the width of the rectangle: "))
    print("Area:", calculate_area(shape, length, width))
elif shape == "circle":
    radius = float(input("Enter the radius of the circle: "))
    print("Area:", calculate_area(shape, radius))
else:
    print("Invalid shape.")