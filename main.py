import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar, Separator
import pandas as pd
import os
import re
import time

result_boxes = []
loading_bar = None
is_expanded = False  # Global variable to track the expansion state

def calculate_average_temperature(file_name):
    try:
        df = pd.read_csv(file_name)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%m/%d/%Y %I:%M:%S %p')
        df['Date'] = df['Timestamp'].dt.date
        averages = df.groupby('Date')['Temperature(Fahrenheit)'].mean().round(1)
        return averages
    except Exception as e:
        messagebox.showwarning("Error", f"Failed to process file.\n\nError: {str(e)}")
        return None

def extract_sensor_name_and_dates(file_name):
    pattern = r"MOCREO_ST4_(\w+)_\((\d{2}_\d{2}_\d{4}), (\d{2}_\d{2}_\d{4})\)_record"
    match = re.search(pattern, file_name)
    if match:
        sensor_name, date_from, date_to = match.group(1), match.group(2).replace('_', '/'), match.group(3).replace('_', '/')
        return sensor_name, date_from, date_to
    else:
        return None, None, None

def upload_csv():
    show_loading_bar()

    filenames = filedialog.askopenfilenames(filetypes=(("CSV Files", "*.csv"),))
    for filename in filenames:
        averages = calculate_average_temperature(filename)
        if averages is not None:
            # Get the file name without the extension
            file_name = os.path.splitext(os.path.basename(filename))[0]
            sensor_name, date_from, date_to = extract_sensor_name_and_dates(file_name)
            if sensor_name is not None and date_from is not None and date_to is not None:
                result = f"Sensor = {sensor_name}    Dates = {date_from} to {date_to}\n{averages.to_string()}"
                create_result_box(result)

    # Start a timer to stop the loading bar after 2 seconds
    root.after(100, stop_loading_bar)

def show_loading_bar():
    global loading_bar
    loading_bar = Progressbar(root, mode='determinate', cursor='watch')
    loading_bar.pack(pady=5)
    loading_bar.start()

def stop_loading_bar():
    if loading_bar is not None:
        loading_bar.stop()
        loading_bar.pack_forget()



def copy_results(txt_result):
    results = txt_result.get("1.0", tk.END)
    lines = results.strip().split('\n')
    formatted_results = [f"{data[0]}\t{data[1]}" for line in lines for data in [line.split()] if len(data) == 2]
    formatted_results = '\n'.join(formatted_results)
    root.clipboard_clear()
    root.clipboard_append(formatted_results)

def clear_results():
    global result_boxes
    for frame in result_boxes:
        frame.destroy()
    result_boxes = []

def remove_result_box(frame):
    frame.destroy()
    result_boxes.remove(frame)

def create_result_box(result):
    frame = tk.Frame(root, bd=1, relief=tk.RIDGE)
    frame.pack(pady=5)
    result_boxes.append(frame)

    remove_button = tk.Button(frame, text="X", fg="white", bg="red", activebackground="red", font=("Arial", 12, 'bold'), width=2, cursor='X_cursor', command=lambda: remove_result_box(frame))
    remove_button.pack(side=tk.LEFT, anchor=tk.CENTER, fill=tk.Y)

    #lines_frame = tk.Frame(frame, height=20, width=60, cursor='X_cursor')
    #lines_frame.pack(side=tk.LEFT, pady=5)

    #lines_symbol = tk.Label(lines_frame, text='☰ ☰ ☰↨', font=("Arial", 10), anchor=tk.W)
    #lines_symbol.pack(side=tk.LEFT, padx=5)

    txt_result = tk.Text(frame, wrap=tk.WORD, height=3, width=65)
    txt_result.insert(tk.END, result)

    # Bold formatting for the sensor name
    sensor_name_start = len("Sensor = ")
    sensor_name_end = result.index("    ")
    txt_result.tag_add("bold", f"1.{sensor_name_start}", f"1.{sensor_name_end}")
    txt_result.tag_config("bold", font=("Arial", 10, "bold"))

    txt_result.pack(side=tk.LEFT, padx=10)

    btn_copy = tk.Button(frame, text="← Copy Data", command=lambda: copy_results(txt_result), fg="white", bg="green", activebackground="green", font=("Helvetica", 12, 'bold'))
    btn_copy.pack(side=tk.LEFT, padx=10)

    # Configure text widget to handle tab characters
    txt_result.configure(tabs=("2c", "4c", "6c", "8c"))

def toggle_expansion():
    global is_expanded
    is_expanded = not is_expanded
    expansion_text = "Collapse All" if is_expanded else "Expand All"
    btn_expand.config(text=expansion_text)
    expand_content_boxes()

def expand_content_boxes():
    num_lines = 5 if is_expanded else 3
    for frame in result_boxes:
        txt_result = frame.children["!text"]
        txt_result.configure(height=num_lines)

def show_about():
    messagebox.showinfo("About", "Tempify - A CSV Processor for Arturo\nVersion 1.0\n\nOperation Stand Down Rhode Island\n       \"A Hand Up Not A Hand Out\"\n\n~OSDRI USE ONLY~\n\nCreated by Steve Tucker\nContact: stucker@osdri.org")

if __name__ == "__main__":
    root = tk.Tk()
    root.title('Tempify - A CSV Processor for OSDRI')
    root.geometry('800x950')  # width x height
    root.resizable(False, False)
    root.bind("<Escape>", lambda event: root.destroy())

    # Create the menu bar
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # Create the File dropdown menu
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Upload File", command=upload_csv)
    menubar.add_cascade(label="File", menu=file_menu)

    edit_menu = tk.Menu(menubar, tearoff=0)
    edit_menu.add_command(label="Clear All", command=clear_results)
    edit_menu.add_command(label="Toggle Expansion", command=toggle_expansion)
    menubar.add_cascade(label="Edit", menu=edit_menu)

    # Create the Help dropdown menu
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="How to Use")
    help_menu.add_command(label="About", command=show_about)
    menubar.add_cascade(label="Help", menu=help_menu)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=5)

    btn_upload = tk.Button(btn_frame, text="Load CSV(s)", command=upload_csv, fg="white", bg="blue", activebackground="blue", font=("Arial", 16, 'bold'), height=2, width=15)
    btn_upload.configure(cursor='crosshair')
    btn_upload.pack(side=tk.LEFT, padx=5)

    btn_clear = tk.Button(btn_frame, text="Clear All", command=clear_results, fg="white", bg="red", activebackground="red", font=("Arial", 16, 'bold'), height=2, width=15)
    btn_clear.configure(cursor='X_cursor')
    btn_clear.pack(side=tk.LEFT, padx=5)

    btn_expand = tk.Button(btn_frame, text="Expand All", command=toggle_expansion, fg="white", bg="green", activebackground="green", font=("Arial", 12, 'bold'))
    btn_expand.pack(side=tk.LEFT, padx=5)

    lbl_max_size = tk.Label(root, text="Max Size: 12 Unexpanded, 8 Expanded", font=("Arial", 12, 'bold'))
    lbl_max_size.pack(anchor=tk.N, padx=10, pady=10)    

    separator = Separator(root, orient=tk.HORIZONTAL)
    separator.pack(fill=tk.X, padx=10, pady=10)

    root.mainloop()
