import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pymongo import MongoClient
import pandas as pd
import os
import matplotlib.pyplot as plt

client = MongoClient("mongodb://localhost:27017/")
db = client["women_safety_db"]
collection = db["alerts"]


def open_alert_window():

    window = tk.Toplevel()
    window.title("Women Safety - Alert Dashboard")
    window.geometry("1300x650")
    window.configure(bg="#f3f4f6")

    # ================= HEADER =================
    tk.Label(window, text="🚨 ALERT DASHBOARD",
             font=("Segoe UI", 20, "bold"),
             bg="#111827",
             fg="white",
             pady=15).pack(fill="x")

    # ================= SEARCH + FILTER FRAME =================
    top_frame = tk.Frame(window, bg="#f3f4f6")
    top_frame.pack(pady=10)

    tk.Label(top_frame, text="Search by Date (YYYY-MM-DD):",
             bg="#f3f4f6").grid(row=0, column=0, padx=5)

    date_entry = tk.Entry(top_frame)
    date_entry.grid(row=0, column=1, padx=5)

    tk.Label(top_frame, text="Filter by Emotion:",
             bg="#f3f4f6").grid(row=0, column=2, padx=5)

    emotion_combo = ttk.Combobox(top_frame,
                                  values=["", "fear"])
    emotion_combo.grid(row=0, column=3, padx=5)

    # ================= TABLE =================
    columns = ("date", "time", "emotion", "weapon", "message", "screenshot")
    tree = ttk.Treeview(window, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=150)

    tree.pack(fill="both", expand=True, padx=20, pady=10)

    # ================= FUNCTIONS =================
    def load_data():
        tree.delete(*tree.get_children())

        query = {}

        if date_entry.get():
            query["date"] = date_entry.get()

        if emotion_combo.get():
            query["emotion"] = emotion_combo.get()

        alerts = collection.find(query)

        for alert in alerts:
            tree.insert("", "end", values=(
                alert.get("date"),
                alert.get("time"),
                alert.get("emotion"),
                alert.get("weapon_detected"),
                alert.get("message"),
                alert.get("screenshot")
            ))

    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a row first")
            return

        item = tree.item(selected[0])
        date = item["values"][0]
        time = item["values"][1]

        collection.delete_one({"date": date, "time": time})
        load_data()

    def export_csv():
        alerts = list(collection.find())
        if not alerts:
            return

        df = pd.DataFrame(alerts)
        file_path = filedialog.asksaveasfilename(defaultextension=".csv")
        if file_path:
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Success", "Exported Successfully!")

    def show_graph():
        emotions = list(collection.find({}, {"emotion": 1}))
        emotion_list = [e["emotion"] for e in emotions if "emotion" in e]

        if not emotion_list:
            return

        plt.figure()
        plt.title("Emotion Analysis")
        plt.hist(emotion_list)
        plt.show()

    def open_image(event):
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])
            screenshot = item["values"][5]
            if os.path.exists(screenshot):
                os.startfile(screenshot)

    tree.bind("<Double-1>", open_image)

    # ================= BUTTONS =================
    bottom = tk.Frame(window, bg="#f3f4f6")
    bottom.pack(pady=10)

    tk.Button(bottom, text="🔍 Search",
              command=load_data,
              bg="#2563eb", fg="white").pack(side="left", padx=5)

    tk.Button(bottom, text="🗑 Delete",
              command=delete_selected,
              bg="#dc2626", fg="white").pack(side="left", padx=5)

    tk.Button(bottom, text="📥 Export CSV",
              command=export_csv,
              bg="#16a34a", fg="white").pack(side="left", padx=5)

    tk.Button(bottom, text="📊 Graph",
              command=show_graph,
              bg="#9333ea", fg="white").pack(side="left", padx=5)

    load_data()