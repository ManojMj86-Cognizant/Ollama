import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton,
)
from PySide6.QtCore import Qt, Signal, QObject, QThread
from ollama import Client
import UI_Enabled.styles as styles  # Import the styles module

# Ollama API setup
client = Client(host='http://localhost:11434')
conversation_history = []
max_context_size = 50

class OllamaWorker(QObject):
    """Worker thread for Ollama API calls."""
    chunk_received = Signal(str)
    error_occurred = Signal(str)

    def generate_response(self, prompt):
        try:
            response = client.generate(
                model='llama3.2',
                prompt=prompt,
                stream=True,
                options={'temperature': 0.8}
            )
            for part in response:
                text_chunk = part['response']
                self.chunk_received.emit(text_chunk)
        except Exception as e:
            self.error_occurred.emit(f"Error: {e}")

class OllamaChat(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.worker = OllamaWorker()  # Create worker in main thread
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)
        self.worker_thread.start()
        self.worker.chunk_received.connect(self.append_chunk)
        self.worker.error_occurred.connect(self.display_error)
        self.full_response = ""

    def append_chunk(self, chunk):
        if not self.full_response:
            self.text_area.insertPlainText("\nAssistant: ")
        self.text_area.insertPlainText(chunk)
        self.full_response += chunk
        if chunk.endswith('\n'):
            return
        elif len(chunk) > 0 and chunk[-1] in ['.', '!', '?']:
            self.text_area.insertPlainText('\n')

    def send_message(self):
        user_input = self.input_entry.text()
        if user_input:
            self.text_area.append(f"You: {user_input}")
            self.input_entry.clear()
            conversation_history.append({"role": "user", "content": user_input})
            prompt = self.get_prompt()
            self.full_response = ""
            self.worker_thread.quit()
            self.worker_thread.wait()
            self.worker_thread = QThread()
            self.worker.moveToThread(self.worker_thread)
            self.worker_thread.started.connect(lambda: self.worker.generate_response(prompt))  # Correct signal connection
            self.worker_thread.start()

    def display_error(self, error_message):
        self.text_area.append(error_message)

    def init_ui(self):
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet(styles.chat_text_edit_style)

        self.input_entry = QLineEdit(self)
        self.input_entry.setStyleSheet(styles.chat_line_edit_style)

        self.send_button = QPushButton("Send", self)
        self.send_button.setStyleSheet(styles.chat_push_button_style)
        self.send_button.clicked.connect(self.send_message)  # Connect the button to the send_message method

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_entry)
        input_layout.addWidget(self.send_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.text_area)
        main_layout.addLayout(input_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("Ollama Chat")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet(styles.chat_widget_style)

    def get_prompt(self):
        """Constructs the prompt with conversation history."""
        system_message = "You are a professional assistant Respond with conversation mode."
        prompt = f"{system_message}\n"
        for entry in conversation_history[-max_context_size:]:
            if entry["role"] == "user":
                prompt += f"User: {entry['content']}\n"
            elif entry["role"] == "assistant":
                prompt += f"Assistant: {entry['content']}\n"
        return prompt

if __name__ == "__main__":
    app = QApplication(sys.argv)
    chat_window = OllamaChat()
    chat_window.show()
    sys.exit(app.exec())