

import tkinter as tk
from tkinter import filedialog, messagebox  
import re                                   
import os                                   

def select_files_and_generate():

    file_paths = filedialog.askopenfilenames(
        title="Select Python File(s)",
        filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
    )
    
    if not file_paths:
        return

    modules = set()  
    
    for file_path in file_paths:
        try:
            with open(file_path, "r") as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file:\n{file_path}\n{e}")
            continue
        
        import_pattern = re.compile(r'^\s*(import|from)\s+([a-zA-Z0-9_]+)', re.MULTILINE)
        matches = import_pattern.findall(content)
        
        for match in matches:
            modules.add(match[1])
    
    modules_list = sorted(modules)
    
    output_directory = filedialog.askdirectory(title="Select Output Directory for requirements.txt")
    if not output_directory:
        return
    
    req_file_path = os.path.join(output_directory, "requirements.txt")
    
    if len(file_paths) == 1:
        header = f"# These are the dependencies for one file: {os.path.basename(file_paths[0])}"
    else:
        file_names = ", ".join(os.path.basename(f) for f in file_paths)
        header = f"# These are the dependencies for multiple files: {file_names}"
    
    try:
        with open(req_file_path, "w") as req_file:
            req_file.write(header + "\n\n")
            for module in modules_list:
                req_file.write(module + "\n")
        messagebox.showinfo("Success", f"'requirements.txt' generated at:\n{req_file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not write requirements.txt:\n{e}")


root = tk.Tk()
root.title("Requirements Generator")

button = tk.Button(
    root,
    text="Select Python File(s) and Generate requirements.txt",
    command=select_files_and_generate
)
button.pack(pady=20, padx=20)

root.mainloop()
