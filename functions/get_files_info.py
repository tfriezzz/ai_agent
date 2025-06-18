import os


def get_files_info(working_directory, directory=None):
    working_directory = os.path.abspath(working_directory)
    directory_path = os.path.join(working_directory, directory)

    if not directory_path.startswith(working_directory):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(directory_path):
        return f'Error: "{directory}" is not a directory'

    return_string = ""
    try:
        for file in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file)
            file_name = file
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)

            this_string = f"- {file_name}: file_size={file_size} is_dir={is_dir}\n"
            return_string = return_string + this_string

        return return_string

    except Exception as e:
        return f"Error: {e}"


def get_file_content(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.join(working_directory, file_path)

    if not abs_file_path.startswith(working_directory):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    MAX_CHARS = 10000

    try:
        with open(abs_file_path, "r") as f:
            text = f.read(MAX_CHARS + 1)
            if len(text) <= MAX_CHARS:
                return text
            elif len(text) > MAX_CHARS:
                return f'{text[:MAX_CHARS]}[...File "{file_path}" truncated at 10000 characters]'

    except Exception as e:
        return f"Error: {e}"


def write_file(working_directory, file_path, content):
    working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.join(working_directory, file_path)

    if not abs_file_path.startswith(working_directory):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        path_file = os.path.split(abs_file_path)
        my_path = path_file[0]
        my_file = path_file[1]
        if not os.path.exists(my_path):
            os.makedirs(my_path)

        with open(abs_file_path, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"
