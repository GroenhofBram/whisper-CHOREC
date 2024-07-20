import os
import stat

def remove_readonly(func, path, _):
    # Change the file or directory to writable and reattempt the removal
    os.chmod(path, stat.S_IWRITE)
    func(path)

def remove_empty_dirs(directory):
    for root, dirs, files in os.walk(directory, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):  # Check if directory is empty
                try:
                    print(f'Removing empty directory: {dir_path}')
                    os.rmdir(dir_path)
                except PermissionError:
                    print(f'Permission denied: {dir_path}. Attempting to change permissions and retry.')
                    try:
                        os.chmod(dir_path, stat.S_IWRITE)
                        os.rmdir(dir_path)
                    except Exception as e:
                        print(f'Failed to remove directory: {dir_path}. Reason: {e}')

# Specify the directory to search for empty directories
directory_path = r"D:\repos\whisper-CHOREC\output\GroNLP-FULLFULL-WHISPERwav2vec2-dutch-large-ft-cgn"

# Call the function to remove empty directories
remove_empty_dirs(directory_path)
