"""Simple demo Python app to be scanned by SonarQube."""


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def main():
    print("Simple Calculator")
    print("2 + 3 =", add(2, 3))
    print("5 - 2 =", subtract(5, 2))
    print("4 * 6 =", multiply(4, 6))
    print("10 / 2 =", divide(10, 2))


if __name__ == "__main__":
    main()
