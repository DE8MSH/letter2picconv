import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

def run_combiner():
    # Holen der Werte aus den Eingabefeldern
    text = text_entry.get()
    image_dir = dir_entry.get()
    max_width = width_entry.get()
    output_file = output_entry.get()

    if not text or not image_dir or not max_width or not output_file:
        messagebox.showerror("Fehler", "Bitte füllen Sie alle Felder aus.")
        return

    try:
        max_width = int(max_width)
    except ValueError:
        messagebox.showerror("Fehler", "Maximale Breite muss eine Zahl sein.")
        return

    # Ausführen des Python-Skripts
    try:
        subprocess.run([
            "python3", "p.py", text, image_dir, str(max_width), output_file
        ], check=True)
        messagebox.showinfo("Erfolg", f"Ausgabebild gespeichert unter: {output_file}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten: {e}")

# Hauptfenster erstellen
root = tk.Tk()
root.title("letter2picconv by DO7OO")
root.geometry("600x600")

# Widgets erstellen
text_label = tk.Label(root, text="Text:")
text_label.pack(pady=5)
text_entry = tk.Entry(root, width=50)
text_entry.pack(pady=5)

dir_label = tk.Label(root, text="Bildverzeichnis:")
dir_label.pack(pady=5)

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        dir_entry.delete(0, tk.END)
        dir_entry.insert(0, directory)

dir_entry = tk.Entry(root, width=50)
dir_entry.pack(pady=5)
dir_button = tk.Button(root, text="Durchsuchen", command=browse_directory)
dir_button.pack(pady=5)

width_label = tk.Label(root, text="Maximale Breite:")
width_label.pack(pady=5)
width_entry = tk.Entry(root, width=50)
width_entry.pack(pady=5)

output_label = tk.Label(root, text="Ausgabedatei:")
output_label.pack(pady=5)

output_entry = tk.Entry(root, width=50)
output_entry.pack(pady=5)

def browse_output_file():
    output_file = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG-Dateien", "*.png")])
    if output_file:
        output_entry.delete(0, tk.END)
        output_entry.insert(0, output_file)

output_button = tk.Button(root, text="Speicherort auswählen", command=browse_output_file)
output_button.pack(pady=5)

run_button = tk.Button(root, text="Kombinieren", command=run_combiner)
run_button.pack(pady=20)

# Hauptschleife starten
root.mainloop()
