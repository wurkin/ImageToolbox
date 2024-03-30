import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter.ttk import Progressbar
import threading
import app.image_processor
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

class ImageToolboxGUI:
    def __init__(self, master):
        self.master = master
        master.title("ImageToolbox")

        self.configure_gui()
        self.create_widgets()

    def configure_gui(self):
        self.master.geometry("600x800")  # Adjust window size as needed

    def create_widgets(self):
        # Input Directory Label and Entry
        self.label_input_dir = tk.Label(self.master, text="Select Input Folder:")
        self.label_input_dir.pack(pady=(10,0))
        self.input_dir_path = tk.Entry(self.master, width=60)
        self.input_dir_path.pack(pady=5)
        self.browse_input_button = tk.Button(self.master, text="Browse Input Folder", command=self.browse_input_folder)
        self.browse_input_button.pack(pady=5)

        # Output Directory Label and Entry
        self.label_output_dir = tk.Label(self.master, text="Select Output Folder:")
        self.label_output_dir.pack(pady=(10,0))
        self.output_dir_path = tk.Entry(self.master, width=60)
        self.output_dir_path.pack(pady=5)
        self.browse_output_button = tk.Button(self.master, text="Browse Output Folder", command=self.browse_output_folder)
        self.browse_output_button.pack(pady=5)

        # Progress Bar
        self.progress = Progressbar(self.master, orient=tk.HORIZONTAL, length=300, mode='determinate')
        self.progress.pack(pady=20)

        # Log Viewer
        self.log_viewer = scrolledtext.ScrolledText(self.master, height=10)
        self.log_viewer.pack(pady=10)
        self.log_viewer.configure(state ='disabled')

        # Start Processing Button
        self.start_button = tk.Button(self.master, text="Start Processing", command=self.start_processing)
        self.start_button.pack(pady=10)

    def browse_input_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.input_dir_path.delete(0, tk.END)
            self.input_dir_path.insert(0, folder_selected)

    def browse_output_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_dir_path.delete(0, tk.END)
            self.output_dir_path.insert(0, folder_selected)

    def log_message(self, message):
        self.log_viewer.configure(state='normal')
        self.log_viewer.insert(tk.END, message + "\n")
        self.log_viewer.configure(state='disabled')
        self.log_viewer.yview(tk.END)

    def update_progress(self, progress):
        self.progress['value'] = progress
        self.master.update_idletasks()

    def start_processing(self):
        input_dir = self.input_dir_path.get()
        output_dir = self.output_dir_path.get()
        self.process_images(input_dir, output_dir, None)
        if not input_dir or not output_dir:
            messagebox.showinfo("Information", "Please select both input and output folders.")
            return

        self.start_button.config(state='enabled')

        # Define a callback for updating the GUI from another thread
        def callback(progress, error=None):
            self.master.after(0, self.update_progress, progress)
            if error:
                self.master.after(0, self.log_message, f"Error: {error}")

        threading.Thread(target=lambda: self.process_images(input_dir, output_dir, callback), daemon=True).start()

    def process_images(self, input_dir, output_dir, callback):
        from .image_processor import predict_images, scan_directory_for_images
        image_path = scan_directory_for_images(self.input_dir_path.get())
        predict_images(image_path, self.log_message)
        self.master.after(0, self.log_message, "Processing completed.")
        self.master.after(0, self.start_button.config, {'state': 'normal'})

def run_app():
    root = tk.Tk()
    app = ImageToolboxGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()
