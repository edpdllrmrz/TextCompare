"""
This is another version of the compare text app:


"""

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import time
import threading

class TextComparerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Compare: by @edpdllrmrz ---> https://github.com/edpdllrmrz")
        self.root.geometry("800x730")  # Set default window size to 800x730 pixels

        # Frame to hold upload buttons
        self.upload_frame = tk.Frame(root)
        self.upload_frame.pack(pady=10)

        # First file upload button
        self.upload_button1 = tk.Button(self.upload_frame, activebackground="#99e0aa", text="<--- Insert File 1 --->", command=self.upload_file1)
        self.upload_button1.pack(side=tk.LEFT, padx=(10, 5))

        # Second file upload button
        self.upload_button2 = tk.Button(self.upload_frame, activebackground="#99e0aa", text="<--- Insert File 2 --->", command=self.upload_file2)
        self.upload_button2.pack(side=tk.RIGHT, padx=(5, 10))

        # Frame to hold text areas
        self.text_frame = tk.Frame(root)
        self.text_frame.pack(pady=(0, 10))

        # Text area 1 to display file contents
        self.text_area1 = tk.Text(self.text_frame, height=15, width=45)
        self.text_area1.pack(side=tk.LEFT, padx=(10, 5))

        # Text area 2 to display file contents
        self.text_area2 = tk.Text(self.text_frame, height=15, width=45)
        self.text_area2.pack(side=tk.RIGHT, padx=(5, 10))

        # Compare button
        self.compare_button = tk.Button(root, text="Compare", bg="#d4ebf2", activeforeground="White", activebackground="#4dacc9", command=self.start_comparison)
        self.compare_button.pack()

        # Progress bar
        self.progress_bar = ttk.Progressbar(root, orient="horizontal", mode="determinate")
        self.progress_bar.pack(fill=tk.X, padx=10, pady=(0, 5))

        # Text area 3 to display differences
        self.text_area3 = tk.Text(root, height=20, width=80)
        self.text_area3.pack(pady=(0, 5))

        # Clear button
        self.clear_button = tk.Button(root, activebackground="#ff3333", activeforeground="White", text="Clear Everything", command=self.clear_all)
        self.clear_button.pack()

    def upload_file1(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file1_content = self.read_file_content(file_path)
            self.text_area1.delete("1.0", tk.END)
            self.text_area1.insert(tk.END, self.file1_content)

    def upload_file2(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file2_content = self.read_file_content(file_path)
            self.text_area2.delete("1.0", tk.END)
            self.text_area2.insert(tk.END, self.file2_content)

    def read_file_content(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()

    def start_comparison(self):
        if hasattr(self, 'file1_content') and hasattr(self, 'file2_content'):
            self.compare_button.config(state="disabled")  # Disable the Compare button
            self.progress_bar.start(10)  # Start the progress bar (filling up)
            threading.Thread(target=self.compare_files).start()  # Start comparison in a separate thread
        else:
            tk.messagebox.showinfo("Error", "Please upload both files before comparing.")

    def compare_files(self):
        # Simulate a time-consuming operation
        time.sleep(3)

        differences = self.compare_files_content(self.file1_content, self.file2_content)

        self.progress_bar.stop()  # Stop the progress bar
        self.compare_button.config(state="normal")  # Enable the Compare button again

        self.text_area3.delete("1.0", tk.END)
        self.text_area3.insert(tk.END, differences)

    def compare_files_content(self, file1_content, file2_content):
        differences = ""

        # Split the contents of each file into lines
        lines_file1 = file1_content.splitlines()
        lines_file2 = file2_content.splitlines()

        # Flag to check if there are differences
        has_differences = False

        # Iterate through lines
        for line_num, (line1, line2) in enumerate(zip(lines_file1, lines_file2), start=1):
            if line1 != line2:
                # Add the differences to the string
                differences += f"Difference found at line {line_num}:\n \n"
                differences += f"File 1: {line1}\n \n"
                differences += f"File 2: {line2}\n \n"
                has_differences = True

        # If no differences found, set the message to "NO DIFFERENCES"
        if not has_differences:
            differences = "***NO DIFFERENCES***"

        # If one file has more lines than the other
        if len(lines_file1) > len(lines_file2):
            for extra_line_num in range(len(lines_file2), len(lines_file1)):
                differences += f"Extra line in File 1 at line {extra_line_num + 1}: {lines_file1[extra_line_num]}\n"
        elif len(lines_file2) > len(lines_file1):
            for extra_line_num in range(len(lines_file1), len(lines_file2)):
                differences += f"Extra line in File 2 at line {extra_line_num + 1}: {lines_file2[extra_line_num]}\n"

        return differences

    def clear_all(self):
        self.text_area1.delete("1.0", tk.END)
        self.text_area2.delete("1.0", tk.END)
        self.text_area3.delete("1.0", tk.END)
        if hasattr(self, 'file1_content'):
            del self.file1_content
        if hasattr(self, 'file2_content'):
            del self.file2_content

root = tk.Tk()
app = TextComparerApp(root)
root.mainloop()
