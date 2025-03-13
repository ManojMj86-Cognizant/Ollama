# Ollama

This project allows you to chat with the Llama language model using a Python script. The script sends user inputs to the Llama API and streams the responses in real-time.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/ManojMj86-Cognizant/Ollama.git
   

2. Create and activate the virtual environment: 
    ```bash
    python -m venv .venv
    # on Mac/ Linux use --- source .venv/bin/activate  
    .venv\Scripts\activate  # On Windows use 

3. Install Dependencies 
    ```bash 
    pip install -r requirements.txt

4. Open the project in VS Code and select the .venv interpreter.


## Usage

1. Chat with Llama --> 
    Run the script:
    ```
    python llama_context_V1.py
    ```
    
    Start chatting:
    Type your message and press Enter.
    Type exit to stop the chat.
2. For PDF extraction -->
    Keep the pdf file in documents folder. Keep the document name copied
    update the document path in the pdfreader.py file
    Run the script:
    ```
    python pdfreader.py
    ```

