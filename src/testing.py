# REMOVE AND ADD WHISPER/FASTER-WHISPER
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import torch
import re, platform
import pandas as pd
from src.file_path import get_file_path
from src.textgrid import use_text_grids
from src.constants import WHISPER_MODEL_NAME
from src.cuda import DEVICE
from faster_whisper import WhisperModel
import re

# import whisperx
import gc

def main():
    # run_whisper_v3()
    #   run_whisperx()
    run_faster_whisper(vad = True)

def run_faster_whisper(vad: bool):
    model_size = "large-v2"
    transcription_dict = {"text": ""}

    # Run on GPU with "float16", CPU "int8"
    model = WhisperModel(model_size, device=DEVICE, compute_type="int8")

    if vad:
        segments, info = model.transcribe("files//test_glob//S03C010M1_1LG.wav", beam_size=5, language = "nl", vad_filter=True)
    elif vad == False:
        segments, info = model.transcribe("files//test_glob//S03C010M1_1LG.wav", beam_size=5, language = "nl")


    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        transcription_dict["text"] += segment.text
    
    if vad == False:
        transcription_dict["text"] = re.sub(r'(?<!\.)\s(?!\.)', '', transcription_dict["text"])
        transcription_dict["text"] = transcription_dict["text"].replace(".", "")
    
    # segments = list(segments)

    print("\n - - - - - - Full transcription - - - - - - -\n")
    print(transcription_dict)
    print("\n--------------------------------------\n")

def run_whisperx():
    audio_file = "files//test_glob//S03C010M1_1LG.wav"
    device = DEVICE
    batch_size = 16 
    compute_type = "int8"

    model = whisperx.load_model("large-v2", device, compute_type=compute_type)


    # Save model
    model_dir = "src//models//models_loaded"
    model = whisperx.load_model("large-v2", device, compute_type=compute_type, download_root=model_dir)


    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size, language="nl")
    
    print("\n### BEFORE ALIGNMENT ###\n")
    print(result["segments"])
    print("\n#############\n")

    # Alignment
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
    
    print("\n### AFTER ALIGNMENT ###\n")
    print(result["segments"])
    print("\n#############\n")


def run_whisper_v3():
    file_path = "files//test_glob//S03C010M1_1LG.wav"


    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model_id = WHISPER_MODEL_NAME

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True)
    model.to(DEVICE)

    processor = AutoProcessor.from_pretrained(model_id)
    
    # may need to take this out 
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        return_timestamps=True,
        torch_dtype=torch_dtype,
        device=DEVICE,
    )

    result = pipe(file_path, generate_kwargs={"language": "dutch"})
    print("- - - - - - - - - RESULT\n")
    print(result)
    print("- - - - - - - - - RESULT\n")

    ASR_transcription = re.sub(r'\s+', "", result['text'])
    


    print("- - - - - - - - - JUST TEXT\n")
    print(ASR_transcription)
    print("- - - - - - - - - JUST TEXT\n")

    # output = pipe(file_path, chunk_length_s=10, stride_length_s=(4, 2))

    # ASR_transcription = re.sub(r'\s+', ' ', output['text'])
    
    # # print(output)
    # # print(ASR_transcription)

    # return ASR_transcription

