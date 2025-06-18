import subprocess
import os


def run_python_file(working_directory, file_path):
    working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    file_type = os.path.splitext(file_path)

    if not abs_file_path.startswith(working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    if file_type[1] != ".py":
        return f'Error: "{file_path}" is not a Python file.'

    try:
        program = subprocess.run(
            ["python3", abs_file_path],
            cwd=working_directory,
            capture_output=True,
            timeout=30,
            text=True,
        )
        output = []
        program_stdout = program.stdout
        program_stderr = program.stderr
        program_exit_code = program.returncode

        output.append(f"STDOUT:{program_stdout}")
        output.append(f"STDERR:{program_stderr}")

        if program_exit_code != 0:
            output.append(f"Process exited with code {program_exit_code}")
            return "\n".join(output)
        if program_exit_code == 0 and not program_stdout and not program_stderr:
            return "No output produced."

        return "\n".join(output)

    except Exception as e:
        return f"Error: executing Python file: {e}"
