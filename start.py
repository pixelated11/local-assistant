import customtkinter as ctk
import subprocess
import sys
import os

# Get the correct path for bundled files when using PyInstaller
def resource_path(filename):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

app = ctk.CTk()
app.grid_columnconfigure(0, weight=1)

label = ctk.CTkLabel(app, text="Install Qwen3 4B LLM? Will take 5GB+ space. (Required to run LocalAssistant)", font=ctk.CTkFont("Monospace", 25), wraplength=1150)
label.grid(row=0, column=0, pady=10, padx=20)

def install_button():
    if sys.platform == "win32":
        script_path = resource_path("install-llm.ps1")
        result = subprocess.run([
            "powershell", "-ExecutionPolicy", "Bypass", "-File", script_path
        ])
    if result.returncode == 0:
        app.destroy()
        subprocess.run(["python", resource_path("program.py")])
    else:
        print("Installation failed. Cannot continue.")

def abort_button():
    print("Cannot continue LocalAssistant installation. Aborted")
    sys.exit(0)

button = ctk.CTkButton(app, text="Install (PowerShell Window will pop up, requesting admin privileges.)", font=ctk.CTkFont("Calibri", 20), command=install_button)
button.grid(row=1, column=0, padx=30, pady=20)

button_abort = ctk.CTkButton(app, text="Cancel", font=ctk.CTkFont("Calibri", 20), command=abort_button)
button_abort.grid(row=2, column=0, padx=30, pady=5)

label_note = ctk.CTkLabel(app, text="Note that by pressing install, you acknowledge that installation can take up to 5GB of space and internet bandwidth.", font=ctk.CTkFont("Adwaita Mono", 20), wraplength=1150)
label_note.grid(row=3, column=0, padx=10, pady=10)

app.geometry("1200x500")
app.title("LocalAssistant Installer")
app.mainloop()