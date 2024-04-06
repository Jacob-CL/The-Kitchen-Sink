import os
import sys

def print_file_contents(file_path):
    print(f"\nContents of file '{file_path}':")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            contents = file.read()
            print(contents)
    except UnicodeDecodeError:
        print("Could not read the file contents. The file might not be a text file.")
    except Exception as e:
        print(f"Error reading file: {e}")

def list_files_and_folders(directory):
    # Check if the provided directory path exists
    if not os.path.exists(directory):
        print(f"The directory '{directory}' does not exist.")
        return

    # Check if the provided path is indeed a directory
    if not os.path.isdir(directory):
        print(f"The path '{directory}' is not a directory.")
        return

    # List everything in the directory
    entries = os.listdir(directory)

    # Separate files and folders
    files = []
    folders = []

    for entry in entries:
        full_path = os.path.join(directory, entry)
        if os.path.isfile(full_path):
            files.append(entry)
        elif os.path.isdir(full_path):
            folders.append(entry)

    # Print the files and folders
    print(f"Contents of directory '{directory}':\n")
    
    print("Folders:")
    for folder in folders:
        print(f"  {folder}")

    print("Files:")
    for file in files:
        print(f"  {file}")
        # Check if the directory is 'testfolder1' and print file contents
        if 'testfolder1' in directory:  # Adjust this condition as needed
            print_file_contents(os.path.join(directory, file))

if __name__ == "__main__":
    # Check if a directory path is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory_path>")
    else:
        directory_path = sys.argv[1]
        list_files_and_folders(directory_path)
