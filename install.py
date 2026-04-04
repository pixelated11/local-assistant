import time
import os 
import subprocess
import customtkinter as ctk 
app = ctk.CTk()
app.grid_columnconfigure(0, weight=1)

textbox = ctk.CTkTextbox(app)

label = ctk.CTkLabel(app, text="Install LLM for LocalAI? (Required to run LocalAI. Can take up to 5GB+ of space.)", font=ctk.CTkFont(family="Arial", size=17))
label.pack()
label.grid(row=0, column=0, padx=10, pady=15)


def install_button():
    subprocess.run(["chmod", "+x", "./install-llm.sh"])
    result = subprocess.run(["sudo", "./install-llm.sh"])

    # Both exit 0 cases (already installed OR just installed), redirect to program.py
    if result.returncode == 0:
        app.destroy()                         # Close this window
        subprocess.run(["python", "program.py"])
    else:
        print("Installation failed. Cannot continue.")

def abort_button():
    exit(1)

app.title("LocalAI LLM installer")
app.geometry("650x200")


button = ctk.CTkButton(app, text="Install (look at terminal, will ask for sudo.)", command=install_button, width=175, height=50)
button.grid(row=1, column=0, pady=10, padx=20)

button = ctk.CTkButton(app, text="Cancel", command=abort_button, width=175, height=50)
button.grid(row=2, column=0, pady=5, padx=20)

app.mainloop()