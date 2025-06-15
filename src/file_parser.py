import re

def remove_comments(code: str) -> str:
    """
    Removes both inline and block comments from C code.
    """
    # Remove block comments (/* */)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    # Remove inline comments (//)
    code = re.sub(r'//.*', '', code)
    return code

def parse_input_file(file_path: str) -> list:
    """
    Reads a .c or .h file, removes comments and whitespace,
    and returns a list of dictionaries with line number and code.
    
    Example output:
    [
        {"line_number": 12, "code": "int32_t Bootloader_MmcsdRaw_writeToOffset(...)"},
        ...
    ]
    """
    parsed_lines = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_code = f.read()

        cleaned_code = remove_comments(raw_code)
        lines = cleaned_code.split('\n')

        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()
            if stripped:  # Skip empty lines
                parsed_lines.append({
                    "line_number": idx,
                    "code": stripped
                })

        return parsed_lines

    except Exception as e:
        print(f"Error while parsing input file: {e}")
        return []
