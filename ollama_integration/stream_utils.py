import json

def extract_text_from_stream_line(line):
    try:
        data = json.loads(line)
        return data.get('response', '')
    except Exception:
        return ''
