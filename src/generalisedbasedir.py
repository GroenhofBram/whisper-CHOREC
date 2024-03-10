from islinux import is_linux
from pathing import get_abs_folder_path

LINUX_BASE_DIR = "/vol/bigdata/corpora/CHOREC-1.0/data"
WINDOWS_BASE_DIR = get_abs_folder_path("files\\test_glob")

def get_base_dir_for_generalised_path():
    if is_linux():
        return LINUX_BASE_DIR
    return f"{WINDOWS_BASE_DIR}"