import tkinter as tk
from tkinter import messagebox


def open_login(root, open_dashboard):

    login_window = tk.Toplevel(root)
    login_window.title("Admin Login")
    login_window.geometry("400x300")
    login_window.configure(bg="#1f2937")

    tk.Label(login_window, text="ADMIN LOGIN",
             font=("Segoe UI", 18, "bold"),
             bg="#1f2937", fg="white").pack(pady=20)

    tk.Label(login_window, text="Username",
             bg="#1f2937", fg="white").pack()

    username_entry = tk.Entry(login_window, font=("Segoe UI", 12))
    username_entry.pack(pady=5)

    tk.Label(login_window, text="Password",
             bg="#1f2937", fg="white").pack()

    password_entry = tk.Entry(login_window, show="*", font=("Segoe UI", 12))
    password_entry.pack(pady=5)

    def check_login():
        username = username_entry.get()
        password = password_entry.get()

        if username == "admin" and password == "1234":
            login_window.destroy()
            open_dashboard()
        else:
            messagebox.showerror("Error", "Invalid Credentials")

    tk.Button(login_window, text="Login",
              command=check_login,
              bg="#2563eb",
              fg="white",
              font=("Segoe UI", 12, "bold"),
              padx=10,
              pady=5).pack(pady=20)