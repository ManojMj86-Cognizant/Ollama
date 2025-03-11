import requests
import json

# Initialize conversation history
conversation_history = []

# Max number of exchanges to keep track of (e.g., 5 recent exchanges)
max_context_size = 50

# System message for context
# system_message = "You are a professional assistant. Respond formally."

# Function to update and get the current prompt with the context
def get_prompt():
    context = " ".join([entry["content"] for entry in conversation_history[-max_context_size:]])
    return context
    # return f"{system_message} {context}"

# Function to send a request to the Llama API with streaming support
def send_request_to_llama(prompt):
    url = "http://localhost:11434/api/generate"  # Update API endpoint if needed
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "temperature": 0.8,
        "stream": True
    }

    try:
        with requests.post(url, headers=headers, data=json.dumps(payload), stream=True) as response:
            if response.status_code == 200:
                print("Assistant: ", end="", flush=True)  # Print assistant label without newline
                full_response = ""

                for line in response.iter_lines():
                    if line:
                        try:
                            json_line = json.loads(line.decode('utf-8'))
                            text_chunk = json_line["response"]
                            print(text_chunk, end="", flush=True)  # Stream text in real-time
                            full_response += text_chunk  # Collect full response
                        except json.JSONDecodeError as e:
                            print("\nError decoding JSON:", e)

                print("\n")  # Move to a new line after full response
                return full_response
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None

# Start conversation loop
def start_chat():
    print("Chat with Llama (Type 'exit' to stop)")

    while True:
        # Get user input
        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            print("Exiting chat. Goodbye!")
            break

        # Add user input to conversation history
        conversation_history.append({"role": "user", "content": user_input})

        # Get the current prompt with context
        prompt = get_prompt()

        # Get response from the model
        response = send_request_to_llama(prompt)

        if response:
            # Add assistant's response to conversation history
            conversation_history.append({"role": "assistant", "content": response})

# Run the chat function
if __name__ == "__main__":
    start_chat()