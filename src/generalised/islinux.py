from platform import system

def is_linux() -> bool:
    return system().lower() == "linux"