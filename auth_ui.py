import tkinter as tk
from tkinter import messagebox
from db import users_collection
import os


class AuthSystem:

    def __init__(self, root, open_alert_callback):
        self.root = root
        self.open_alert_callback = open_alert_callback

        self.root.title("Login - Women Safety System")
        self.root.geometry("500x450")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")

        self.show_login()

    # ================= LOGIN =================
    def show_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root,
            text="Login",
            font=("Segoe UI", 24, "bold"),
            bg="#1e1e1e",
            fg="white"
        ).pack(pady=30)

        # Username Label
        tk.Label(
            self.root,
            text="Username",
            font=("Segoe UI", 12),
            bg="#1e1e1e",
            fg="white"
        ).pack(pady=(10, 0))

        self.username_entry = tk.Entry(
            self.root,
            font=("Segoe UI", 14),
            width=25
        )
        self.username_entry.pack(pady=5)

        # Password Label
        tk.Label(
            self.root,
            text="Password",
            font=("Segoe UI", 12),
            bg="#1e1e1e",
            fg="white"
        ).pack(pady=(15, 0))

        self.password_entry = tk.Entry(
            self.root,
            show="*",
            font=("Segoe UI", 14),
            width=25
        )
        self.password_entry.pack(pady=5)

        tk.Button(
            self.root,
            text="Login",
            width=18,
            bg="#1f75fe",
            fg="white",
            command=self.login_check
        ).pack(pady=25)

        tk.Button(
            self.root,
            text="Create Account",
            width=18,
            bg="#444",
            fg="white",
            command=self.show_signup
        ).pack()

    def login_check(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = users_collection.find_one({
            "username": username,
            "password": password
        })

        if user:
            with open("session.txt", "w") as f:
                f.write("logged_in=True")

            messagebox.showinfo("Success", "Login Successful")
            self.root.destroy()
            self.open_alert_callback()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

    # ================= SIGNUP =================
    def show_signup(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root,
            text="Sign Up",
            font=("Segoe UI", 24, "bold"),
            bg="#1e1e1e",
            fg="white"
        ).pack(pady=30)

        # Username Label
        tk.Label(
            self.root,
            text="Username",
            font=("Segoe UI", 12),
            bg="#1e1e1e",
            fg="white"
        ).pack(pady=(10, 0))

        self.new_user = tk.Entry(
            self.root,
            font=("Segoe UI", 14),
            width=25
        )
        self.new_user.pack(pady=5)

        # Password Label
        tk.Label(
            self.root,
            text="Password",
            font=("Segoe UI", 12),
            bg="#1e1e1e",
            fg="white"
        ).pack(pady=(15, 0))

        self.new_pass = tk.Entry(
            self.root,
            show="*",
            font=("Segoe UI", 14),
            width=25
        )
        self.new_pass.pack(pady=5)

        tk.Button(
            self.root,
            text="Create Account",
            width=18,
            bg="#ff2e75",
            fg="white",
            command=self.create_account
        ).pack(pady=25)

        tk.Button(
            self.root,
            text="Back to Login",
            width=18,
            bg="#444",
            fg="white",
            command=self.show_login
        ).pack()

    def create_account(self):
        username = self.new_user.get()
        password = self.new_pass.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields required")
            return

        if users_collection.find_one({"username": username}):
            messagebox.showerror("Error", "User already exists")
        else:
            users_collection.insert_one({
                "username": username,
                "password": password
            })
            messagebox.showinfo("Success", "Account Created Successfully")
            self.show_login()