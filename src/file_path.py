from islinux import is_linux

linux_file_path_base = f"/vol/bigdata/corpora/CHOREC-1.0/data"
windows_local_file_path = f"D:\\repos\\wav2vec-CHOREC\\files\\test_glob"

def get_file_path(input_file_name):
    if is_linux:
        return f"{linux_file_path_base}/{input_file_name}"
    return f"{windows_local_file_path}\\{input_file_name}"