import tkinter as tk
from tkinter import filedialog, messagebox

class ImageToolboxGUI:
    def __init__(self, master):
        self.master = master
        master.title("ImageToolbox")

        # Configure the main window
        self.configure_gui()

        # Initialize GUI components
        self.create_widgets()

    def configure_gui(self):
        self.master.geometry("400x200")  # Set the window size

    def create_widgets(self):
        # Label
        self.label = tk.Label(self.master, text="Select a folder and process images:")
        self.label.pack(pady=10)

        # Folder path entry
        self.folder_path = tk.Entry(self.master, width=50)
        self.folder_path.pack(pady=5)

        # Browse button
        self.browse_button = tk.Button(self.master, text="Browse", command=self.browse_folder)
        self.browse_button.pack(pady=5)

        # Start button
        self.start_button = tk.Button(self.master, text="Start Processing", command=self.start_processing)
        self.start_button.pack(pady=10)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            # Display the selected directory in the folder path entry box
            self.folder_path.delete(0, tk.END)
            self.folder_path.insert(0, folder_selected)

    def start_processing(self):
        folder = self.folder_path.get()
        if not folder:
            messagebox.showinfo("Information", "Please select a folder first.")
            return
        
        # Here, you would integrate your image processing functionality
        # For demonstration, just show a message
        messagebox.showinfo("Processing", f"Images in {folder} would be processed now...")
        # You could replace the above line with a call to your image processing function

def run_app():
    root = tk.Tk()
    app = ImageToolboxGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()
