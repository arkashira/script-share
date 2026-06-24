import argparse
import json
import dataclasses
import os
import sys
import zipfile

@dataclasses.dataclass
class Script:
    filename: str
    dependencies: list

def upload_script(script_filename, dependencies_filename):
    try:
        with open(script_filename, 'r') as f:
            script_content = f.read()
        with open(dependencies_filename, 'r') as f:
            dependencies_content = f.read()
        dependencies = dependencies_content.splitlines()
        return Script(os.path.basename(script_filename), dependencies)
    except FileNotFoundError:
        raise ValueError("Script or dependencies file not found")

def generate_executable(script, output_filename):
    try:
        with zipfile.ZipFile(output_filename, 'w') as zip_file:
            zip_file.writestr('script.py', script.filename)
            for dependency in script.dependencies:
                zip_file.writestr(dependency, '')
        return output_filename
    except Exception as e:
        raise ValueError("Failed to generate executable") from e

def main():
    parser = argparse.ArgumentParser(description='Generate a standalone executable')
    parser.add_argument('--script', help='Path to the Python script')
    parser.add_argument('--dependencies', help='Path to the dependencies file')
    parser.add_argument('--output', help='Path to the output executable')
    args = parser.parse_args()
    script = upload_script(args.script, args.dependencies)
    output_filename = generate_executable(script, args.output)
    print(f"Executable generated: {output_filename}")

if __name__ == "__main__":
    main()
