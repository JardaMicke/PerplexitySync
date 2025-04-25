import re
from typing import List, Dict

def parse_artifacts(text: str) -> List[Dict]:
    """
    Parsuje artefakty ve formátu [FILE:OPERATION:FILENAME]
    """
    artifact_pattern = r"\[FILE:(?P<operation>CREATE|UPDATE):(?P<filename>[^\]]+)\]"
    matches = re.finditer(artifact_pattern, text)
    return [
        {"operation": m.group("operation"), "filename": m.group("filename")}
        for m in matches
    ]
