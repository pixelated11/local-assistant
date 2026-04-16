import customtkinter as ctk
import subprocess
import sys
import os

MODELS = {
    "Qwen3 4B": "qwen3:4b",
    "Llama 3 8B": "llama3:8b",
    "Llama 3.2 3B": "llama3.2:3b"
}

def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

def check_ollama():
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        for model_tag in MODELS.values():
            if model_tag in result.stdout:
                subprocess.run(["python", resource_path("program.py")])
                sys.exit(0)
    except FileNotFoundError:
        pass

check_ollama()

app = ctk.CTk()
app.grid_columnconfigure(0, weight=1)

label = ctk.CTkLabel(app, text="Install LLM? Will take 5GB+ space. (Required to run LocalAssistant)", font=ctk.CTkFont("Adwaita Mono", 25), wraplength=1150)
label.grid(row=0, column=0, pady=10, padx=20)

label_model = ctk.CTkLabel(app, text="Select your LLM:", font=ctk.CTkFont("Adwaita Mono", 18))
label_model.grid(row=1, column=0, pady=5, padx=20)

model_selector = ctk.CTkOptionMenu(app, values=list(MODELS.keys()), font=ctk.CTkFont("Adwaita Mono", 15))
model_selector.grid(row=2, column=0, pady=5, padx=20)

def install_button():
    selected_model = MODELS[model_selector.get()]

    if sys.platform == "win32":
        script_path = resource_path("install-llm.ps1")
        result = subprocess.run([
            "powershell", "-ExecutionPolicy", "Bypass", "-File", script_path, "-Model", selected_model
        ])
    else:
        script_path = resource_path("install-llm.sh")
        subprocess.run(["chmod", "+x", script_path])
        result = subprocess.run(["sudo", script_path, selected_model])

    if result.returncode == 0:
        app.destroy()
        subprocess.run(["python", resource_path("program.py"), selected_model])
    else:
        print("Installation failed. Cannot continue.")

def abort_button():
    print("Cannot continue LocalAssistant installation. Aborted")
    sys.exit(0)

button = ctk.CTkButton(app, text="Install (Will ask for admin)", font=ctk.CTkFont("Adwaita Sans", 20), command=install_button)
button.grid(row=3, column=0, padx=30, pady=20)

button_abort = ctk.CTkButton(app, text="Cancel", font=ctk.CTkFont("Adwaita Sans", 20), command=abort_button)
button_abort.grid(row=4, column=0, padx=30, pady=5)

label_note = ctk.CTkLabel(app, text="Note that by pressing install, you acknowledge that installation can take up to 5GB of space and internet bandwidth.", font=ctk.CTkFont("Adwaita Mono", 20), wraplength=1150)
label_note.grid(row=5, column=0, padx=10, pady=10)

app.geometry("1200x500")
app.title("LocalAssistant Installer")
app.mainloop()