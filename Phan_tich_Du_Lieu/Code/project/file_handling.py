import os
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

file_name_global = ""
folder_name = ""

def input_file():
    """Select input file through GUI."""
    def submit():
        global file_name_global
        file_name = filedialog.askopenfilename(
            title="Select a File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not file_name:
            messagebox.showerror("Error", "File name cannot be empty")
        else:
            messagebox.showinfo("Input", f'The file name you entered is: {file_name}')
            file_name_global = file_name
            root.destroy()

    root = tk.Tk()
    root.title("Dự án nhóm 3")
    image_path = r'D:\Game\Du_An\Phan_tich_Du_Lieu\Code\project\PTIT_logo.png'
    img = Image.open(image_path)
    img = img.resize((200, 200))
    photo = ImageTk.PhotoImage(img)
    image_label = tk.Label(root, image=photo)
    image_label.pack(padx=20, pady=10)
    label = tk.Label(root, text="Vui lòng chọn file:")
    label.pack(padx=20, pady=10)
    button = tk.Button(root, text="Chọn file", command=submit)
    button.pack(padx=20, pady=20)
    root.mainloop()

def get_base_path():
    return r"D:\Game\Du_An\Phan_tich_Du_Lieu"

def new_folder():
    """Create a new folder for output."""
    global folder_name
    folder_name = "Sales_Report"
    folder = os.path.join(get_base_path(), folder_name)
    if not os.path.exists(folder):
        os.makedirs(folder)

def combine_csv_files(path):
    """Combine all CSV files into a single DataFrame."""
    import pandas as pd
    frames = []
    for file in os.listdir(path):
        if file.endswith('.csv'):
            filepath = os.path.join(path, file)
            df = pd.read_csv(filepath)
            frames.append(df)
    folder = os.path.join(get_base_path(), folder_name)
    output_file = os.path.join(folder, 'annualSales2019.csv')
    data = pd.concat(frames)
    data.to_csv(output_file, index=False)
    return data
