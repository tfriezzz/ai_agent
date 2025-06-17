import os
from functions.get_file_content import get_files_info


def get_file_content(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    # abs_file_path = os.path.join(working_directory, file_path)

    if not file_path.startswith(working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    MAX_CHARS = 10000

    try:
        with open(file_path, "r") as f:
            if len(f.read) < 10000:
                return f.read
            elif len(f.read) > 10000:
                file_content_string = f.read(MAX_CHARS)
                return f'{file_content_string} ...File "{file_path}" truncated at 10000 characters'

    except Exception as e:
        return f"Error: {e}"
