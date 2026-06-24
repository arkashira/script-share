import pytest
from src.packager import upload_script, generate_executable
import os
import sys
import tempfile

def test_upload_script():
    with tempfile.TemporaryDirectory() as tmp_dir:
        script_filename = os.path.join(tmp_dir, 'script.py')
        dependencies_filename = os.path.join(tmp_dir, 'dependencies.txt')
        with open(script_filename, 'w') as f:
            f.write('print("Hello World")')
        with open(dependencies_filename, 'w') as f:
            f.write('dependency1\ndependency2')
        script = upload_script(script_filename, dependencies_filename)
        assert script.filename == 'script.py'
        assert script.dependencies == ['dependency1', 'dependency2']

def test_upload_script_file_not_found():
    with pytest.raises(ValueError):
        upload_script('non_existent_script.py', 'dependencies.txt')

def test_generate_executable():
    with tempfile.TemporaryDirectory() as tmp_dir:
        script_filename = os.path.join(tmp_dir, 'script.py')
        dependencies_filename = os.path.join(tmp_dir, 'dependencies.txt')
        output_filename = os.path.join(tmp_dir, 'output.zip')
        with open(script_filename, 'w') as f:
            f.write('print("Hello World")')
        with open(dependencies_filename, 'w') as f:
            f.write('dependency1\ndependency2')
        script = upload_script(script_filename, dependencies_filename)
        output_filename = generate_executable(script, output_filename)
        assert os.path.exists(output_filename)

def test_generate_executable_failure():
    with pytest.raises(ValueError):
        generate_executable(None, 'output.zip')

def test_main():
    with tempfile.TemporaryDirectory() as tmp_dir:
        script_filename = os.path.join(tmp_dir, 'script.py')
        dependencies_filename = os.path.join(tmp_dir, 'dependencies.txt')
        output_filename = os.path.join(tmp_dir, 'output.zip')
        with open(script_filename, 'w') as f:
            f.write('print("Hello World")')
        with open(dependencies_filename, 'w') as f:
            f.write('dependency1\ndependency2')
        sys.argv = ['packager.py', '--script', script_filename, '--dependencies', dependencies_filename, '--output', output_filename]
        from src.packager import main
        main()
        assert os.path.exists(output_filename)
