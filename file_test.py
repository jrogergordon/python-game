
import os

# Get the current directory
directory = '/home/jrogergordon/python_game/'

# List the files in the directory
file_options = os.listdir(directory)

# Print the file options
print("Files available in the directory:")
for file_option in file_options:
    print(file_option)
