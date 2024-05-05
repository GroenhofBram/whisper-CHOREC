def clean_reading_error_column(input: str):
    if input == None or input.strip() == '':
        return "CORRECTLY_READ"
    return input