from json import load

def load_json_file(file_path: str) -> dict:
    with open(file_path, "r") as fp:
        return load(fp)

SPEAKERS = 'speakers'
WORDS = 'words'

def extract_words_from_json(json_data: dict, session_speaker_id: str) -> dict:
    key = session_speaker_id
    words_session_key = f"({session_speaker_id}-{WORDS})"
    words_key = WORDS
    return json_data['speakers'][key][words_session_key][words_key]