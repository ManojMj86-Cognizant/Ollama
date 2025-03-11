# Ollama

This project allows you to chat with the Llama language model using a Python script. The script sends user inputs to the Llama API and streams the responses in real-time.

## Requirements

- Python 3.6 or higher
- `requests` library

You can install the `requests` library using pip:

```bash
pip install requests
```
### Usage

Clone the repository (if applicable) or download the script. 
Make sure the Ollama application is running in background

Update the API endpoint in the send_request_to_llama function if needed:

url = "http://localhost:11434/api/generate"
Run the script:

python llama_context.py
Start chatting:

Type your message and press Enter.
Type exit to stop the chat.
