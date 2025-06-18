import os

def loadCodeLines(filePath: str) -> list:
    """
    Reads a C or header file and returns its content line by line.

    Args:
        filePath (str): Path to the .c or .h input file.

    Returns:
        List[Dict]: Each dict contains 'lineNumber' and 'codeLine'.
    """
    if not os.path.isfile(filePath):
        raise FileNotFoundError(f"❌ Input file not found: {filePath}")

    codeLines = []
    with open(filePath, 'r') as f:
        for idx, line in enumerate(f, start=1):
            cleanedLine = line.strip()
            if cleanedLine:  # Skip empty lines
                codeLines.append({
                    "lineNumber": idx,
                    "codeLine": cleanedLine
                })

    return codeLines
