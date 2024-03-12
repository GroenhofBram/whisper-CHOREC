############### ONLY GRAB FILES THAT CONTAIN "LG", AVI and others cause issues


import tgt
import pandas as pd

tg_file = 'D:\\repos\\wav2vec-CHOREC\\files\\test_glob\\S01\\S01C003V1\\S01C003V1_1LG_f01.TextGrid'
 

# Read TextGrid file
tg = tgt.io.read_textgrid(tg_file, encoding='utf-8', include_empty_intervals=False)


table = tgt.io.export_to_table(tg,
separator=',')
formatted_table = [x.split(',')
for x in table.split('\n')]

# for idx, item in enumerate(formatted_table):
# 	if(len(item) == 6):
# 		print(idx, item)


tg_df = pd.DataFrame(formatted_table[1:], columns = formatted_table[0])
tg_df_prompts = tg_df[tg_df['tier_name'] == 'words to be read']
tg_df_prompts = tg_df_prompts[tg_df_prompts['text'] != "<"]
tg_df_prompts = tg_df_prompts[tg_df_prompts['text'] != "<<"]
tg_df_prompts = tg_df_prompts[tg_df_prompts['text'] != "<<<"]
tg_df_prompts = tg_df_prompts[tg_df_prompts['text'] != "<<<<"]
tg_df_orthography = tg_df[tg_df['tier_name'] == 'orthography']

# print(len(tg_df_orthography))

filtered_df_orthography = tg_df_orthography[tg_df_orthography['start_time'].isin(tg_df_prompts['start_time'])]
missing_start_times = tg_df_prompts[~tg_df_prompts['start_time'].isin(filtered_df_orthography['start_time'])]

# If there are missing start_times, append them to filtered_df_orthography
if not missing_start_times.empty:
	missing_start_times['text'] = "[ORTHOGRAPHY MISSING]"
	filtered_df_orthography = pd.concat([filtered_df_orthography, missing_start_times], ignore_index=True)



# print(tg_df_orthography['text'])

print("\nOrthography")

print(filtered_df_orthography['text'])

print("\nPrompts")

print(tg_df_prompts['text'])

print(len(tg_df_orthography))
print("AFter filter (should be equal)")
print(len(filtered_df_orthography))
print(len(tg_df_prompts))

print(tg_df_prompts)
print(filtered_df_orthography)

