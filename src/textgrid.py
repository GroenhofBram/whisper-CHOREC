
import tgt
import pandas as pd

from src.file_path import get_file_path

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



def load_text_grid_as_df(tgt_file_path):
    # Read TextGrid file
    tg = tgt.io.read_textgrid(tgt_file_path, encoding='utf-8', include_empty_intervals=False)

    # Convert TextGrid file to Formatted Table (= df with on each row one interval)
    table = tgt.io.export_to_table(tg, separator=',')
    formatted_table = [x.split(',') for x in table.split('\n')]
    if(len(formatted_table)) == 0:
        print(tgt_file_path)

    print("\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    print(formatted_table[0])
    print(formatted_table[1:])
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")

    tg_df = pd.DataFrame(formatted_table[1:], columns = formatted_table[0])
    tg_df = tg_df.drop(columns=['tier_type'])

    # Need to be equal length
    tg_df_orthography = tg_df[tg_df['tier_name'] == "orthography"]
    tg_df_prompt = tg_df[tg_df['tier_name'] == "words to be read"]
    print("\nDFs before ANY filtering (Check if orhotgraphy has dron for s01c002v1_1LGPseudo)")
    print("\tOrthography")
    print(tg_df_orthography)
    print("\tPrompt")
    print(tg_df_prompt)
    
    # Aligns words to be read with prthography layers
    tg_df_prompt = tg_df_prompt[tg_df_prompt['text'] != "<"]
    # tg_df_orthography = tg_df_orthography[~tg_df_orthography['text'].str.contains(r'^(\*\s*x\s*)+$')]
    # tg_df_orthography = tg_df_orthography[~tg_df_orthography['text'].str.contains(r'\*x')]
    # tg_df_orthography = tg_df_orthography[~tg_df_orthography['text'].str.contains(r'\*x \*x')]
    # tg_df_orthography = tg_df_orthography[~tg_df_orthography['text'].isin(['*x']) & (tg_df_orthography['text'] != '*x *x')]
    
    tg_df_orthography = tg_df_orthography[~tg_df_orthography['text'].str.match(r'^\*x$')]
    
    # Possible solution: If *x *x is found and reading strategy is not empty, replace it with reading strategy. Store reading strategy somewhere,
        # then combine the data frames and remove all rows that have that reading strategy (or others) matched exactly
    if tg_df_orthography['text'].str.contains(r'\*x \*x').any():
        print("Replacing empty orthographies")
        tg_df_orthography['text'] = tg_df_orthography['text'].str.replace(r'\*x \*x', '[EMPTY ORTHOGRAPHY]', regex=True)
    else:
        print("No empty orthographies found")
    
    # tg_df_orthography = tg_df_orthography[tg_df_orthography['text'].str.replace('\*x \*x', '[EMPTY ORTHOGRAPHY]', regex=True)]




    print("\n- - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    print("- - - - - - orthography_df - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    print(tg_df_orthography)
    print(len(tg_df_orthography))
    print("- - - - - - prompt_df - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    print(tg_df_prompt)
    print(len(tg_df_prompt))
    print("- - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    print("\nChecking if Lengths Match")
    print(f"Length of tg_df_orthography:{len(tg_df_orthography)}")
    print(f"Length of tg_df_orthography[text]:{len(tg_df_prompt['text'])}")
    if len(tg_df_orthography) != len(tg_df_prompt['text']):
        print("- - - tg_df_orthography - - - ")
        print(tg_df_orthography)
        print("--------------------------------")
        print("- - - tg_df_prompt['text'] - - - ")
        print(tg_df_prompt['text'])


    tgt_df_repr = tg_df_orthography.assign(prompt=list(tg_df_prompt['text']))
    tgt_df_repr = tgt_df_repr.reset_index()
    
    print("\n- - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    print("tgt_df_repr before dropping cols")
    print(tgt_df_repr)
    print("- - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    tgt_df_repr = tgt_df_repr.drop(columns=['tier_name', 'index'])
    tgt_df_repr = tgt_df_repr.rename(columns={"text": "orthography"})

    print("\n- - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
    print("tgt_df_repr after dropping/renaming cols")
    print(tgt_df_repr)
    print("- - - - - -  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")

    return tgt_df_repr