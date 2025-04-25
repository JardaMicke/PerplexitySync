import requests

def generate_code(prompt, model='codellama:7b', stream=True, api_url='http://localhost:11434/api/generate'):
    payload = {
        'model': model,
        'prompt': prompt,
        'stream': stream
    }
    with requests.post(api_url, json=payload, stream=stream) as resp:
        resp.raise_for_status()
        if stream:
            for line in resp.iter_lines():
                if line:
                    yield line.decode('utf-8')
        else:
            yield resp.json()['response']
