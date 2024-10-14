from pathlib import Path

from models.participantfile import ParticipantFile

# def create_participant_file(full_file_path: str, input: str):
#     file_path_from_base = full_file_path.replace(input, "")
#     pts = Path(file_path_from_base).parts
#     file_name = str(pts[1])
#     arr = file_name.replace(".wav", "").split("_")
#     print(f"\npts: {pts}")
#     print(f"arr: {arr}")

#     session_name = arr[-2]
#     print(session_name)
#     participant_id = arr[-2]
#     print(participant_id)
#     file_name = pts[-1]
#     print(file_name)

def create_participant_file(full_file_path: str, input: str):
    file_path_from_base = full_file_path.replace(input, "")
    file_name = Path(file_path_from_base).name  # Get the file name part
    arr = file_name.replace(".wav", "").split("_")  # Split the file name

    print(f"\nfile_name: {file_name}")
    print(f"arr: {arr}")

    if len(arr) < 2:
        raise ValueError(f"\n\n\t!!!!!Filename does not conform to expected format: {file_name}!!!!!\n\n")

    session_name = arr[-2]
    participant_id = arr[-2]

    print(session_name)
    print(participant_id)
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