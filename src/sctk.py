


import subprocess

from islinux import is_linux

SCTK_LINUX_PATH = "/vol/tensusers5/bgroenhof/wav2vec2_chorec_run/sctk_run/sctk"

def run_sctk(output_folder, ref_csv_path, hyp_csv_path):
    if not is_linux():
        print("Can't run as not on linux")
        print(f"OUT: {output_folder}")
        print(f"REF: {ref_csv_path}")
        print(f"HYP: {hyp_csv_path}")

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
        return subprocess.run(args, executable=SCTK_LINUX_PATH, check=True)
    except Exception as e:
        print(e)
