import threading
import time
import requests
from auth import is_logged_in
from io import BytesIO
from PIL import Image
import customtkinter as ctk
from ui import HistoryFrame
from auth import get_user_info
from datetime import datetime
from utils import is_connected
from history import load_history, save_history_file
from utils import generate_random_password, copy_to_clipboard
from master_password import master_password_exists
from database import upload_history, download_history
class PasswordManagerApp:

    def __init__(self):

        self.app = ctk.CTk()
        self.app.title("Password Generator v2.0")
        self.app.geometry("700x600")
        self.app.resizable(True, True)
        self.password_hidden = False
        self.password_history = load_history()
        self.user = get_user_info()
        self.user_picture = self.user.get("picture", "")
        self.user_name = self.user.get("name", "Unknown User")
        self.user_email = self.user.get("email", "")
        self.last_sync_time = "Never"
        self.build_ui()
        if not is_logged_in():

            self.show_login()

        elif not master_password_exists():

            self.show_master(create=True)

        else:

            self.show_master(create=False)
        #threading.Thread(
            #target=self.auto_sync_loop,
            #daemon=True
        #).start()
        
    def build_ui(self):
        self.login_frame = ctk.CTkFrame(self.app)
        self.master_frame = ctk.CTkFrame(self.app)
        self.home_frame = ctk.CTkFrame(self.app)
        self.history_frame = ctk.CTkFrame(self.app)
        self.profile_frame = ctk.CTkFrame(self.app)
        self.build_profile_picture()
        self.build_title()
        self.build_slider()
        self.build_options()
        self.build_password_box()
        self.build_buttons()
        self.build_status()
        
    def hide_all_frames(self):

        self.login_frame.pack_forget()
        self.master_frame.pack_forget()
        self.home_frame.pack_forget()
        self.profile_frame.pack_forget()
        self.history_frame.pack_forget()
    def show_login(self):

        self.hide_all_frames()
        for widget in self.login_frame.winfo_children():
            widget.destroy()
        self.login_frame.pack(
            fill="both",
            expand=True
        )

        title = ctk.CTkLabel(
            self.login_frame,
            text="🔐 Password Manager",
            font=("Segoe UI", 28, "bold")
        )

        title.pack(pady=(80,20))

        login_btn = ctk.CTkButton(
            self.login_frame,
            text="Continue with Google",
            width=250,
            height=45,
            command=self.login_google
        )

        login_btn.pack(pady=20)

    def show_master(self, create=False):

        self.hide_all_frames()
        for widget in self.master_frame.winfo_children():
            widget.destroy()
        self.master_frame.pack(
            fill="both",
            expand=True
        )

        title = ctk.CTkLabel(
            self.master_frame,
            text="Create Master Password" if create else "Enter Master Password",
            font=("Segoe UI", 24, "bold")
        )

        title.pack(pady=(70, 25))

        self.master_entry = ctk.CTkEntry(
            self.master_frame,
            width=280,
            height=40,
            show="*"
        )

        self.master_entry.pack(pady=10)

        unlock_btn = ctk.CTkButton(
            self.master_frame,
            text="Save" if create else "Unlock",
            width=200,
            command=lambda: self.verify_master(create)
        )

        unlock_btn.pack(pady=20)

    def show_home(self):
        self.hide_all_frames()
        self.home_frame.pack(
            fill="both",
            expand=True
        )

    def show_history(self):
        self.hide_all_frames()

        self.history_frame.pack(
            fill="both",
            expand=True
        )

        history_ui = HistoryFrame(
            self.history_frame,
            self.password_history,
            self
        )

        history_ui.build()
    def verify_master(self, create=False):

        from master_password import (
            set_master_password,
            verify_master_password
        )

        password = self.master_entry.get()

        if create:

            set_master_password(password)

            self.show_home()

            return

        if verify_master_password(password):

            self.show_home()

        else:

            self.master_entry.delete(0, "end")
    def build_profile_picture(self):
        
        if not self.user_picture:
            return

        response = requests.get(self.user_picture)

        image = Image.open(BytesIO(response.content))

        image = image.resize((42, 42))

        self.profile_image = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=(42, 42)
        )

        self.profile_btn = ctk.CTkButton(
             self.home_frame,
            text="",
            image=self.profile_image,
                width=42,
                height=42,
            fg_color="transparent",
            hover_color="#3A3A3A",
            command=self.show_profile
        )

        self.profile_btn.place(
            relx=0.97,
            y=15,
            anchor="ne"
        )
    def show_profile(self):
        self.hide_all_frames()

        for widget in self.profile_frame.winfo_children():
            widget.destroy()

        self.profile_frame.pack(
            fill="both",
            expand=True
        )
        back_btn = ctk.CTkButton(
            self.profile_frame,
            text="← Back",
            width=120,
            command=self.show_home
        )

        back_btn.pack(
            anchor="nw",
            padx=15,
            pady=15
        )
        
        if self.profile_image:

            picture = ctk.CTkLabel(
                self.profile_frame,
                image=self.profile_image,
                text=""
        )

        picture.pack(pady=(15, 10))

        title = ctk.CTkLabel(
            self.profile_frame,
            text="Google Account",
            font=("Segoe UI", 18, "bold")
        )   

        title.pack(pady=(20, 10))

        name = ctk.CTkLabel(
            self.profile_frame,
            text=self.user_name,
            font=("Segoe UI", 16)
        )

        name.pack()

        email = ctk.CTkLabel(
            self.profile_frame,
            text=self.user_email,
            font=("Segoe UI", 13)
        )

        email.pack(pady=(0, 20))

        logout_btn = ctk.CTkButton(
            self.profile_frame,
            text="🚪 Logout",
            width=220,
            height=40,
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            command=self.logout
        )

        logout_btn.pack(pady=10)
    def build_user_info(self):

        frame = ctk.CTkFrame(self.app)

        frame.pack(fill="x", padx=15, pady=10)

        welcome = ctk.CTkLabel(
            frame,
            text="Welcome",
            font=("Segoe UI", 14)
        )

        welcome.pack(anchor="w", padx=10)

        name = ctk.CTkLabel(
            frame,
            text=self.user_name,
            font=("Segoe UI", 18, "bold")
        )

        name.pack(anchor="w", padx=10)

        email = ctk.CTkLabel(
            frame,
            text=self.user_email,
            font=("Segoe UI", 13)
        )

        email.pack(anchor="w", padx=10)
    def build_title(self):

        title = ctk.CTkLabel(
            self.home_frame,
            text="🔐 Password Generator",
            font=("Segoe UI", 30, "bold")
        )

        title.pack(pady=25)

        subtitle = ctk.CTkLabel(
            self.home_frame,
            text="Generate Strong & Secure Passwords",
            font=("Segoe UI", 16)
        )

        subtitle.pack(pady=5)
    def build_slider(self):

        self.length_frame = ctk.CTkFrame(self.home_frame)
        self.length_frame.pack(pady=20)

        length_label = ctk.CTkLabel(
            self.length_frame,
            text="Password Length",
            font=("Segoe UI", 18, "bold")
        )

        length_label.pack()

        self.length_value = ctk.CTkLabel(
            self.length_frame,
            text="16",
            font=("Segoe UI", 16)
        )

        self.length_value.pack()

        self.length_slider = ctk.CTkSlider(
            self.length_frame,
            from_=8,
            to=64,
            number_of_steps=56,
            command=self.update_slider,
            width=350
        )

        self.length_slider.set(16)
        self.length_slider.pack(pady=10)
    def update_slider(self, value):

        self.length_value.configure(
            text=str(int(value))
        )
    def build_options(self):

        self.options_frame = ctk.CTkFrame(self.home_frame)
        self.options_frame.pack(pady=15)

        self.uppercase_var = ctk.BooleanVar(value=True)
        self.lowercase_var = ctk.BooleanVar(value=True)
        self.numbers_var = ctk.BooleanVar(value=True)
        self.symbols_var = ctk.BooleanVar(value=True)

        uppercase = ctk.CTkCheckBox(
            self.options_frame,
            text="Uppercase",
            variable=self.uppercase_var
        )

        uppercase.grid(row=0, column=0, padx=20, pady=10)

        lowercase = ctk.CTkCheckBox(
            self.options_frame,
            text="Lowercase",
            variable=self.lowercase_var
        )

        lowercase.grid(row=0, column=1, padx=20)

        numbers = ctk.CTkCheckBox(
            self.options_frame,
            text="Numbers",
            variable=self.numbers_var
        )

        numbers.grid(row=1, column=0, padx=20)

        symbols = ctk.CTkCheckBox(
            self.options_frame,
            text="Symbols",
            variable=self.symbols_var
        )

        symbols.grid(row=1, column=1, padx=20)
    def build_password_box(self):

        self.password_frame = ctk.CTkFrame(self.home_frame)
        self.password_frame.pack(pady=20)

        self.password_entry = ctk.CTkEntry(
            self.password_frame,
            width=420,
            height=45,
            font=("Consolas", 18),
            justify="center",
            placeholder_text="Your password will appear here..."
        )

        self.password_entry.grid(
            row=0,
            column=0,
            padx=10,
            pady=10
        )

        self.show_btn = ctk.CTkButton(
            self.password_frame,
            text="👁",
            width=45,
            height=45,
            command=self.toggle_password
        )

        self.show_btn.grid(
            row=0,
            column=1,
            padx=5
        )
    def build_buttons(self):

        self.buttons_frame = ctk.CTkFrame(
            self.home_frame,
            fg_color="transparent"
        )

        self.buttons_frame.pack(pady=10)

        self.copy_btn = ctk.CTkButton(
            self.buttons_frame,
            text="📋 Copy",
            width=140,
            height=40,
            state="disabled",
            command=self.copy_password
        )

        self.copy_btn.grid(
            row=0,
            column=0,
            padx=10
        )

        history_btn = ctk.CTkButton(
            self.buttons_frame,
            text="📜 History",
            width=140,
            height=40,
            command=self.show_history
        )

        history_btn.grid(
            row=0,
            column=1,
            padx=10
        )

        generate_btn = ctk.CTkButton(
            self.home_frame,
            text="Generate Password",
            width=250,
            height=45,
            font=("Segoe UI", 16, "bold"),
            command=self.generate_password
        )

        generate_btn.pack(pady=15)
    def toggle_password(self):

        if self.password_entry.get() == "":
            return

        if self.password_hidden:

            self.password_entry.configure(show="")

            self.show_btn.configure(text="👁")

            self.password_hidden = False

        else:

            self.password_entry.configure(show="•")

            self.show_btn.configure(text="🙈")

            self.password_hidden = True
    def build_status(self):

        self.status_label = ctk.CTkLabel(
            self.home_frame,
            text="Ready to generate password",
            font=("Segoe UI", 14)
        )
        self.status_label.pack(pady=5)

        self.sync_label = ctk.CTkLabel(
            self.home_frame,
            text="☁ Last Sync: Never",
            font=("Segoe UI", 12)
        )
        self.sync_label.pack()
    def generate_password(self):

        length = int(self.length_slider.get())

        password = generate_random_password(
            length,
            self.uppercase_var.get(),
            self.lowercase_var.get(),
            self.numbers_var.get(),
            self.symbols_var.get()
        )

        if password == "":

            self.status_label.configure(
                text="⚠ Select at least one option!",
                text_color="red"
            )

            return

        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)

        self.copy_btn.configure(state="normal")

        self.status_label.configure(
        text="✅ Password Generated",
            text_color="lightgreen"
        )

        current_time = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")

        self.password_history.append({
            "date": current_time,
            "account": "",
            "password": password
        })

        save_history_file(self.password_history)
        self.sync_to_cloud()
        self.password_entry.configure(show="")
        self.show_btn.configure(text="👁")

        self.password_hidden = False
    def sync_to_cloud(self):
        upload_history(
            self.user_email,
            self.password_history
        )
    def update_sync_time(self):

        self.last_sync_time = datetime.now().strftime(
            "%d-%m-%Y %I:%M:%S %p"
        )

        self.sync_label.configure(
            text=f"☁ Last Sync: {self.last_sync_time}"
        )
    def auto_sync_loop(self):

        while True:

            if is_connected():

                self.sync_to_cloud()

            time.sleep(30)
    def copy_password(self):

        password = self.password_entry.get()

        if password == "":
            return

        copy_to_clipboard(
            self.home_frame,
            password
        )

        self.status_label.configure(
            text="📋 Password Copied!",
            text_color="lightgreen"
        )
   
    def run(self):

         self.app.mainloop()
    def logout(self):

        from auth import google_logout

        google_logout()
        self.show_login()

    def login_google(self):

        from auth import google_login

        google_login()

        self.password_history = download_history(
            self.user_email
        )

        save_history_file(
            self.password_history
        )

        self.show_master(
            create=not master_password_exists()
        )