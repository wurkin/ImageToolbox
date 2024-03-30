import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter.ttk import Progressbar
import threading
from app.image_processor import batch_convert_raw_to_jpeg
import logging
from app.utils import setup_logging

class ImageToolboxGUI:
    def __init__(self, master):
        self.master = master
        master.title("ImageToolbox")

        self.configure_gui()
        self.create_widgets()
        setup_logging()

    def configure_gui(self):
        self.master.geometry("600x400")  # Adjust window size as needed

    def create_widgets(self):
        # Input and Output Directory Selection
        self.create_directory_widgets()
        
        # Progress Bar
        self.progress = Progressbar(self.master, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress.pack(pady=20)

        # Log Viewer
        self.log_viewer = scrolledtext.ScrolledText(self.master, height=10)
        self.log_viewer.pack(pady=10)
        self.log_viewer.configure(state ='disabled')

        # Start Processing Button
        self.start_button = tk.Button(self.master, text="Start Processing", command=self.start_processing)
        self.start_button.pack(pady=10)

    def create_directory_widgets(self):
        # Similar to previous implementation, define here your directory widgets (input/output)
        pass

    def browse_input_folder(self):
        # Your existing implementation
        pass

    def browse_output_folder(self):
        # Your existing implementation
        pass

    def update_progress(self, progress, error=None):
        # Safe way to update progress bar from different thread
        self.progress['value'] = progress
        if error:
            self.log(f"Error: {error}")
    
    def log(self, message):
        # Safe way to update log viewer from different thread
        self.log_viewer.configure(state='normal')
        self.log_viewer.insert(tk.END, message + "\n")
        self.log_viewer.configure(state='disabled')
        self.log_viewer.yview(tk.END)

    def start_processing(self):
        input_dir = self.input_dir_path.get()
        output_dir = self.output_dir_path.get()
        if not input_dir or not output_dir:
            messagebox.showinfo("Information", "Please select both input and output folders.")
            return

        # Disable the start button to prevent multiple clicks
        self.start_button.config(state='disabled')

        # Start the image processing in a separate thread
        threading.Thread(target=self.process_images, args=(input_dir, output_dir), daemon=True).start()

    def process_images(self, input_dir, output_dir):
        def callback(progress, error=None):
            # Use 'after' to schedule the update_progress call in the main GUI thread
            self.master.after(100, self.update_progress, progress, error)

        batch_convert_raw_to_jpeg(input_dir, output_dir, progress_callback=callback)

        # Re-enable the start button after processing is complete
        self.start_button.config(state='normal')
        self.log("Processing completed.")

def run_app():
    root = tk.Tk()
    app = ImageToolboxGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()
