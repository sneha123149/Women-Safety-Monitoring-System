import tkinter as tk
import os


def open_alert_window():
    alert_window = tk.Toplevel()
    alert_window.title("Alert Monitoring Section")
    alert_window.geometry("900x500")
    alert_window.configure(bg="#1e1e1e")

    tk.Label(
        alert_window,
        text="Alert Monitoring Dashboard",
        font=("Segoe UI", 22, "bold"),
        bg="#1e1e1e",
        fg="white"
    ).pack(pady=30)

    tk.Label(
        alert_window,
        text="Here your emotion detection alerts will appear.\n\n"
             "You can connect this with your MongoDB data.",
        font=("Segoe UI", 14),
        bg="#1e1e1e",
        fg="white"
    ).pack(pady=20)

    # Logout Button
    def logout():
        if os.path.exists("session.txt"):
            os.remove("session.txt")
        alert_window.destroy()

    tk.Button(
        alert_window,
        text="Logout",
        width=15,
        command=logout
    ).pack(pady=40)