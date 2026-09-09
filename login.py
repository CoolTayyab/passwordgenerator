import customtkinter as ctk

from auth import google_login



class LoginWindow:

    def __init__(self):

        self.window = ctk.CTk()

        self.window.title("Password Manager Login")

        self.window.geometry("420x300")

        self.window.resizable(False, False)

        self.build_ui()

    def build_ui(self):

        title = ctk.CTkLabel(
            self.window,
            text="🔐 Password Manager",
            font=("Segoe UI", 26, "bold")
        )

        title.pack(pady=(45, 15))

        subtitle = ctk.CTkLabel(
            self.window,
            text="Sign in to continue",
            font=("Segoe UI", 14)
        )

        subtitle.pack(pady=(0, 30))

        login_btn = ctk.CTkButton(
            self.window,
            text="Continue with Google",
            width=230,
            height=45,
            command=self.login
        )

        login_btn.pack()

    def login(self):

        google_login()

        self.window.destroy()

        from app import PasswordManagerApp

        app = PasswordManagerApp()

        app.run()
    def run(self):

        self.window.mainloop()
def show_login():

    login = LoginWindow()

    login.run()