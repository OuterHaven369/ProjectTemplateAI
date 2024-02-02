"""
SimpleDirectoryBuilder.py provides a lightweight solution for generating a project's directory structure based on YAML file configurations. Without the need for internet connectivity or external APIs, it efficiently creates directories and placeholder files as specified, making it suitable for quick project initialization.

Features:
- Direct parsing and execution of YAML configurations for directory structure.
- Simple and straightforward execution without external dependencies.
- Efficient creation of directories and files, including handling of empty directories.

Usage:
Run with a path to a YAML configuration to quickly establish the backbone of a project structure, ideal for users seeking simplicity and speed in project setup.
"""


import os
import glob
import yaml

def list_yaml_files(directory):
    """List all YAML files in the specified directory."""
    return glob.glob(os.path.join(directory, '*.yaml'))

def load_yaml_file(file_path):
    """Load a YAML file and return its content."""
    with open(file_path, 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)

def create_directory_structure(structure, current_path=""):
    """Recursively create a directory structure based on the provided structure."""
    for item, value in structure.items():
        item_path = os.path.join(current_path, item)
        if isinstance(value, dict):
            os.makedirs(item_path, exist_ok=True)
            create_directory_structure(value, item_path)
        elif isinstance(value, list):
            for file_name in value:
                if isinstance(file_name, str):
                    file_path = os.path.join(item_path, file_name)
                    parent_directory = os.path.dirname(file_path)
                    os.makedirs(parent_directory, exist_ok=True)
                    if file_name.endswith('.exe') or file_name == 'app_executable':
                        file_path += '.temp_exe.txt'  # Add a temporary extension
                    with open(file_path, 'w'): pass
                elif value == []:
                    os.makedirs(item_path, exist_ok=True)
        elif value is None:
            os.makedirs(item_path, exist_ok=True)

def main():
    yaml_dir = 'C:/Users/Racin/Projects/.Library/DynamicDirectoryStructureBuilder/structures'
    yaml_files = list_yaml_files(yaml_dir)

    if not yaml_files:
        print("No YAML files found in the specified directory.")
        return

    print("Available YAML files:")
    for i, yaml_file in enumerate(yaml_files):
        print(f"{i + 1}. {os.path.basename(yaml_file)}")

    while True:
        try:
            selected_index = int(input("Enter the number of the YAML file to use: ")) - 1
            selected_yaml_file = yaml_files[selected_index]
            structure = load_yaml_file(selected_yaml_file)
            create_directory_structure(structure)
            print(f"Directory structure created using '{os.path.basename(selected_yaml_file)}'.")
            break
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid number for the YAML file.")
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    main()
