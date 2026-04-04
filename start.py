import customtkinter as ctk
import subprocess

app = ctk.CTk()
app.grid_columnconfigure(0, weight=1)

label = ctk.CTkLabel(app, text="Install Llama 3 8B LLM? Will take 5GB+ space. (Required to run LocalAI)", font=ctk.CTkFont("Adwaita Mono", 25), wraplength=1150)
label.grid(row=0, column=0, pady=10, padx=20)

def install_button():
    subprocess.run(["chmod", "+x", "./install-llm.sh"])
    result = subprocess.run(["sudo", "./install-llm.sh"])

    if result.returncode == 0:
        app.destroy()
        subprocess.run(["python", "program.py"])
    else:
        print("Installation failed. Cannot continue.")

def abort_button():
    print("Cannot continue LocalAI installation. Aborted")
    exit(0)

button = ctk.CTkButton(app, text="Install (Look in terminal, will ask for sudo)", font=ctk.CTkFont("Adwaita Sans", 20), command=install_button)
button.grid(row=1, column=0, padx=30, pady=20)

button_abort = ctk.CTkButton(app, text="Cancel", font=ctk.CTkFont("Adwaita Sans", 20), command=abort_button)
button_abort.grid(row=2, column=0, padx=30, pady=5)

label_note = ctk.CTkLabel(app, text="Note that by pressing install, you acknowledge that installation can take up to 5GB of space and internet bandwith.", font=ctk.CTkFont("Adwaita Mono", 20), wraplength=1150)
label_note.grid(row=3, column=0, padx=10, pady=10)

app.geometry("1200x500")
app.title("LocalAI LLM installer")
app.mainloop()