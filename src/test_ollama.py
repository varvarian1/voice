from llm.ollama_client import OllamaClient

def main():
    client = OllamaClient()

    text = "Погода в Москве"

    response = client.ask(text)
    print(f"Answer: {response}")

if __name__ == "__main__":
    main()