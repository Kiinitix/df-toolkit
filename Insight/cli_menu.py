import subprocess
import pkg_resources
import importlib

modules_to_check = ['carving', 'disk_analyzer', ' file_explorer', 'hex_reader', 'magic_cipher', 'timeline_analysis']

def list_installed_packages():
    """
    Get a list of installed packages.
    """
    return [pkg.key for pkg in pkg_resources.working_set]

def list_available_modules(modules_to_check):
    """
    Get a list of available modules specified in the script.
    """
    available_modules = []

    # Check availability of modules
    for module_name in modules_to_check:
        if importlib.util.find_spec(module_name) is not None:
            available_modules.append(module_name)

    return available_modules

def write_available_modules_to_file(available_modules, output_file):
    """
    Write the list of available modules to a text file.
    """
    with open(output_file, 'w') as file:
        for module_name in available_modules:
            file.write(module_name + '\n')

    print("List of available modules has updated")

def install_modules(modules):
    """
    Install selected modules using pip.
    """
    for module in modules:
        subprocess.call(['pip3', 'install', module])

def print_menu():
    print("\nMenu:")
    print("1. List available modules (Including installed ones)")
    print("2. Install modules")
    print("3. Exit")

def update():
    available_modules_file = "available_modules.txt"

    available_modules = list_available_modules(modules_to_check)
    write_available_modules_to_file(available_modules, available_modules_file)


def main():
    update()

    while True:
        print_menu()
        choice = input("\nEnter your choice: ")

        if choice == '1':
            available_modules = list_available_modules(modules_to_check)
            installed_modules = list_installed_packages()
            print("-" * 50)
            print("\nAvailable Modules (Including Installed Ones):")
            for index, module in enumerate(available_modules, start=1):
                if module in installed_modules:
                    print(f"{index}. {module} (Installed)")
                else:
                    print(f"{index}. {module}")
            print("-" * 50)

        elif choice == '2':
            installed_modules = list_installed_packages()
            available_modules = list_available_modules(modules_to_check)
            print("-" * 50)
            print("\nAvailable Modules (Excluding Installed Ones):")
            for index, module in enumerate(available_modules, start=1):
                print(f"{index}. {module}")
            selected_indices = input("\nEnter the numbers of modules to download (comma-separated): ").split(",")
            selected_modules = [available_modules[int(index) - 1] for index in selected_indices if available_modules[int(index) - 1] not in installed_modules]

            print("Installing selected modules...")
            install_modules(selected_modules)
            print("Installation complete!")
            print("-" * 50)

        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main()
