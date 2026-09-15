import sqlite3
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# Database setup
conn = sqlite3.connect("bmi_records.db")
cursor = conn.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS bmi_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        weight REAL,
        height REAL,
        bmi REAL,
        category TEXT
    )
"""
)
conn.commit()


def calculate_bmi():
    name = entry_name.get().strip()
    try:
        weight = float(entry_weight.get())
        height = float(entry_height.get())
        if weight <= 0 or height <= 0:
            messagebox.showerror(
                "Input Error", "Weight and Height must be positive numbers."
            )
            return
    except ValueError:
        messagebox.showerror(
            "Input Error", "Please enter valid numeric values."
        )
        return

    bmi = round(weight / (height**2), 2)

    if bmi < 18.5:
        category = "Underweight"
        color = "#3b82f6"
    elif 18.5 <= bmi <= 24.9:
        category = "Normal"
        color = "#10b981"
    elif 25.0 <= bmi <= 29.9:
        category = "Overweight"
        color = "#f59e0b"
    else:
        category = "Obese"
        color = "#ef4444"

    lbl_result.config(
        text=f"BMI: {bmi} ({category})", fg=color, font=("Arial", 12, "bold")
    )

    if name:
        cursor.execute(
            "INSERT INTO bmi_data (name, weight, height, bmi, category) VALUES (?, ?, ?, ?, ?)",
            (name, weight, height, bmi, category),
        )
        conn.commit()
        messagebox.showinfo("Success", f"Record saved for {name}!")


def show_history():
    name = entry_name.get().strip()
    if not name:
        messagebox.showwarning(
            "Input Required", "Enter a name to view history graph."
        )
        return

    cursor.execute("SELECT bmi FROM bmi_data WHERE name = ?", (name,))
    records = cursor.fetchall()

    if not records:
        messagebox.showinfo("No Data", f"No records found for '{name}'.")
        return

    bmi_values = [r[0] for r in records]
    plt.figure(figsize=(6, 4))
    plt.plot(
        range(1, len(bmi_values) + 1),
        bmi_values,
        marker="o",
        color="#0284c7",
        linewidth=2,
    )
    plt.title(f"BMI History for {name}")
    plt.xlabel("Entry Number")
    plt.ylabel("BMI Value")
    plt.grid(True)
    plt.show()


# Tkinter GUI Setup
root = tk.Tk()
root.title("BMI Calculator")
root.geometry("380x380")
root.resizable(False, False)

tk.Label(root, text="BMI Calculator", font=("Arial", 16, "bold")).pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="User Name:").grid(row=0, column=0, sticky="w", pady=5)
entry_name = tk.Entry(frame)
entry_name.grid(row=0, column=1, pady=5)

tk.Label(frame, text="Weight (kg):").grid(row=1, column=0, sticky="w", pady=5)
entry_weight = tk.Entry(frame)
entry_weight.grid(row=1, column=1, pady=5)

tk.Label(frame, text="Height (m):").grid(row=2, column=0, sticky="w", pady=5)
entry_height = tk.Entry(frame)
entry_height.grid(row=2, column=1, pady=5)

btn_calc = tk.Button(
    root,
    text="Calculate & Save",
    command=calculate_bmi,
    bg="#10b981",
    fg="white",
    font=("Arial", 10, "bold"),
)
btn_calc.pack(pady=10)

lbl_result = tk.Label(root, text="BMI: --", font=("Arial", 12))
lbl_result.pack(pady=5)

btn_graph = tk.Button(
    root,
    text="View User BMI Trend",
    command=show_history,
    bg="#0284c7",
    fg="white",
)
btn_graph.pack(pady=5)

root.mainloop()