import os

from google import genai
from google.genai import types

def get_files_info(working_directory, directory="."):
    abs_working_dir = os.path.abspath(working_directory)
    abs_target_dir = os.path.abspath(os.path.join(working_directory, directory))
    abs_working_dir_with_sep = abs_working_dir + os.sep
    if not (abs_target_dir == abs_working_dir or abs_target_dir.startswith(abs_working_dir_with_sep)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'  
    
    if not os.path.isdir(abs_target_dir):
        return f'Error: "{directory}" is not a directory'

    try:
        entries = os.listdir(abs_target_dir)
        lines = []
        for name in entries:
            entry_path = os.path.join(abs_target_dir, name)
            size = os.path.getsize(entry_path)
            is_dir = os.path.isdir(entry_path)
            line = f"- {name}: file_size={size} bytes, is_dir={is_dir}"
            lines.append(line)
        
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)