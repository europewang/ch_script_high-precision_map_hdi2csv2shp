import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys

# 确保可以导入 hdi_to_csv_processor.py
# 如果 hdi_to_csv_processor.py 不在当前目录，需要调整 sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hdi_to_csv_processor import run_hdi_processing

class HDIProcessorGUI:
    def __init__(self, master):
        self.master = master
        master.title("高精地图全景影像显示工具-hdi2csv2shp")

        # Input Directory
        self.label_input_dir = tk.Label(master, text="HDI 文件目录:")
        self.label_input_dir.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_input_dir = tk.Entry(master, width=50)
        self.entry_input_dir.grid(row=0, column=1, padx=5, pady=5)
        self.button_browse_input = tk.Button(master, text="浏览", command=self.browse_input_dir)
        self.button_browse_input.grid(row=0, column=2, padx=5, pady=5)

        # Base Path
        self.label_base_path = tk.Label(master, text="照片相对路径基准:")
        self.label_base_path.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_base_path = tk.Entry(master, width=50)
        self.entry_base_path.insert(0, r"E:\Code") # Default value
        self.entry_base_path.grid(row=1, column=1, padx=5, pady=5)
        self.button_browse_base = tk.Button(master, text="浏览", command=self.browse_base_path)
        self.button_browse_base.grid(row=1, column=2, padx=5, pady=5)

        # Output Name
        self.label_output_name = tk.Label(master, text="输出文件名称:")
        self.label_output_name.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_output_name = tk.Entry(master, width=50)
        self.entry_output_name.insert(0, "merged_hdi_data") # Default value
        self.entry_output_name.grid(row=2, column=1, padx=5, pady=5)

        # Process Button
        self.button_process = tk.Button(master, text="开始处理", command=self.process_files)
        self.button_process.grid(row=3, column=0, columnspan=3, pady=10)

        # Log Output
        self.log_text = tk.Text(master, height=10, width=70)
        self.log_text.grid(row=4, column=0, columnspan=3, padx=5, pady=5)
        self.log_text.config(state=tk.DISABLED) # Make it read-only

    def browse_input_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.entry_input_dir.delete(0, tk.END)
            self.entry_input_dir.insert(0, directory)

    def browse_base_path(self):
        directory = filedialog.askdirectory()
        if directory:
            self.entry_base_path.delete(0, tk.END)
            self.entry_base_path.insert(0, directory)

    def log_message(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END) # Scroll to the end
        self.log_text.config(state=tk.DISABLED)

    def process_files(self):
        input_dir = self.entry_input_dir.get()
        base_path = self.entry_base_path.get()
        output_name = self.entry_output_name.get()

        if not input_dir:
            messagebox.showerror("错误", "请选择 HDI 文件目录！")
            return

        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.log_message("开始处理...")

        try:
            # Redirect stdout to capture print statements
            old_stdout = sys.stdout
            sys.stdout = TextRedirector(self.log_text, "stdout")

            run_hdi_processing(input_dir, base_path, output_name)
            self.log_message("处理完成！")
            messagebox.showinfo("完成", "文件处理成功完成！")
        except Exception as e:
            self.log_message(f"处理失败: {e}")
            messagebox.showerror("错误", f"文件处理失败: {e}")
        finally:
            sys.stdout = old_stdout # Restore stdout

# Custom class to redirect stdout to tkinter Text widget
class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.config(state=tk.NORMAL)
        self.widget.insert(tk.END, str, (self.tag,))
        self.widget.see(tk.END)
        self.widget.config(state=tk.DISABLED)

    def flush(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = HDIProcessorGUI(root)
    root.mainloop()