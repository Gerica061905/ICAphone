import tkinter as tk
from tkinter import messagebox, scrolledtext, simpledialog
import math
import re

def format_number(number):
    number = str(number).strip()

    # Remove non-digit characters
    number = ''.join(filter(str.isdigit, number))

    # Fix numbers that start with "63" but are missing a digit (e.g., 63xxxxxxxxx)
    if number.startswith('63') and len(number) == 11:
        number = '639' + number[2:]

    # Fix numbers that are 9 digits and start with a non-9 digit (like 603590539)
    if len(number) == 9 and not number.startswith('9'):
        number = '9' + number

    # If number has 10 digits and starts with 9, assume it's valid PH mobile and add +63
    if len(number) == 10 and number.startswith('9'):
        number = '63' + number

    # Final format
    if number.startswith('63') and len(number) == 12:
        return '+{}'.format(number)
    else:
        return None  # Invalid number

# Example usage:
numbers = ['603590539', '935905390', '63935905390', '93590539']
for n in numbers:
    formatted = format_number(n)
    print(f"Original: {n} => Formatted: {formatted}")


def process_numbers():
    raw_text = input_text.get("1.0", tk.END).strip()
    if not raw_text:
        messagebox.showwarning("No Input", "Please enter phone numbers.")
        return

    # Extract all sequences of digits and '+' that resemble phone numbers
    raw_numbers = re.findall(r"\+?\d{10,13}", raw_text)
    formatted_numbers = [format_number(n) for n in raw_numbers]
    formatted_numbers = [n for n in formatted_numbers if n]  # Remove None values
    # Remove duplicates while preserving order
    formatted_numbers = list(dict.fromkeys(formatted_numbers))

    batch_size = 48
    max_batches = 200
    total_batches = min(max_batches, math.ceil(len(formatted_numbers) / batch_size))

    if total_batches == 0:
        messagebox.showinfo("Not Enough Numbers", "You need at least 1 number to make a batch.")
        return

    # Ask for one 1st number
    first_number = simpledialog.askstring("1st Number",
        f"Enter the 1st number to be used for all {total_batches} batches:", parent=root)
    if not first_number:
        messagebox.showerror("Missing Input", "You didn't enter the 1st number.")
        return
    first_number = format_number(first_number)
    if not first_number:
        messagebox.showerror("Invalid Input", "The 1st number format is invalid.")
        return

    # Ask for one 50th number
    fiftieth_number = simpledialog.askstring("50th Number",
        f"Enter the 50th number to be used for all {total_batches} batches:", parent=root)
    if not fiftieth_number:
        messagebox.showerror("Missing Input", "You didn't enter the 50th number.")
        return
    fiftieth_number = format_number(fiftieth_number)
    if not fiftieth_number:
        messagebox.showerror("Invalid Input", "The 50th number format is invalid.")
        return

    # Ask for output filename
    file_name = simpledialog.askstring("File Name", "Enter a name for your output text file (without .txt):", parent=root)
    if not file_name:
        messagebox.showwarning("Missing File Name", "You must enter a file name.")
        return
    file_name = file_name.strip() + ".txt"

    output_text.delete("1.0", tk.END)
    output_lines = []

    for i in range(total_batches):
        start = i * batch_size
        end = min(start + batch_size, len(formatted_numbers))
        middle_48 = formatted_numbers[start:end]

        batch = [first_number] + middle_48 + [fiftieth_number]

        output_text.insert(tk.END, "\n".join(batch) + "\n\n")
        output_lines.extend(batch)
        output_lines.append("")  # blank line between batches

    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(output_lines))
        messagebox.showinfo("Saved", f"Output saved to '{file_name}'")
    except Exception as e:
        messagebox.showerror("File Error", f"Failed to save file: {e}")

# GUI Setup
root = tk.Tk()
root.title("icaphone")
root.configure(bg="light pink")
root.geometry("800x600")

tk.Label(root, text="Enter Phone Numbers (any format):", bg="light pink").pack()
input_text = scrolledtext.ScrolledText(root, height=10, width=90)
input_text.pack(padx=10, pady=5)

tk.Label(root, text="Optional Batch Name:", bg="light pink").pack()
batch_name_entry = tk.Entry(root, width=50)
batch_name_entry.pack(pady=5)

tk.Button(root, text="Process Numbers", command=process_numbers, bg="#fbaed2").pack(pady=10)

output_text = scrolledtext.ScrolledText(root, height=20, width=90)
output_text.pack(padx=10, pady=10)

root.mainloop()