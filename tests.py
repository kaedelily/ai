from functions import get_file_content, write_file
from functions.get_files_info import get_files_info
from functions.run_python import run_python_file


def test():
    result = get_file_content({'file_path': 'main.py'})
    print(result)

    result = write_file({'file_path': 'main.txt', 'content': 'hello'})
    print(result)

    result = run_python_file({'file_path': 'main.py'})
    print(result)

    result = get_files_info({'directory': 'pkg'})
    print(result)


if __name__ == "__main__":
    test()
