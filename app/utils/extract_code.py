import re

def extract_code_block(response_text):
    match = re.search(r"```(?:\w+)?\n(.*?)```", response_text, re.DOTALL)
    return match.group(1).strip() if match else None
