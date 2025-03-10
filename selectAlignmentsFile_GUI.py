import tkinter as tk
from tkinter import filedialog, messagebox
import codecs
import unicodedata
import os

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0] != "C")

def process_file():
    input_file = input_file_entry.get()
    output_file = output_file_entry.get()
    try:
        confidence = float(confidence_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid numeric confidence value.")
        return

    if not input_file or not output_file:
        messagebox.showerror("Error", "Please specify both input and output files.")
        return

    try:
        with codecs.open(input_file, "r", encoding="utf-8") as entrada, \
             codecs.open(output_file, "w", encoding="utf-8") as sortida:

            llistasortida = []
            iguals = 0
            totals = 0

            for linia in entrada:
                linia = linia.rstrip().replace("~~~", "")
                camps = linia.split("\t")
                L1seg = camps[0].strip()
                L1seg = " ".join(L1seg.split())
                L2seg = camps[1].strip()
                L2seg = " ".join(L2seg.split())
                totals += 1
                if not L1seg == "<p>" and L1seg == L2seg:
                    iguals += 1
                sim = float(camps[2])
                if sim >= confidence and not L1seg == "<p>" and not L1seg == "" and not L2seg == "<p>" and not L2seg == "":
                    L1seg = remove_control_characters(L1seg)
                    L2seg = remove_control_characters(L2seg)
                    if len(L1seg) > 0 and len(L2seg) > 0:
                        cadena = L1seg + "\t" + L2seg
                        llistasortida.append(cadena)

            try:
                percent = iguals / totals
            except ZeroDivisionError:
                percent = 1

            if percent <= 0.5:
                for cadena in llistasortida:
                    camps = cadena.split("\t")
                    sl1 = camps[0]
                    sl2 = camps[1]
                    to_write = True
                    if len(sl1) > 25 and sl1 == sl2:
                        to_write = False
                    if to_write:
                        sortida.write(cadena + "\n")

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
root.title("selectAlignmentsFile_GUI")

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

# Confidence value
confidence_label = tk.Label(root, text="Confidence Value:")
confidence_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

confidence_entry = tk.Entry(root, width=50)
confidence_entry.grid(row=2, column=1, padx=10, pady=5)

# Process button
process_button = tk.Button(root, text="Process", command=process_file)
process_button.grid(row=3, column=0, columnspan=3, pady=10)

# Start the main loop
root.mainloop()