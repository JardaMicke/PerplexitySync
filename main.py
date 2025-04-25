from monitor.process_watcher import watch_perplexity_process
from monitor.chat_socket import start_chat_listener
from monitor.artifact_parser import parse_artifacts

def on_detect():
    print("Perplexity.exe detekován. Spouštím listener na chatové zprávy...")
    def on_message(text):
        print(f"Přijatá zpráva: {text}")
        artifacts = parse_artifacts(text)
        if artifacts:
            print(f"Detekované artefakty: {artifacts}")
    start_chat_listener(on_message)

if __name__ == "__main__":
    print("Sleduji běh procesu Perplexity...")
    watch_perplexity_process(on_detect)
