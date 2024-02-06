#! python3

def main(x):
    y = 456
    a = x - y
    c = x + y
    b = 123456
    print("runner_script.py::main() function called")
    print(f"runner_script.py::b value: {b}")
    print(f"runner_script.py::c value: {c}")

    return a

if __name__ == '__main__':
    a = main(x)