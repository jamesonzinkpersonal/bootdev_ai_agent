from google import genai
from google.genai import types
from functions.get_file_content import *
from functions.get_files_info import *
from functions.run_python_file import *
from functions.write_file import *
from config import WORKING_DIR

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

def call_function(function_call, verbose=False):
    
    func_name = function_call.name or ""
    func_args = function_call.args
    
    if verbose:
        print(f" - Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")
    
    local_func = function_map.get(func_name)
    
    if not local_func:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"},
                )
            ],
        )
    
    args = dict(func_args) if func_args else {}
    args["working_directory"] = WORKING_DIR # or from config
    result = local_func(**args)

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=func_name,
            response={"result": result},
        )
    ],
)
