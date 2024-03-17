from islinux import is_linux
from pathing import get_abs_folder_path

LINUX_BASE_DIR_UNALIGNED_JSON = "/vol/tensusers5/bgroenhof/wav2vec2_chorec_run/wav2vec2build/output"
WINDOWS_BASE_DIR_UNALIGNED_JSON = get_abs_folder_path("output")

def get_base_dir_for_generalised_path_unaligned_json():
    if is_linux():
        return LINUX_BASE_DIR_UNALIGNED_JSON
    
    print(WINDOWS_BASE_DIR_UNALIGNED_JSON)
    return f"{WINDOWS_BASE_DIR_UNALIGNED_JSON}"

