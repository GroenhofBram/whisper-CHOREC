from transformers import pipeline
import re, os, tgt, torch, pandas as pd

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def main():
    ASR_transcription = run_wav2vec2()
    tgt_df_repr = use_text_grids()
    sctk_align(ASR_transcription, tgt_df_repr)

def run_wav2vec2():
    # CHOREC: Tier 2 = prompts, Tier 3 = orthographic transcription
    file_path = 'D:\\repos\\wav2vec-CHOREC\\files\\S01C002V1_2LG.wav' # os.path.join(__file__, "..", "files\\S01C002V1_2LG.wav")
    model_name="GroNLP/wav2vec2-dutch-large-ft-cgn"
    pipe = pipeline(model=model_name)

    # Chunk length = windows (?)
    # Stides = context for each window for better inference (?)
    output = pipe(file_path, chunk_length_s=10, stride_length_s=(4, 2))

    ASR_transcription = re.sub(r'\s+', ' ', output['text'])
    print(output)
    print(ASR_transcription)

    return ASR_transcription

def use_text_grids():
    tg_file = "D:\\repos\\wav2vec-CHOREC\\files\\S01C002V1_2LG_f01.TextGrid"

    # Read TextGrid file
    tg = tgt.io.read_textgrid(tg_file, encoding='utf-8', include_empty_intervals=False)


    # Convert TextGrid file to Formatted Table (= df with on each row one interval)
    table = tgt.io.export_to_table(tg,
    separator=',')
    formatted_table = [x.split(',')
    for x in table.split('\n')]

    for idx, item in enumerate(formatted_table):
        if(len(item) == 6):
            print(idx, item)


    tg_df = pd.DataFrame(formatted_table[1:], columns = formatted_table[0])
    tg_df = tg_df.drop(columns=['tier_type'])

    tg_df_orthography = tg_df[tg_df['tier_name'] == "orthography"]
    tg_df_prompt = tg_df[tg_df['tier_name'] == "words to be read"]

    # print(tg_df_orthography)
    # print(tg_df_prompt)
    tgt_df_repr = tg_df_orthography.assign(prompt=list(tg_df_prompt['text']))

    tgt_df_repr = tgt_df_repr.reset_index()
    tgt_df_repr = tgt_df_repr.drop(columns=['tier_name', 'index'])
    tgt_df_repr = tgt_df_repr.rename(columns={"text": "orthography"})
    print(tgt_df_repr)

    return tgt_df_repr

def sctk_align(ASR_transcription, tgt_df_repr):
    
    # # # # HYPOTHESIS
    d = {'utterance_id': ['S01C001M1_1LG-words' ] ,
        'transcript': [ASR_transcription.lower()]}
    df = pd.DataFrame(data=d)
    df.to_csv('output/hyp.csv', index=False)

    # # # # REFERENCE
    d = {'utterance_id': ['S01C001M1_1LG-words'],
        'transcript': [" ".join(tgt_df_repr.orthography.values)]} # Or prompt: " ".join(tgt_df_repr.prompt.values)
    df = pd.DataFrame(data=d)
    df.to_csv('output/ref.csv', index=False)

    # For overview of what each argument does see:
    ## !./sctk score --help
    
    # !version=v0.3.0 && wget -q -O sctk https://github.com/shahruk10/go-sctk/releases/download/${version}/sctk && chmod +x ./sctk
    # !./sctk score \
    # --ignore-first=true \
    # --delimiter="," \
    # --col-id=0 \
    # --col-trn=1 \
    # --cer=false \
    # --out=./report \
    # --ref=./ref.csv \
    # --hyp=./hyp.csv \