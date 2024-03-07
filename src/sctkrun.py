import subprocess, platform

linux_path = "/vol/tensusers5/bgroenhof/wav2vec2_chorec_run/sctk_run/sctk"

def main():
    check_executable()
    run_sctk(
        output_folder="/vol/tensusers5/bgroenhof/wav2vec2_chorec_run/wav2vec2build/report/unaligned",
        ref_csv_path="/vol/tensusers5/bgroenhof/wav2vec2_chorec_run/wav2vec2build/output/ref.csv",
        hyp_csv_path="/vol/tensusers5/bgroenhof/wav2vec2_chorec_run/wav2vec2build/output/hyp.csv"
    )

def check_executable():
    if platform.system().lower() != "linux":
        raise ValueError("NOT LINUX")

def run_sctk(output_folder, ref_csv_path, hyp_csv_path):
    args = [
        "sctk", 
        "score",
        "--ignore-first=true",
        "--delimiter=,",
        "--col-id=0",
        "--col-trn=1",
        "--cer=false",
        f"--out={output_folder}",
        f"--ref={ref_csv_path}",
        f"--hyp={hyp_csv_path}"
    ]

    try:
        return subprocess.run(args, executable=linux_path, check=True)
    except Exception as e:
        print(e)
