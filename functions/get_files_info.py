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
