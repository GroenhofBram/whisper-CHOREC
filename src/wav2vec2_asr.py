from transformers import pipeline
from faster_whisper import WhisperModel
import re
from re import sub as regex_sub
from transformers import pipeline
from islinux import is_linux

from constants import WAV2VEC2_MODEL_NAME
from models.participantfile import ParticipantFile
from cuda import DEVICE

def wav2vec2_asr(input_participant_wav_file: ParticipantFile) -> str:
    # CHOREC: Tier 2 = prompts, Tier 3 = orthographic transcription
    file_path = input_participant_wav_file.full_file_path
    # may need to take this out 
    pipe = pipeline(model=WAV2VEC2_MODEL_NAME, device=DEVICE)

    # Chunk length = windows (?)
    # Stides = context for each window for better inference (?)
    output = pipe(file_path, chunk_length_s=10, stride_length_s=(4, 2))

    ASR_transcription = regex_sub(r'\s+', ' ', output['text'])
    ASR_transcription = regex_sub(r'[?.!,]', '', ASR_transcription)

    return ASR_transcription

# Filter transcription output before returning
def whisper_asr(input_participant_wav_file: ParticipantFile) -> str:
    file_path = input_participant_wav_file.full_file_path

    model_size = "large-v2"
    transcription_dict = {"text": ""}
    compute_type = "float16" if is_linux() else "int8"

    # Run on GPU with "float16", CPU "int8"
    model = WhisperModel(model_size, device=DEVICE, compute_type=compute_type)

    # S01C014V1_1LG.wav
    segments, info = model.transcribe(file_path,
                                      beam_size=5,
                                      language = "nl")


    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        transcription_dict["text"] += segment.text 
    
    print("\n - - - - - - Full last SEGMENT - - - - - - -\n")
    print(segment)
    print("\n--------------------------------------\n")
    

    print("\n - - - - - - Full transcription - - - - - - -\n")
    print(transcription_dict)
    print("\n--------------------------------------\n")

    ASR_transcription = regex_sub(r'\s+', ' ', transcription_dict["text"])
    ASR_transcription = regex_sub(r'[?.!,]', '', ASR_transcription)

    return ASR_transcription


