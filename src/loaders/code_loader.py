import os

def loadCodeLines(filePath: str) -> list:
    """
    Loads code lines from a given C or header file.

    Args:
        filePath (str): Full path to the C (.c) or header (.h) file.

    Returns:
        List[Dict]: List of dictionaries with line number and code line.
    """
    if not os.path.exists(filePath):
        raise FileNotFoundError(f"❌ Code file not found: {filePath}")

    codeLines = []
    with open(filePath, 'r') as file:
        for idx, line in enumerate(file, start=1):
            cleanLine = line.rstrip()
            if cleanLine:  # skip empty lines
                codeLines.append({
                    "lineNumber": idx,
                    "codeLine": cleanLine
                })

    if not codeLines:
        raise ValueError(f"⚠️ No valid code lines found in file: {filePath}")

    return codeLines
