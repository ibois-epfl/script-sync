#! python3

import my_module

if __name__ == "__main__":
    print("script-sync::running main()")
    my_module.print_from_my_module()

    list_test = [1, 2, 3, 4, 5]
    nested_list_test = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    o_out = nested_list_test
