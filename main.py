import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter import ttk  # Use ttk for custom styles
from langchain.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

# Define the prompt template
template = """
Answer the Question below.

Here is the conversation history : {context}

Question: {question}

Answer:
"""

# Model list to choose from
available_models = {
    "llama3:latest": "365c0bd3c000",
    "gemma2:9b": "ff02c3702f32",
    "llama2:latest": "78e26419b446"
}

# Function to handle the conversation logic
def handle_conversation(context, question, chain):
    result = chain.invoke({"context": context, "question": question})
    return result

# GUI Application
class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Chatbot")
        self.context = ""  # Conversation history

        # Set background color for the form
        self.root.config(bg="gray")

        # Create model selection dropdown
        self.selected_model = tk.StringVar(value="llama3:latest")  # Default model
        model_menu = tk.OptionMenu(root, self.selected_model, *available_models.keys())
        model_menu.grid(column=0, row=0, padx=10, pady=10, sticky='ew')

        # Create conversation window (light gray background)
        self.conversation_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, state='disabled', bg='lightgray')
        self.conversation_window.grid(column=0, row=1, padx=10, pady=10)

        # Define tags for different colors
        self.conversation_window.tag_config('user', foreground='blue')
        self.conversation_window.tag_config('ai', foreground='green')

        # Create multiline text box for user's question with black text and light gray background
        self.input_textbox = tk.Text(root, width=50, height=5, fg="black", bg="lightgray", wrap=tk.WORD)
        self.input_textbox.grid(column=0, row=2, padx=10, pady=10)

        # Bind Ctrl + Enter to the "Ask" button click (submit question)
        self.input_textbox.bind("<Control-Return>", lambda event: self.send_question())

        # Create a submit button
        self.submit_button = tk.Button(root, text="Ask", command=self.send_question)
        self.submit_button.grid(column=1, row=2, padx=10, pady=10)

    def send_question(self):
        # Get the text from the text box
        user_input = self.input_textbox.get("1.0", tk.END).strip()
        if user_input.lower() == "exit":
            self.root.quit()

        if user_input:
            # Get the selected model
            selected_model = self.selected_model.get()

            # Check if the model is available
            if selected_model not in available_models:
                messagebox.showerror("Model Error", f"The model '{selected_model}' is not available.")
                return

            # Instantiate the selected model and prompt
            model = OllamaLLM(model=selected_model)
            prompt = ChatPromptTemplate.from_template(template)
            chain = prompt | model

            # Update conversation window with user input (blue text)
            self.conversation_window.config(state='normal')
            self.conversation_window.insert(tk.END, f"User: {user_input}\n", 'user')
            self.conversation_window.config(state='disabled')

            # Get AI response
            response = handle_conversation(self.context, user_input, chain)

            # Update conversation window with AI response (green text)
            self.conversation_window.config(state='normal')
            self.conversation_window.insert(tk.END, f"AI: {response}\n\n", 'ai')
            self.conversation_window.config(state='disabled')

            # Update conversation context
            self.context += f"User: {user_input}\nAI: {response}\n"

            # Clear the input field (text box)
            self.input_textbox.delete("1.0", tk.END)

# Main entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
