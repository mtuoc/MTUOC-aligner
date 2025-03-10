import tkinter as tk
from tkinter import filedialog, messagebox
import codecs
import os

def process_files():
    dir_sl = source_dir_entry.get()
    dir_tl = target_dir_entry.get()
    dir_ali = aligned_dir_entry.get()
    batch_file = batch_file_entry.get()
    r1 = r1_entry.get()
    r2 = r2_entry.get()

    if not dir_sl or not dir_tl or not dir_ali or not batch_file:
        messagebox.showerror("Error", "Please specify all directories and the batch file name.")
        return

    try:
        if not os.path.exists(dir_ali):
            os.makedirs(dir_ali)

        files1 = []
        for r, d, f in os.walk(dir_sl):
            for file in f:
                files1.append(file)

        files2 = []
        for r, d, f in os.walk(dir_tl):
            for file in f:
                files2.append(file)

        with codecs.open(batch_file, "w", encoding="utf-8") as sortida:
            for file1 in files1:
                file2 = file1.replace(r1, r2)

                if file2 in files2:
                    dirfile1 = os.path.normpath(os.path.join(dir_sl, file1))
                    dirfile2 = os.path.normpath(os.path.join(dir_tl, file2))
                    fileali = "ali-" + file1
                    dirfileali = os.path.normpath(os.path.join(dir_ali, fileali))
                    cadena = f"{dirfile1}\t{dirfile2}\t{dirfileali}"
                    sortida.write(cadena + "\n")
                else:
                    print(f"*** {file1}")

        with open(batch_file) as f_input:
            data = f_input.read().rstrip('\n')

        with open(batch_file, 'w') as f_output:
            f_output.write(data)

        messagebox.showinfo("Success", "Batch file created successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def browse_source_dir():
    directory = filedialog.askdirectory(title="Select Source Language Directory")
    if directory:
        source_dir_entry.delete(0, tk.END)
        source_dir_entry.insert(0, directory)

def browse_target_dir():
    directory = filedialog.askdirectory(title="Select Target Language Directory")
    if directory:
        target_dir_entry.delete(0, tk.END)
        target_dir_entry.insert(0, directory)

def browse_aligned_dir():
    directory = filedialog.askdirectory(title="Select Aligned Files Directory")
    if directory:
        aligned_dir_entry.delete(0, tk.END)
        aligned_dir_entry.insert(0, directory)

def browse_batch_file():
    filename = filedialog.asksaveasfilename(title="Select Batch File", defaultextension=".txt")
    if filename:
        batch_file_entry.delete(0, tk.END)
        batch_file_entry.insert(0, filename)

# Create the main window
root = tk.Tk()
root.title("MTUOC-create-batchfileGUI")

# Source language directory
source_dir_label = tk.Label(root, text="Source Language Directory:")
source_dir_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

source_dir_entry = tk.Entry(root, width=50)
source_dir_entry.grid(row=0, column=1, padx=10, pady=5)

browse_source_dir_button = tk.Button(root, text="Browse", command=browse_source_dir)
browse_source_dir_button.grid(row=0, column=2, padx=10, pady=5)

# Target language directory
target_dir_label = tk.Label(root, text="Target Language Directory:")
target_dir_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

target_dir_entry = tk.Entry(root, width=50)
target_dir_entry.grid(row=1, column=1, padx=10, pady=5)

browse_target_dir_button = tk.Button(root, text="Browse", command=browse_target_dir)
browse_target_dir_button.grid(row=1, column=2, padx=10, pady=5)

# Aligned files directory
aligned_dir_label = tk.Label(root, text="Aligned Files Directory:")
aligned_dir_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

aligned_dir_entry = tk.Entry(root, width=50)
aligned_dir_entry.grid(row=2, column=1, padx=10, pady=5)

browse_aligned_dir_button = tk.Button(root, text="Browse", command=browse_aligned_dir)
browse_aligned_dir_button.grid(row=2, column=2, padx=10, pady=5)

# Batch file name
batch_file_label = tk.Label(root, text="Batch File Name:")
batch_file_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")

batch_file_entry = tk.Entry(root, width=50)
batch_file_entry.grid(row=3, column=1, padx=10, pady=5)

browse_batch_file_button = tk.Button(root, text="Browse", command=browse_batch_file)
browse_batch_file_button.grid(row=3, column=2, padx=10, pady=5)

# Replacement strings
r1_label = tk.Label(root, text="Replacement String 1 (Optional):")
r1_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")

r1_entry = tk.Entry(root, width=50)
r1_entry.grid(row=4, column=1, padx=10, pady=5)

r2_label = tk.Label(root, text="Replacement String 2 (Optional):")
r2_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")

r2_entry = tk.Entry(root, width=50)
r2_entry.grid(row=5, column=1, padx=10, pady=5)

# Process button
process_button = tk.Button(root, text="Process", command=process_files)
process_button.grid(row=6, column=0, columnspan=3, pady=10)

# Start the main loop
root.mainloop()
