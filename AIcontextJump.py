import os
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime

def process_folder():
    # 1. Ask user for directory
    root = tk.Tk()
    root.withdraw() # Hide the main tkinter window
    folder_path = filedialog.askdirectory(title="Select Folder to Context-Jump")
    
    if not folder_path:
        return # User cancelled

    # Get the folder name and current timestamp
    folder_name = os.path.basename(os.path.normpath(folder_path))
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # NEW naming format: AIcontextJump-(FolderName)_YYYY-MM-DD_HH-MM-SS.txt
    output_filename = f"AIcontextJump-({folder_name})_{timestamp}.txt"
    
    # Save the file in the parent directory of the selected folder 
    # (or you can keep it inside the folder if you prefer)
    output_path = os.path.join(folder_path, output_filename)

    # 2. Walk through all folders and subfolders
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for root_dir, dirs, files in os.walk(folder_path):
            for file in files:
                # Skip the output file itself
                if file == output_filename:
                    continue
                
                file_path = os.path.join(root_dir, file)
                
                try:
                    outfile.write(f"\n\n--- FILE: {file_path} ---\n\n")
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"\n[Could not read file {file}: {e}]\n")

    # 3. Success Notification
    messagebox.showinfo("Success", f"SUCCESS - File created at: {output_path}")

if __name__ == "__main__":
    process_folder()