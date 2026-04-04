import customtkinter as ctk
import os
import subprocess
import time

app = ctk.CTk()
app.grid_columnconfigure(0, weight=1)


label = ctk.CTkLabel(app, text="Test", font=ctk.CTkFont("Arial", 20))
label.grid(row=0, column=0, padx=10, pady=10)

app.geometry("500x500")
app.title("Test")
app.mainloop()