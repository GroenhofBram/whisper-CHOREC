import subprocess
import platform

def main():
    py_files = get_python_files()
    run_py_files(py_files)


def get_python_files():
    # python_files = [
    #     "wav2vec2chorec.py",
    #     "sctkrun.py",
    #     "wav2vec2chorecjson.py",
    #     "filteredalignment.py",
    #     "sctkrun_aligned.py"
    # ]

    python_files = ["test1.py","test2.py"]
    return(python_files)

def run_py_files(py_files):
    for file in py_files:
        subprocess.run(["python", file])


main()