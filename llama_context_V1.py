from ollama import Client                       # Import the Ollama client library

client = Client(host='http://localhost:11434')  # Initialize the Ollama client, specifying the host URL
conversation_history = []                       # Initialize an empty list to store the conversation history
max_context_size = 50                           # Set the maximum number of conversation turns to keep in context

def get_prompt():
    """
    Constructs the prompt to send to the language model, including system message and conversation history.
    """
    system_message = "You are a professional assistant. Respond formally."              # Define the system message
    prompt = f"{system_message}\n"                                  
    for entry in conversation_history[-max_context_size:]:              # Iterate through the recent conversation history
        if entry["role"] == "user":                                     # If the entry is from the user
            prompt += f"User: {entry['content']}\n"                     # Add the user's message to the prompt
        elif entry["role"] == "assistant":                              # If the entry is from the assistant
            prompt += f"Assistant: {entry['content']}\n"                # Add the assistant's message to the prompt
    return prompt                                                       # Return the constructed prompt

def send_request_to_llama(prompt):
    """
    Sends a request to the Ollama API with the given prompt and streams the response.
    """
    try:
        response = client.generate(                                     # Send the request to Ollama using the client
            model='llama3.2',                                           # Specify the model to use
            prompt=prompt,                                              # Pass the constructed prompt
            stream=True,                                                # Enable streaming to receive responses in chunks
            options={'temperature': 0.8}                                # Set the temperature for response generation
        )
        full_response = ""                                              # Initialize an empty string to store the full response
        print("Assistant: ", end="", flush=True)                        # Print the assistant label without a newline
        for part in response:                                           # Iterate through the streamed response chunks
            text_chunk = part['response']                               # Extract the text chunk from the response
            print(text_chunk, end="", flush=True)                       # Print the text chunk without a newline
            full_response += text_chunk                                 # Append the text chunk to the full response
        print("\n")  
        return full_response                                            # Return the full response
    except Exception as e:                                              # Handle any exceptions that occur during the request
        print(f"Error: {e}")  
        return None                                                     # Return None to indicate an error

def start_chat():
    """
    Starts the interactive chat loop.
    """
    print("Chat with Llama (Type 'exit' to stop)")                      # Print a welcome message
    while True:                 
        user_input = input("\nYou: ")                                   # Get user input from the console
        if user_input.lower() == "exit":                                # Check if the user wants to exit
            print("Exiting chat. Goodbye!")  
            break                                                       # Exit the loop
        conversation_history.append({"role": "user", "content": user_input})    # Add the user's input to the history
        prompt = get_prompt()                                                   # Get the prompt with context
        response = send_request_to_llama(prompt)                                # Send the request to the model
        if response:                                                            # Check if a valid response was received
            conversation_history.append({"role": "assistant", "content": response})  # Add the assistant's response to the history

if __name__ == "__main__":
    start_chat()  