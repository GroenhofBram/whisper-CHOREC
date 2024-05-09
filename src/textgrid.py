
import tgt
import pandas as pd


def lambda_fn(f) -> str:
    print(f)
    return f

def use_text_grids(tgt_file_name):
    print(tgt_file_name)
    # tg_file = get_file_path(tgt_file_name)
    tg_file = tgt_file_name

    # Read TextGrid file
    tg = tgt.io.read_textgrid(tg_file, encoding='utf-8', include_empty_intervals=False)

    # Convert TextGrid file to Formatted Table (= df with on each row one interval)
    table = tgt.io.export_to_table(tg, separator=',')
    formatted_table = [x.split(',') for x in table.split('\n')]

    tg_df = pd.DataFrame(formatted_table[1:], columns = formatted_table[0])

    tg_df_prompts = tg_df[tg_df['tier_name'] == 'words to be read']
    tg_df_reading_errs = tg_df[tg_df['tier_name'] == 'reading errors']
    tg_df_prompts['reading_errs'] = None

    # for all rows of tg_df_prompts:
    # Use current row and go through all rows tg_df_reading_errs
    # If the "start_time" of the current tg_df_prompts row as the current tg_df_reading_errs row, take the value in "text" from tg_df_reading_errs,
        # and add that to the current row of tg_df_prompts
    for index, prompt_row in tg_df_prompts.iterrows():
        for _, error_row in tg_df_reading_errs.iterrows():
            if prompt_row['start_time'] == error_row['start_time']:
                tg_df_prompts.at[index, 'reading_errs'] = error_row['text']
                break  # Break inner loop when matched
    
    tg_df_prompts['reading_errs'] = tg_df_prompts['reading_errs'].fillna('CORRECTLY_READ')
    print(tg_df_prompts)

    tg_df_prompts = tg_df_prompts[tg_df_prompts['text'] != "<"]
    tg_df_prompts = tg_df_prompts[tg_df_prompts['text'] != "<<"]
    tg_df_prompts = tg_df_prompts[tg_df_prompts['text'] != "<<<"]
    tg_df_prompts = tg_df_prompts[tg_df_prompts['text'] != "<<<<"]
    tgt_df_repr = tg_df_prompts.reset_index()
    tgt_df_repr = tgt_df_repr.drop(columns=['index', 'tier_type', 'tier_name', 'start_time', 'text'])
    tgt_df_repr = tgt_df_repr.rename(columns={"reading_errs": "orthography"})

    # breakpoint()

    return tgt_df_repr
