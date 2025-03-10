import tkinter as tk
from tkinter import filedialog, messagebox
import codecs

def process_files():
    input_file_x = input_file_x_entry.get()
    input_file_y = input_file_y_entry.get()
    output_file = output_file_entry.get()

    if not input_file_x or not input_file_y or not output_file:
        messagebox.showerror("Error", "Please specify all input and output files.")
        return

    try:
        dic_en_x = {}
        dic_en_y = {}

        with codecs.open(input_file_x, "r", encoding="utf-8") as entrada_x:
            for linia in entrada_x:
                linia = linia.strip()
                try:
                    x, en = linia.split("\t")
                    if en not in dic_en_x:
                        dic_en_x[en] = []
                    dic_en_x[en].append(x)
                except:
                    pass

        with codecs.open(input_file_y, "r", encoding="utf-8") as entrada_y:
            for linia in entrada_y:
                linia = linia.strip()
                try:
                    y, en = linia.split("\t")
                    if en not in dic_en_y:
                        dic_en_y[en] = []
                    dic_en_y[en].append(y)
                except:
                    pass

        with codecs.open(output_file, "w", encoding="utf-8") as sortida:
            for en in dic_en_x:
                if en in dic_en_y:
                    for x in dic_en_x[en]:
                        for y in dic_en_y[en]:
                            cadena = f"{y} @ {x}"
                            sortida.write(cadena + "\n")

        messagebox.showinfo("Success", "Files processed successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def browse_input_file_x():
    filename = filedialog.askopenfilename(title="Select Input File X")
    if filename:
        input_file_x_entry.delete(0, tk.END)
        input_file_x_entry.insert(0, filename)

def browse_input_file_y():
    filename = filedialog.askopenfilename(title="Select Input File Y")
    if filename:
        input_file_y_entry.delete(0, tk.END)
        input_file_y_entry.insert(0, filename)

def browse_output_file():
    filename = filedialog.asksaveasfilename(title="Select Output File", defaultextension=".txt")
    if filename:
        output_file_entry.delete(0, tk.END)
        output_file_entry.insert(0, filename)

# Create the main window
root = tk.Tk()
root.title("MUSE2Hunalign-X-en-Y-GUI")

# Input file X selection
input_file_x_label = tk.Label(root, text="Muse X-en:")
input_file_x_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

input_file_x_entry = tk.Entry(root, width=50)
input_file_x_entry.grid(row=0, column=1, padx=10, pady=5)

browse_input_x_button = tk.Button(root, text="Browse", command=browse_input_file_x)
browse_input_x_button.grid(row=0, column=2, padx=10, pady=5)

# Input file Y selection
input_file_y_label = tk.Label(root, text="Muse Y-en:")
input_file_y_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")

input_file_y_entry = tk.Entry(root, width=50)
input_file_y_entry.grid(row=1, column=1, padx=10, pady=5)

browse_input_y_button = tk.Button(root, text="Browse", command=browse_input_file_y)
browse_input_y_button.grid(row=1, column=2, padx=10, pady=5)

# Output file selection
output_file_label = tk.Label(root, text="Output hunalign dict X-Y:")
output_file_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")

output_file_entry = tk.Entry(root, width=50)
output_file_entry.grid(row=2, column=1, padx=10, pady=5)

browse_output_button = tk.Button(root, text="Browse", command=browse_output_file)
browse_output_button.grid(row=2, column=2, padx=10, pady=5)

# Process button
process_button = tk.Button(root, text="Process", command=process_files)
process_button.grid(row=3, column=0, columnspan=3, pady=10)

# Start the main loop
root.mainloop()
