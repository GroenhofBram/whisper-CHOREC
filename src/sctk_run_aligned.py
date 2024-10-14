from sctk import run_sctk
from islinux import check_linux_or_error

def main():
    check_linux_or_error()
    run_sctk(
        output_folder="/vol/tensusers5/bgroenhof/wav2vec2_chorec_run/wav2vec2build/report/aligned",
        ref_csv_path="/vol/tensusers5/bgroenhof/wav2vec2_chorec_run/wav2vec2build/output/ref_filtered.csv",
        hyp_csv_path="/vol/tensusers5/bgroenhof/wav2vec2_chorec_run/wav2vec2build/output/hyp_filtered.csv"
    )