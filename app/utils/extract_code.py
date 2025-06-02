import re

def extract_code_block(response_text: str) -> str | None:
    """
    Finds the first triple‐backtick‐wrapped section in response_text
    and returns just its inner content (without the backticks).
    If no code block is found, returns None.
    """
    pattern = r"```(?:\w+)?\n(.*?)```"
    match = re.search(pattern, response_text, re.DOTALL)
    return match.group(1).strip() if match else None
