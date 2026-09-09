import customtkinter as ctk
from history import save_history_file, load_history
class HistoryFrame:

    def __init__(self, parent, password_history, app):
        self.app = app
        self.parent = parent
        self.password_history = password_history
        self.account_entries = []
    def build(self):

        for widget in self.parent.winfo_children():
            widget.destroy()
        back_btn = ctk.CTkButton(
            self.parent,
            text="← Back",
            width=110,
            command=self.app.show_home
        )

        back_btn.pack(
            anchor="nw",
            padx=15,
            pady=15
        )

        title = ctk.CTkLabel(
            self.parent,
            text="📜 Password History",
            font=("Segoe UI", 22, "bold")
        )

        title.pack(pady=15)

        self.history_frame = ctk.CTkScrollableFrame(
            self.parent
        )

        self.history_frame.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=10
        )
        self.refresh()
        save_btn = ctk.CTkButton(
            self.parent,
            text="💾 Save Changes",
            width=180,
            height=40,
            command=self.save_notes
        )

        save_btn.pack(pady=10)
    def refresh(self):
        self.account_entries.clear()
        for widget in self.history_frame.winfo_children():
            widget.destroy()

        if not self.password_history:

            empty = ctk.CTkLabel(
                self.history_frame,
                text="No password history available."
            )

            empty.pack(pady=30)

            return

        for index, item in enumerate(self.password_history):

            self.create_card(index, item)
    def create_card(self, index, item):

        card = ctk.CTkFrame(self.history_frame)

        card.pack(
            fill="x",
            padx=5,
            pady=8
        )

        date_label = ctk.CTkLabel(
            card,
            text=item["date"],
            font=("Segoe UI", 12)
        )

        date_label.pack(
            anchor="w",
            padx=10,
            pady=(8, 2)
        )
        account_entry = ctk.CTkEntry(
            card,
            width=250,
            placeholder_text="Account Name (Gmail, Instagram...)"
        )

        account_entry.insert(
            0,
            item["account"]
        )

        account_entry.pack(
            anchor="w",
            padx=10,
            pady=5
        )
        self.account_entries.append(account_entry)
        bottom_frame = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        bottom_frame.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )
        password_entry = ctk.CTkEntry(
            bottom_frame,
            width=420,
            show="•"
        )

        password_entry.insert(
            0,
            item["password"]
        )

        password_entry.pack(
            side="left",
            padx=(0, 10)
        )
        show_btn = ctk.CTkButton(
            bottom_frame,
            text="👁",
            width=40
        )

        show_btn.configure(
            command=lambda e=password_entry, b=show_btn:
            self.toggle_history_password(e, b)
        )

        show_btn.pack(
            side="left",
            padx=5
        )
        copy_btn = ctk.CTkButton(
            bottom_frame,
            text="📋",
            width=40,
            command=lambda p=item["password"]:
            self.copy_history_password(p)
        )

        copy_btn.pack(
            side="left",
            padx=5
        )
        delete_btn = ctk.CTkButton(
            bottom_frame,
            text="🗑",
            width=40,
            fg_color="red",
            hover_color="#8B0000",
            command=lambda i=index:
            self.delete_password(i)
        )

        delete_btn.pack(
            side="left",
            padx=5
        )
    def toggle_history_password(self, entry, button):

        if entry.cget("show") == "":
            entry.configure(show="•")
            button.configure(text="👁")
        else:
            entry.configure(show="")
            button.configure(text="🙈")

    def copy_history_password(self, password):

        self.app.app.clipboard_clear()
        self.app.app.clipboard_append(password)
    def delete_password(self, index):

        del self.password_history[index]

        save_history_file(self.password_history)
        self.app.sync_to_cloud()
        self.refresh()
    def save_notes(self):

        for index, entry in enumerate(self.account_entries):

            self.password_history[index]["account"] = entry.get()

        save_history_file(self.password_history)
        self.app.sync_to_cloud()
        status = ctk.CTkLabel(
            self.parent,
            text="✅ Changes Saved",
            text_color="lightgreen"
        )

        status.pack(pady=5)

        self.parent.after(
            1500,
            status.destroy
        )

