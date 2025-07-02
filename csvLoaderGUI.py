import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

def csv_loader():
    """
    Creates a GUI for selecting and importing a .csv file.
    Returns the DataFrame if successful, None if cancelled or error occurs.
    """
    def select_file():
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv")]
        )
        if file_path:
            try:
                df = pd.read_csv(file_path)
                root.result = df
                root.quit()
                root.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read CSV file:\n{str(e)}")
        else:
            root.result = None
            root.quit()
            root.destroy()

    # Create the main window
    root = tk.Tk()
    root.title("Import CSV File")
    root.geometry("400x200")
    root.result = None  # Initialize result attribute
    
    # Create and pack the main frame
    frame = tk.Frame(root)
    frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    # Add instruction label
    label = tk.Label(
        frame,
        text="Please select a CSV file to import:",
        font=("Arial", 12)
    )
    label.pack(pady=20)
    
    # Add select file button
    select_button = tk.Button(
        frame,
        text="Select CSV File",
        command=select_file,
        font=("Arial", 10, "bold"),
        relief="raised"
    )
    select_button.pack(pady=10)
    
    # Add cancel button
    cancel_button = tk.Button(
        frame,
        text="Cancel",
        command=lambda: [setattr(root, 'result', None), root.destroy()],
        font=("Arial", 10, "bold"),
        relief="raised"
    )
    cancel_button.pack(pady=10)
    
    root.protocol("WM_DELETE_WINDOW", lambda: [setattr(root, 'result', None), root.destroy()])
    root.mainloop()
    
    return root.result

if __name__ == "__main__":
    df = csv_loader()
    if df is not None:
        print("CSV file successfully imported!")
        print("DataFrame shape:", df.shape)
        print("\nFirst few rows of the DataFrame:")
        print(df.head())
    else:
        print("No file selected or import failed.")