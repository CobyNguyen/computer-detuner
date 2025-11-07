import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.geometry("400x240")
app.title("Computer Detuner")

label = customtkinter.CTkLabel(app, text="Welcome to Computer Detuner!", font=customtkinter.CTkFont(size=20, weight="bold"))
label.pack(pady=20)

app.mainloop()