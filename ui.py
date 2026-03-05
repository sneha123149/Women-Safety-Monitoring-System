import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from detection.camera import start_camera
from auth_ui import AuthSystem
from view_alerts import open_alert_window
from emergency_handler import trigger_emergency
import os


# =============================
# MAIN WINDOW SETUP
# =============================
root = tk.Tk()
root.title("Women Safety System")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")
root.resizable(False, False)


# =============================
# FUNCTIONS
# =============================

def start_detection():
    start_camera()


# ---- Session Based Alert Access ----
def open_alerts_with_session():
    if os.path.exists("session.txt"):
        open_alert_window()
    else:
        AuthSystem(tk.Toplevel(root), open_alert_window)


# ---- Emergency Button Action ----
def emergency_action():
    success = trigger_emergency()

    if success:
        messagebox.showinfo("Emergency", "🚨 Emergency alert sent successfully!")
    else:
        messagebox.showerror("Emergency", "Failed to send emergency alert.")


# ---- Proper Logout ----
def logout_user():
    if os.path.exists("session.txt"):
        os.remove("session.txt")
        messagebox.showinfo("Logout", "You have been logged out successfully.")
    else:
        messagebox.showinfo("Logout", "No active session found.")

    close_sidebar()


# ---- Sidebar Toggle ----
sidebar_visible = False

def toggle_sidebar():
    global sidebar_visible
    if sidebar_visible:
        sidebar.place(x=-250, y=0)
        sidebar_visible = False
    else:
        sidebar.place(x=0, y=0)
        sidebar_visible = True

def close_sidebar():
    global sidebar_visible
    sidebar.place(x=-250, y=0)
    sidebar_visible = False


# =============================
# BACKGROUND IMAGE
# =============================
bg_image = Image.open("bg1.png")
bg_image = bg_image.resize((screen_width, screen_height), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


# =============================
# SIDEBAR
# =============================
sidebar = tk.Frame(root, width=250, bg="#111111", height=screen_height)
sidebar.place(x=-250, y=0)

tk.Label(
    sidebar,
    text="MENU",
    bg="#111111",
    fg="white",
    font=("Segoe UI", 18, "bold")
).pack(pady=20)

tk.Button(
    sidebar,
    text="Login / Sign Up",
    bg="#222",
    fg="white",
    relief="flat",
    command=lambda: AuthSystem(tk.Toplevel(root), open_alert_window)
).pack(fill="x", pady=5, padx=20)

tk.Button(
    sidebar,
    text="View Alerts",
    bg="#222",
    fg="white",
    relief="flat",
    command=open_alerts_with_session
).pack(fill="x", pady=5, padx=20)

tk.Button(
    sidebar,
    text="Emergency Contacts",
    bg="#222",
    fg="white",
    relief="flat",
    command=lambda: open_emergency_window()
).pack(fill="x", pady=5, padx=20)

tk.Button(
    sidebar,
    text="Help",
    bg="#222",
    fg="white",
    relief="flat",
    command=lambda: open_help_window()
).pack(fill="x", pady=5, padx=20)

tk.Button(
    sidebar,
    text="Logout",
    bg="#8b0000",
    fg="white",
    relief="flat",
    command=logout_user
).pack(fill="x", pady=5, padx=20)


# =============================
# HAMBURGER MENU BUTTON
# =============================
menu_button = tk.Button(
    root,
    text="☰",
    font=("Segoe UI", 22),
    bg="black",
    fg="white",
    bd=0,
    command=toggle_sidebar
)
menu_button.place(x=20, y=20)


# =============================
# EMERGENCY CONTACT WINDOW
# =============================
def open_emergency_window():
    emergency = tk.Toplevel(root)
    emergency.title("Emergency Contacts")
    emergency.geometry("500x450")
    emergency.configure(bg="#111111")
    emergency.resizable(False, False)

    tk.Label(
        emergency,
        text="Emergency Support",
        font=("Segoe UI", 20, "bold"),
        bg="#111111",
        fg="#ff2e75"
    ).pack(pady=20)

    contacts = [
        ("🚓 Police", "100"),
        ("👩 Women Helpline", "181"),
        ("🚑 Ambulance", "108"),
        ("📞 National Emergency", "112"),
        ("👶 Child Helpline", "1098")
    ]

    for name, number in contacts:
        frame = tk.Frame(emergency, bg="#1c1c1c")
        frame.pack(fill="x", padx=40, pady=8)

        tk.Label(frame, text=name,
                 font=("Segoe UI", 12),
                 bg="#1c1c1c",
                 fg="white").pack(side="left", padx=10)

        tk.Label(frame, text=number,
                 font=("Segoe UI", 12, "bold"),
                 bg="#1c1c1c",
                 fg="#1f75fe").pack(side="right", padx=10)

    tk.Button(
        emergency,
        text="Close",
        bg="#ff2e75",
        fg="white",
        width=15,
        command=emergency.destroy
    ).pack(pady=25)


# =============================
# HELP WINDOW
# =============================
def open_help_window():
    help_win = tk.Toplevel(root)
    help_win.title("Help & User Guide")
    help_win.geometry("600x500")
    help_win.configure(bg="#111111")
    help_win.resizable(False, False)

    tk.Label(
        help_win,
        text="System Help Guide",
        font=("Segoe UI", 20, "bold"),
        bg="#111111",
        fg="#1f75fe"
    ).pack(pady=20)

    help_text = (
        "Welcome to Women Safety Monitoring System\n\n"
        "HOW TO USE:\n"
        "• Click START to begin live detection.\n"
        "• Click ALERTS to view stored alert records.\n"
        "• Click EMERGENCY to send instant alert without camera.\n\n"
        "FEATURES:\n"
        "• Real-Time Emotion Detection\n"
        "• Manual Emergency Alert System\n"
        "• SMS Notification\n"
        "• MongoDB Database Integration\n"
        "• Secure Login System\n"
    )

    tk.Label(
        help_win,
        text=help_text,
        justify="left",
        bg="#111111",
        fg="white",
        font=("Segoe UI", 11),
        wraplength=520
    ).pack(padx=30, pady=10)

    tk.Button(
        help_win,
        text="Close",
        bg="#1f75fe",
        fg="white",
        width=15,
        command=help_win.destroy
    ).pack(pady=20)


# =============================
# CIRCLE BUTTON FUNCTION
# =============================
def create_circle_button(parent, text, command, color, hover_color):

    canvas = tk.Canvas(parent, width=100, height=100,
                       bg="black", highlightthickness=0)
    canvas.pack(pady=15)

    circle = canvas.create_oval(5, 5, 95, 95, fill=color, outline="")

    canvas.create_text(
        50, 50,
        text=text,
        fill="white",
        font=("Segoe UI", 9, "bold"),
        width=70
    )

    def on_enter(event):
        canvas.itemconfig(circle, fill=hover_color)

    def on_leave(event):
        canvas.itemconfig(circle, fill=color)

    def on_click(event):
        command()

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    canvas.bind("<Button-1>", on_click)

    return canvas


# =============================
# RIGHT SIDE BUTTONS
# =============================
button_frame = tk.Frame(root, bg="black")
button_frame.place(relx=0.93, rely=0.40, anchor="center")

create_circle_button(
    button_frame,
    "START",
    start_detection,
    "#ff2e75",
    "#cc0052"
)

create_circle_button(
    button_frame,
    "ALERTS",
    open_alerts_with_session,
    "#1f75fe",
    "#0047ab"
)

create_circle_button(
    button_frame,
    "EMERGENCY",
    emergency_action,
    "#8b0000",
    "#5c0000"
)


# =============================
# FOOTER
# =============================
footer = tk.Label(
    root,
    text="AI Powered Real-Time Women Safety Monitoring System",
    font=("Segoe UI", 10),
    fg="white",
    bg="black",
    padx=10,
    pady=4
)
footer.place(relx=0.5, rely=0.97, anchor="center")


root.mainloop()