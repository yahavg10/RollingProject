from typing import NoReturn, Callable, Any


def load_binary_files(files, load_method: Callable[[str, str], Any]) -> NoReturn:
    for filename, content in files:
        load_method(filename, content)
