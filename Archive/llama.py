import requests  # Import the requests library for making API calls
import json  # Import JSON for parsing API responses

# Define the API endpoint for Ollama
url = "http://localhost:11434/api/generate"

# Define the request payload with the model name, prompt, and streaming enabled
data = {
    "model": "llama3.2",  # Specify the model to use
    "prompt": "What is Artificial Inteligience",  # Input prompt  (This could be converted to user Input.)
    "system": "You are a knowledgeable and professional assistant. Your responses should be clear, concise, and formal.",  # Professional tone
    "temperature": 0.9,  # Lower temperature for a more deterministic and formal response
    "stream": True  # Enable streaming for real-time output
}

# Send the request to Ollama with streaming enabled
response = requests.post(url, json=data, stream=True)

# Print header for the output
print("Response (Streaming):\n")

# Process the response line by line as it streams
for line in response.iter_lines():
    if line:  # Ensure the line is not empty
        try:
            # Decode the JSON response line
            json_line = line.decode("utf-8")
            parsed_json = json.loads(json_line)

            # Extract and print the response text
            if "response" in parsed_json:
                print(parsed_json["response"], end="", flush=True)  # Print text without newlines for smooth streaming

        except json.JSONDecodeError:
            # Handle cases where the JSON response is malformed
            print("\n[JSON Decode Error] Skipping malformed data.")
