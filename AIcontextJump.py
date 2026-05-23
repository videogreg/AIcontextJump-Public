import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from datetime import datetime

def process_folder():
    # 1. Ask for directory
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title="Select Folder to Context-Jump")
    if not folder_path: return

    # Setup the Progress Window
    progress_win = tk.Toplevel()
    progress_win.title("Processing...")
    progress_win.geometry("400x150")
    
    label = tk.Label(progress_win, text="Aggregating files, please wait...")
    label.pack(pady=10)
    
    # New label to show current file name
    current_file_label = tk.Label(progress_win, text="", wraplength=380, font=("Arial", 8))
    current_file_label.pack(pady=5)
    
    progress = ttk.Progressbar(progress_win, orient="horizontal", length=350, mode="determinate")
    progress.pack(pady=10)

    # Calculation for progress
    all_files = [os.path.join(r, f) for r, _, files in os.walk(folder_path) for f in files]
    total_files = len(all_files)
    progress["maximum"] = total_files

    # File logic
    def run_process():
        folder_name = os.path.basename(os.path.normpath(folder_path))
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_filename = f"AIcontextJump-({folder_name})_{timestamp}.txt"
        output_path = os.path.join(folder_path, output_filename)

        count = 0
        with open(output_path, 'w', encoding='utf-8') as outfile:
            for root_dir, _, files in os.walk(folder_path):
                for file in files:
                    if file == output_filename: continue
                    
                    # Update label with current filename
                    current_file_label.config(text=f"Processing: {file}")
                    
                    file_path = os.path.join(root_dir, file)
                    try:
                        outfile.write(f"\n\n--- FILE: {file_path} ---\n\n")
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                            outfile.write(infile.read())
                    except: pass
                    
                    count += 1
                    progress["value"] = count
        
        progress_win.destroy()
        messagebox.showinfo("Success", f"SUCCESS - File created at: {output_path}")

    # Run in background
    threading.Thread(target=run_process, daemon=True).start()
    progress_win.mainloop()

if __name__ == "__main__":
    process_folder()