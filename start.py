import customtkinter as ctk
import os
import subprocess
import threading
import ollama
from markdown_it import MarkdownIt
from tkinterweb import HtmlFrame

md = MarkdownIt()

app = ctk.CTk()
app.grid_columnconfigure(0, weight=1)

label_title = ctk.CTkLabel(app, text="LocalAI", font=ctk.CTkFont("Adwaita Sans", 35))
label_title.grid(row=0, column=0, padx=10, pady=10)

label_title_desc = ctk.CTkLabel(app, text="Your local AI application, powered with Llama 3-8B LLM.", font=ctk.CTkFont("Adwaita Mono", 15))
label_title_desc.grid(row=1, column=0, padx=35, pady=3)

label_response = ctk.CTkLabel(app, text="AI's Response: ", font=ctk.CTkFont("Adwaita Sans", 12))
label_response.grid(row=2, column=0, pady=5, padx=10)

response_frame = HtmlFrame(app, horizontal_scrollbar="auto")
response_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
app.grid_rowconfigure(3, weight=1)

def display_response(markdown_text):
    html = f"""
    <html><body style="font-family: sans-serif; font-size: 14px; padding: 10px; background-color: #2b2b2b; color: white;">
    {md.render(markdown_text)}
    </body></html>
    """
    response_frame.load_html(html)

prompt_box = ctk.CTkTextbox(app, height=80, font=ctk.CTkFont(size=14), wrap="word")
prompt_box.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

def send_prompt():
    prompt = prompt_box.get("0.0", "end").strip()
    if not prompt:
        return

    button_send.configure(state="disabled", text="Thinking...")
    label_status.configure(text="● AI Status: Thinking...")

    def run():
        response = ollama.chat(
            model="llama3:8b",
            messages=[{"role": "user", "content": prompt}]
        )
        answer = response["message"]["content"]
        app.after(0, lambda: display_response(answer))
        app.after(0, lambda: button_send.configure(state="normal", text="Send"))
        app.after(0, lambda: label_status.configure(text="● AI Status: Idle"))

    threading.Thread(target=run, daemon=True).start()

button_send = ctk.CTkButton(app, text="Send", command=send_prompt, font=ctk.CTkFont("Adwaita Mono", 15), height=45)
button_send.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

label_status = ctk.CTkLabel(app, text="● AI Status: Idle", font=ctk.CTkFont("Adwaita Mono", 13))
label_status.grid(row=6, column=0, padx=10, pady=5)

def stop_ai():
    subprocess.run(["ollama", "stop", "llama3:8b"])
    label_status.configure(text="● AI Status: Stopped")

button_stop = ctk.CTkButton(app, text="Stop AI (If you don't, it will run in the background, and consume RAM.)", command=stop_ai, font=ctk.CTkFont("Adwaita Mono", 15))
button_stop.grid(row=7, column=0, padx=10, pady=3)

app.attributes("-zoomed", True)
app.title("LocalAI")
app.mainloop()