#! python3

import my_module

def main() -> None:
    print("script-sync::running main()")
    my_module.print_from_my_module()

if __name__ == "__main__":
    main()