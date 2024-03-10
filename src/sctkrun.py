from src.sctk import run_sctk
from src.islinux import check_linux_or_error

def main():
    check_linux_or_error()
    run_sctk(
        output_folder="/vol/tensusers5/bgroenhof/wav2vec2_chorec_run/wav2vec2build/report/unaligned",
        ref_csv_path="/vol/tensusers5/bgroenhof/wav2vec2_chorec_run/wav2vec2build/output/ref.csv",
        hyp_csv_path="/vol/tensusers5/bgroenhof/wav2vec2_chorec_run/wav2vec2build/output/hyp.csv"
    )

