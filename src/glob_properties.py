from pathlib import Path

from src.models.participantfile import ParticipantFile

def create_participant_file(full_file_path: str, input: str):
    file_path_from_base = full_file_path.replace(input, "")
    pts = Path(file_path_from_base).parts
    file_name = str(pts[1])
    arr = file_name.replace(".wav", "").split("_")
    print(f"\npts: {pts}")
    print(f"arr: {arr}")

    session_name = arr[-2]
    print(session_name)
    participant_id = arr[-2]
    print(participant_id)
    file_name = pts[-1]
    print(file_name)


    return ParticipantFile(
        full_file_path=full_file_path,
        session_name=session_name,
        participant_id=participant_id,
        file_name=file_name,
    )

def generate_file_properties(files_glob: list[str], base_dir: str) -> list[ParticipantFile]:
    participant_files: map[ParticipantFile] = map(lambda file_path: create_participant_file(file_path, base_dir), files_glob)
    # print(list(f_repl)[-1])
    return list(participant_files)