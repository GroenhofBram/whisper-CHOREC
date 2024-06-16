## BACKUP BEFORE RUNNIGN THIS CODE!!! ##

import os
import shutil
import stat


validation_path = r"D:\repos\wav2vec-CHOREC\output\GroNLP-VALIDATION_SET-wav2vec2-dutch-large-ft-cgn"
training_path = r"D:\repos\wav2vec-CHOREC\output\GroNLP-TRAINING_SET-wav2vec2-dutch-large-ft-cgn"


all_items_validation = os.listdir(validation_path)
validation_directories = [item for item in all_items_validation if os.path.isdir(os.path.join(validation_path, item))]


all_items_training = os.listdir(training_path)
training_directories = [item for item in all_items_training if os.path.isdir(os.path.join(training_path, item))]

# Needs to write 
def handle_remove_readonly(func, path, exc_info):
    exc_type, exc_value, exc_tb = exc_info
    if exc_type is PermissionError:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        raise

# Remove directories 
for dir_name in training_directories:
    if dir_name not in validation_directories:
        dir_path = os.path.join(training_path, dir_name)
        print(f"Removing directory: {dir_path}")  # Print the directory being removed
        shutil.rmtree(dir_path, onerror=handle_remove_readonly)
