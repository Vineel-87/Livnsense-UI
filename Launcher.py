import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
import threading

SCRIPT_FOLDER = os.path.join(os.getcwd(), "Features", "Tests")

def get_script_by_number(number):
    scripts = {}
    for file in os.listdir(SCRIPT_FOLDER):
        if file.endswith(".py"):
            try:
                num = int(file.split("_")[0])
                scripts[num] = file
            except:
                continue
    return scripts.get(number, None)

# Flag to indicate if a test is currently running
is_running = False

def run_script():
    global is_running
    if is_running:
        messagebox.showwarning("Please wait", "A script is already running. Please wait until it finishes.")
        return

    try:
        num = int(entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid script number.")
        return

    script = get_script_by_number(num)
    if not script:
        messagebox.showwarning("Not Found", f"No script found for number {num}.")
        return

    script_path = os.path.join(SCRIPT_FOLDER, script)
    python_executable = sys.executable

    def run():
        global is_running
        try:
            is_running = True
            # Disable button while running
            run_button.config(state=tk.DISABLED)

            command = [
                python_executable, "-m", "pytest",
                script_path,
                "-s",
                "--maxfail=1"
            ]

            process = subprocess.run(command, capture_output=True, text=True, cwd=SCRIPT_FOLDER)

            if process.returncode == 0:
                messagebox.showinfo("Success", f"Script {script} ran successfully!")
            else:
                error_message = process.stdout + "\n" + process.stderr
                messagebox.showerror("Test Failed", f"Script {script} failed.\n\nOutput:\n{error_message}")
        except Exception as e:
            messagebox.showerror("Error", f"Error running script: {e}")
        finally:
            is_running = False
            run_button.config(state=tk.NORMAL)

    threading.Thread(target=run, daemon=True).start()

window = tk.Tk()
window.title("Automation Script Runner")
window.geometry("400x200")
window.configure(bg="#f0f0f0")

tk.Label(window, text="Enter Script Number (1 to 11):", font=("Arial", 12), bg="#f0f0f0").pack(pady=20)

entry = tk.Entry(window, font=("Arial", 14), width=10, justify="center")
entry.pack()

run_button = tk.Button(window, text="Run Script", command=run_script,
                       font=("Arial", 12, "bold"), bg="#007BFF", fg="white")
run_button.pack(pady=20)

window.mainloop()
