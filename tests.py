import unittest
import os
import tempfile

# Assuming get_files_info is in functions/get_files_info.py
from functions.get_files_info import get_files_info

class TestGetFilesInfo(unittest.TestCase):

    def setUp(self):
        # Create a temporary working directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.working_directory = self.temp_dir.name

        # Create some files and directories within the working directory
        os.makedirs(os.path.join(self.working_directory, 'subdir'))
        with open(os.path.join(self.working_directory, 'file1.txt'), 'w') as f:
            f.write("This is a test file.")
        with open(os.path.join(self.working_directory, 'subdir', 'file2.md'), 'w') as f:
            f.write("# Heading")

    def tearDown(self):
        # Clean up the temporary working directory
        self.temp_dir.cleanup()

    def test_list_working_directory(self):
        result = get_files_info(self.working_directory)
        self.assertTrue("- subdir: file_size=0 bytes, is_dir=True" in result)
        self.assertTrue("- file1.txt: file_size=20 bytes, is_dir=False" in result) # Check size of file1.txt

    def test_list_subdir(self):
        result = get_files_info(self.working_directory, directory='subdir')
        self.assertTrue("- file2.md: file_size=9 bytes, is_dir=False" in result) # Check size of file2.md

    def test_directory_outside_working_directory(self):
        # Attempt to access a directory outside the working directory
        result = get_files_info(self.working_directory, directory='../')
        self.assertTrue(result.startswith("Error: Cannot list"))

    def test_invalid_directory_path(self):
        # Attempt to access a file as a directory
        result = get_files_info(self.working_directory, directory='file1.txt')
        self.assertTrue(result.startswith("Error: \"file1.txt\" is not a directory"))

    def test_nonexistent_directory(self):
        # Attempt to access a non-existent directory
        result = get_files_info(self.working_directory, directory='nonexistent_dir')
        self.assertTrue(result.startswith("Error:"))

    def test_nonexistent_working_directory(self):
        # Attempt to use a non-existent working directory
        result = get_files_info("/nonexistent/working/dir")
        self.assertTrue(result.startswith("Error: Working directory"))


if __name__ == '__main__':
    unittest.main()