from ollama import Client

client = Client(host='http://localhost:11434')
conversation_history = []
max_context_size = 50

def get_prompt():
    system_message = "You are a professional assistant. Respond formally."
    prompt = f"{system_message}\n"
    for entry in conversation_history[-max_context_size:]:
        if entry["role"] == "user":
            prompt += f"User: {entry['content']}\n"
        elif entry["role"] == "assistant":
            prompt += f"Assistant: {entry['content']}\n"
    return prompt

def send_request_to_llama(prompt):
    try:
        response = client.generate(
            model='llama3.2',
            prompt=prompt,
            stream=True,
            options={'temperature': 1}
        )
        full_response = ""
        print("Assistant: ", end="", flush=True)
        for part in response:
            text_chunk = part['response']
            print(text_chunk, end="", flush=True)
            full_response += text_chunk
        print("\n")
        return full_response
    except Exception as e:
        print(f"Error: {e}")
        return None

def start_chat():
    print("Chat with Llama (Type 'exit' to stop)")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            print("Exiting chat. Goodbye!")
            break
        conversation_history.append({"role": "user", "content": user_input})
        prompt = get_prompt()
        response = send_request_to_llama(prompt)
        if response:
            conversation_history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    start_chat()