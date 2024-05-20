#! python3

import my_module
import my_package_name
import my_package_name.module_test
import my_package_name.submodule
import my_package_name.submodule.submodule_a
import my_package_name.submodule.submodule_b

if __name__ == "__main__":
    print("script-sync::running main()")
    my_module.print_from_my_module()
    my_package_name.module_test.module_test_hello()
    my_package_name.submodule.submodule_a.hello_submodule_a()
    my_package_name.submodule.submodule_b.hello_submodule_b()
