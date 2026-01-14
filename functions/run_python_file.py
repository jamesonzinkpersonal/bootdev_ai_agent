import os
import subprocess
from config import MAX_CHARS  # <-- use this name
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file within the working directory and returns its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional list of arguments to pass to the Python script",
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        completed_process = subprocess.run(["python", file_path, *args], cwd=working_directory, timeout=30, capture_output=True, text=True)
        if not completed_process.stdout and not completed_process.stderr:
            return "No output produced"

        result = f"STDOUT:{completed_process.stdout}\nSTDERR:{completed_process.stderr}"    

        if completed_process.returncode != 0:
            result += f"\nProcess exited with code {completed_process.returncode}"
        
        return result
    
    except Exception as e:
        return f"Error: executing Python file: {e}"