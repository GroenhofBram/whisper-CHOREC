
import tgt
import pandas as pd

def use_text_grids(tgt_file_name):
    tg_file = get_file_path(tgt_file_name)

    # Read TextGrid file
    tg = tgt.io.read_textgrid(tg_file, encoding='utf-8', include_empty_intervals=False)


    # Convert TextGrid file to Formatted Table (= df with on each row one interval)
    table = tgt.io.export_to_table(tg, separator=',')
    formatted_table = [x.split(',')
    for x in table.split('\n')]

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

    return tgt_df_repr