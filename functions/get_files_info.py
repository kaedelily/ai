import os

def get_files_info(working_directory, directory=None):
    """
    Retrieves information about files and directories within a specified
    working directory, respecting boundary constraints.

    Args:
      working_directory: The base directory where file operations are permitted.
      directory: A relative path within the working_directory to inspect.
                 If None, inspects the working_directory itself.

    Returns:
      A string formatted with file/directory info, or an error string.
    """
    try:
        # Construct the full path
        if directory is None:
            full_path = working_directory
        else:
            full_path = os.path.join(working_directory, directory)

        # Normalize the path to handle cases like '..' and '.'
        normalized_full_path = os.path.normpath(full_path)

        # Get the absolute path of the working directory
        abs_working_directory = os.path.abspath(working_directory)

        # Check if the normalized full path is within the working directory
        # The commonpath of the absolute working directory and the normalized full path should be
        # the same as the absolute working directory.
        if os.path.commonpath([abs_working_directory, normalized_full_path]) != abs_working_directory:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if the path is a directory
        if not os.path.isdir(normalized_full_path):
            return f'Error: "{directory or "."}" is not a directory'

        # List the contents of the directory
        entries = os.listdir(normalized_full_path)

        # Build the output string
        output = ""
        for entry in entries:
            entry_path = os.path.join(normalized_full_path, entry)
            try:
                # Check if it's a directory
                is_dir = os.path.isdir(entry_path)
                # Get file size (will raise an error for directories, which we catch)
                file_size = os.path.getsize(entry_path) if not is_dir else 0
                output += f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}\n"
            except FileNotFoundError:
                output += f"- {entry}: Error getting info (FileNotFoundError)\n"
            except PermissionError:
                output += f"- {entry}: Error getting info (PermissionError)\n"
            except Exception as e:
                output += f"- {entry}: Error getting info ({type(e).__name__})\n"

        return output.strip()  # Remove trailing newline

    except FileNotFoundError:
        return f'Error: Working directory "{working_directory}" not found'
    except PermissionError:
        return f'Error: Permission denied for working directory "{working_directory}"'
    except Exception as e:
        return f'Error: An unexpected error occurred: {type(e).__name__}'
