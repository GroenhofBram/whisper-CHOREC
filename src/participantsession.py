from os.path import dirname, join
from glob import glob
from glob_properties import create_participant_file

from src.models.participantfile import ParticipantFile
from src.models.participant_session import ParticipantSession


def get_textgrid_files_matching_wav(wav_participant_file: ParticipantFile, participant_audio_id: str):
    dir_name = dirname(wav_participant_file.full_file_path)
    glob_path = join(dir_name, f"{participant_audio_id}_f01.TextGrid")
    globs = glob(glob_path)
    #print(globs)
    return globs

def get_participant_sessions_with_textgrids(
    wav_files: list[ParticipantFile],
    glob_search_base_dir: str,
):
    participant_sessions: list[ParticipantSession] = []
    for wav_participant_file in wav_files:
        ## todo: find relevant participant sessio
        participant_audio_id = wav_participant_file.wav_participant_full()
        matching_textgrid_globs = get_textgrid_files_matching_wav(wav_participant_file=wav_participant_file, participant_audio_id=participant_audio_id)
        
        if len(matching_textgrid_globs) == 0:
            continue
        elif len(matching_textgrid_globs) == 1:
            textgrid_file = create_participant_file(matching_textgrid_globs[0], glob_search_base_dir)
            
            p_sesh = ParticipantSession(
                wav_participant_file=wav_participant_file,
                textgrid_participant_file=textgrid_file,
                participant_audio_id=participant_audio_id
            )
            participant_sessions.append(p_sesh)
        else:
            continue
    return participant_sessions
