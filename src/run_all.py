from src.wav2vec2chorec import main as wav2vec2chorec_main
from src.sctkrun import main as sctk_run_unaligned
from src.wav2vec2chorecjson import main as wav2vec2chorec_json
from src.filteredalignment import main as align_filtered
from src.sctk_run_aligned import main as sctk_run_aligned
from src.confusion_matrix import main as conf_mat


def main():
    wav2vec2chorec_main()
    sctk_run_unaligned()
    wav2vec2chorec_json()
    align_filtered()
    sctk_run_aligned()
    conf_mat()