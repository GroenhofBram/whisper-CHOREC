from pandas import DataFrame

def column_to_list(df: DataFrame, col_name: str):
    return df[col_name].tolist()