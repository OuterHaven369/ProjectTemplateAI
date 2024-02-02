#!/usr/bin/env bash

# This is the entry point script for the ProjectSetupAI tool.

# Navigate to the project's root directory (adjust this path as necessary)
cd /path/to/ProjectSetupAI

# Activate your Python virtual environment if you have one
# source /path/to/venv/bin/activate

function show_usage() {
    echo "Usage: setup-project [command] [options]"
    echo "Commands:"
    echo "  dynamic-template   Generate project structure with dynamic templates"
    echo "  simple-builder     Generate project structure using simple directory builder"
    echo "  list-structures    List available YAML structure files"
    echo "Options:"
    echo "  --path <path>      Specify the path to the YAML file or directory"
    echo "  --model <model>    Specify the OpenAI model for template generation"
}

# Check if at least one argument is provided
if [ "$#" -eq 0 ]; then
    show_usage
    exit 1
fi

COMMAND=$1
shift

case "$COMMAND" in
    dynamic-template)
        MODEL="gpt-3.5-turbo" # Default model
        YAML_PATH=""
        while [ "$#" -gt 0 ]; do
            case "$1" in
                --path)
                    YAML_PATH="$2"
                    shift 2
                    ;;
                --model)
                    MODEL="$2"
                    shift 2
                    ;;
                *)
                    show_usage
                    exit 1
                    ;;
            esac
        done
        python src/dynamic_template_generator.py --path "$YAML_PATH" --model "$MODEL"
        ;;
    simple-builder)
        YAML_PATH=""
        while [ "$#" -gt 0 ]; do
            case "$1" in
                --path)
                    YAML_PATH="$2"
                    shift 2
                    ;;
                *)
                    show_usage
                    exit 1
                    ;;
            esac
        done
        python src/simple_directory_builder.py --path "$YAML_PATH"
        ;;
    list-structures)
        python src/structures_handler.py --list
        ;;
    *)
        show_usage
        ;;
esac
