import tkinter as tk
from tkinter import filedialog, messagebox
import codecs

def process_files():
    input_file = input_file_entry.get()
    output_file = output_file_entry.get()

    if not input_file or not output_file:
        messagebox.showerror("Error", "Please specify both input and output files.")
        return

    try:
        with codecs.open(input_file, "r", encoding="utf-8") as entrada, \
             codecs.open(output_file, "w", encoding="utf-8") as sortida:

            for linia in entrada:
                linia = linia.rstrip()
                try:
                    linia = linia.replace("\t", " ")
                    camps = linia.split(" ")
                    cadena = camps[1].strip() + " @ " + camps[0].strip()
                    sortida.write(cadena + "\n")
                except:
                    pass

        messagebox.showinfo("Success", "File processed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def browse_input_file():
    filename = filedialog.askopenfilename(title="Select Input File")
    if filename:
        input_file_entry.delete(0, tk.END)
        input_file_entry.insert(0, filename)

def browse_output_file():
    filename = filedialog.asksaveasfilename(title="Select Output File", defaultextension=".txt")
    if filename:
        output_file_entry.delete(0, tk.END)
        output_file_entry.insert(0, filename)

# Create the main window
root = tk.Tk()
root.title("Muse2Hunalign")

# Input file selection
input_file_label = tk.Label(root, text="Input File:")
input_file_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

input_file_entry = tk.Entry(root, width=50)
input_file_entry.grid(row=0, column=1, padx=10, pady=5)

browse_input_button = tk.Button(root, text="Browse", command=browse_input_file)
browse_input_button.grid(row=0, column=2, padx=10, pady=5)

# Output file selection
output_file_label = tk.Label(root, text="Output File:")
output_file_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

output_file_entry = tk.Entry(root, width=50)
output_file_entry.grid(row=1, column=1, padx=10, pady=5)

browse_output_button = tk.Button(root, text="Browse", command=browse_output_file)
browse_output_button.grid(row=1, column=2, padx=10, pady=5)

# Process button
process_button = tk.Button(root, text="Process", command=process_files)
process_button.grid(row=2, column=0, columnspan=3, pady=10)

# Start the main loop
root.mainloop()
