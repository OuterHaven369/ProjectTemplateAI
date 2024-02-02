"""
DynamicTemplateGenerator.py automates the creation of a project's directory structure with the unique feature of generating file content templates using OpenAI's API. It prompts for an OpenAI API key, allows model selection, and saves the key securely in an .env file. This script is ideal for projects requiring pre-populated files with context-specific templates, enhancing the initial setup process with AI-driven content creation.

Features:
- Environment variable management for secure API key storage.
- Dynamic file content generation using OpenAI API.
- Model selection capability for tailored content creation.
- Error handling for robust operation.

Usage:
Designed to be executed with a path to a YAML configuration, facilitating the automatic generation of directories and files with AI-generated content, streamlining project setup.
"""


import os
import glob
import yaml
import openai
from dotenv import load_dotenv, set_key

# Path to the .env file
env_file = 'C:/Users/Racin/Projects/.Library/.env'

# Check if .env file exists, if not create it
if not os.path.exists(env_file):
    open(env_file, 'w').close()

# Load environment variables from the specified .env file
load_dotenv(env_file)
openai.api_key = os.getenv("OPENAI_API_KEY")


# If the API key is not set, prompt the user to enter it and save to .env file
if not openai.api_key:
    openai_api_key = input("Enter your OpenAI API Key: ")
    # Save the API key in the .env file
    set_key(env_file, "OPENAI_API_KEY", openai_api_key)
    openai.api_key = openai_api_key
    # Reload the environment variables
    load_dotenv(env_file)

def get_available_models():
    """Fetch the list of available models from OpenAI."""
    try:
        models = openai.Model.list()  # Corrected this line
        return [model.id for model in models.data]
    except Exception as e:
        print(f"Error fetching models: {e}")
        return []


def select_model():
    """Allow the user to select a model from the list of available models, excluding chat models."""
    models = get_available_models()
    # Filter out chat models or other incompatible models
    filtered_models = [model for model in models if "chat" not in model]

    if not filtered_models:
        print("No suitable models available.")
        return None

    print("Available Models:")
    for index, model in enumerate(filtered_models, start=1):
        print(f"{index}. {model}")

    try:
        selected = int(input("Select a model number: ")) - 1
        return filtered_models[selected]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return None


def get_template_from_openai(prompt, model, temperature=0.7, max_tokens=150, top_p=1, frequency_penalty=0, presence_penalty=0, stop=None):
    """Generate a template using OpenAI based on the given prompt and model type."""
    try:
        is_chat_model = 'turbo' in model
        is_code_model = 'code' in model

        if is_chat_model:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "system", "content": "You are a helpful assistant."},
                          {"role": "user", "content": prompt}]
            )
        elif is_code_model:
            response = openai.Completion.create(
                model=model,
                prompt=prompt,
                temperature=0.5, 
                max_tokens=250
            )
        else:
            response = openai.Completion.create(
                model=model,
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stop=stop
            )

        # Check if response contains an error message
        if hasattr(response, 'choices') and response.choices:
            return response.choices[0].text.strip()
        else:
            print("Error: Received invalid response from OpenAI.")
            return None

    except openai.APIError as e:
        print(f"An error occurred: {e}")
        return None

def list_yaml_files(directory):
    """List all YAML files in the specified directory."""
    return glob.glob(os.path.join(directory, '*.yaml'))

def load_yaml_file(file_path):
    """Load a YAML file and return its content."""
    with open(file_path, 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)

def create_directory_structure(structure, model, current_path=""):
    """Recursively create a directory structure based on the provided structure and fill with templates."""
    for item, value in structure.items():
        item_path = os.path.join(current_path, item)
        if isinstance(value, dict):
            os.makedirs(item_path, exist_ok=True)
            create_directory_structure(value, model, item_path)
        elif isinstance(value, list):
            for file_name in value:
                if isinstance(file_name, str):
                    file_path = os.path.join(item_path, file_name)
                    parent_directory = os.path.dirname(file_path)
                    os.makedirs(parent_directory, exist_ok=True)
                    prompt = f"Create a template for a file named '{file_name}'"
                    # if promt fails stop and ask for user input to enter openai key

                    template_code = get_template_from_openai(prompt, model)
                    if template_code:
                        with open(file_path, 'w') as file:
                            file.write(template_code)

def main():
    yaml_dir = 'C:/Users/Racin/Projects/.Library/DynamicDirectoryStructureBuilder/structures'
    yaml_files = list_yaml_files(yaml_dir)

    if not yaml_files:
        print("No YAML files found in the specified directory.")
        return

    print("Available YAML files:")
    for i, yaml_file in enumerate(yaml_files):
        print(f"{i + 1}. {os.path.basename(yaml_file)}")

    selected_yaml_file = None
    while not selected_yaml_file:
        try:
            selected_index = int(input("Enter the number of the YAML file to use: ")) - 1
            selected_yaml_file = yaml_files[selected_index]
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid number for the YAML file.")

    structure = load_yaml_file(selected_yaml_file)
    selected_model = select_model()
    if selected_model:
        try:
            create_directory_structure(structure, selected_model)
            print(f"Directory structure created using '{os.path.basename(selected_yaml_file)}'.")
        except Exception as e:
            print(f"An error occurred while creating directory structure: {e}")
            # Decide whether to stop the script or allow re-selection
            return
    else:
        print("Model selection is required to proceed.")
        return

if __name__ == "__main__":
    main()
