def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Cannot divide by zero"
    return x / y

def calculator():
    print("Select operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")

    choice = input("Enter choice(1/2/3/4): ")

    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))

    if choice == '1':
        result = str(num1) + " + " + str(num2) + " = " + str(add(num1, num2))

    elif choice == '2':
        result = str(num1) + " - " + str(num2) + " = " + str(subtract(num1, num2))

    elif choice == '3':
        result = str(num1) + " * " + str(num2) + " = " + str(multiply(num1, num2))

    elif choice == '4':
        result = str(num1) + " / " + str(num2) + " = " + str(divide(num1, num2))
    else:
        result = "Invalid input"

    with open("result.txt", "w") as f:
        f.write(result)

if __name__ == "__main__":
    calculator()