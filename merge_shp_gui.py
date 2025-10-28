# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog, messagebox
import fiona
import os

class MergeShapefileApp:
    def __init__(self, master):
        self.master = master
        master.title("合并shp快速工具")

        self.label_input_dir = tk.Label(master, text="输入目录 (可选):")
        self.label_input_dir.grid(row=0, column=0, sticky="w")
        self.entry_input_dir = tk.Entry(master, width=50)
        self.entry_input_dir.grid(row=0, column=1)
        self.button_browse_dir = tk.Button(master, text="浏览目录", command=self.browse_input_directory)
        self.button_browse_dir.grid(row=0, column=2)

        # Input Shapefile 1
        self.label_input1 = tk.Label(master, text="输入Shapefile 1 (可选):")
        self.label_input1.grid(row=1, column=0, sticky="w")
        self.entry_input1 = tk.Entry(master, width=50)
        self.entry_input1.grid(row=1, column=1)
        self.button_browse_input1 = tk.Button(master, text="浏览", command=self.browse_input_shp1)
        self.button_browse_input1.grid(row=1, column=2)

        # Input Shapefile 2
        self.label_input2 = tk.Label(master, text="输入Shapefile 2 (可选):")
        self.label_input2.grid(row=2, column=0, sticky="w")
        self.entry_input2 = tk.Entry(master, width=50)
        self.entry_input2.grid(row=2, column=1)
        self.button_browse_input2 = tk.Button(master, text="浏览", command=self.browse_input_shp2)
        self.button_browse_input2.grid(row=2, column=2)

        # Output Shapefile
        self.label_output = tk.Label(master, text="输出Shapefile:")
        self.label_output.grid(row=3, column=0, sticky="w")
        self.entry_output = tk.Entry(master, width=50)
        self.entry_output.grid(row=3, column=1)
        self.button_browse_output = tk.Button(master, text="浏览", command=self.browse_output_shp)
        self.button_browse_output.grid(row=3, column=2)

        # Merge Button
        self.button_merge = tk.Button(master, text="合并Shapefile", command=self.merge_shps)
        self.button_merge.grid(row=4, column=1, pady=10)

    def browse_input_directory(self):
        directory_path = filedialog.askdirectory()
        if directory_path:
            self.entry_input_dir.delete(0, tk.END)
            self.entry_input_dir.insert(0, directory_path)

    def browse_input_shp1(self):
        file_path = filedialog.askopenfilename(filetypes=[("Shapefiles", "*.shp")])
        if file_path:
            self.entry_input1.delete(0, tk.END)
            self.entry_input1.insert(0, file_path)

    def browse_input_shp2(self):
        file_path = filedialog.askopenfilename(filetypes=[("Shapefiles", "*.shp")])
        if file_path:
            self.entry_input2.delete(0, tk.END)
            self.entry_input2.insert(0, file_path)

    def browse_output_shp(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".shp", filetypes=[("Shapefiles", "*.shp")])
        if file_path:
            self.entry_output.delete(0, tk.END)
            self.entry_output.insert(0, file_path)

    def merge_shps(self):
        input_dir = self.entry_input_dir.get()
        input_shp1 = self.entry_input1.get()
        input_shp2 = self.entry_input2.get()
        output_shp = self.entry_output.get()

        input_shapefiles = []

        if input_dir:
            for root, _, files in os.walk(input_dir):
                for file in files:
                    if file.lower().endswith('.shp'):
                        input_shapefiles.append(os.path.join(root, file))
            if not input_shapefiles:
                messagebox.showerror("错误", "在指定目录中未找到任何Shapefile文件。")
                return
        else:
            if input_shp1: input_shapefiles.append(input_shp1)
            if input_shp2: input_shapefiles.append(input_shp2)

        if not input_shapefiles:
            messagebox.showerror("错误", "必须提供至少一个输入Shapefile或一个输入目录。")
            return

        if not output_shp:
            messagebox.showerror("错误", "必须提供输出Shapefile路径。")
            return

        try:
            self.merge_shapefiles(input_shapefiles, output_shp)
            messagebox.showinfo("成功", "Shapefile合并成功！")
        except FileNotFoundError as e:
            messagebox.showerror("错误", f"文件未找到: {e}")
        except ValueError as e:
            messagebox.showerror("错误", f"数据错误: {e}")
        except Exception as e:
            messagebox.showerror("发生意外错误", f"发生意外错误: {e}")

    def merge_shapefiles(self, input_shapefiles, output_shp):
        if not input_shapefiles:
            raise ValueError("没有提供输入Shapefile文件。")

        # 检查所有输入文件是否存在
        for shp_file in input_shapefiles:
            if not os.path.exists(shp_file):
                raise FileNotFoundError(f"输入Shapefile未找到: {shp_file}")

        # 打开第一个Shapefile以获取模式和CRS
        with fiona.open(input_shapefiles[0], 'r', encoding='utf-8') as first_source:
            schema = first_source.schema
            crs = first_source.crs

            # 创建输出Shapefile
            with fiona.open(
                output_shp,
                'w',
                driver=first_source.driver,
                crs=crs,
                schema=schema,
                encoding='utf-8'
            ) as sink:
                # 写入第一个Shapefile的特征
                for feature in first_source:
                    sink.write(feature)

                # 写入其余Shapefile的特征
                for i in range(1, len(input_shapefiles)):
                    with fiona.open(input_shapefiles[i], 'r', encoding='utf-8') as source:
                        if source.schema != schema:
                            raise ValueError(f"Shapefile模式不匹配: {input_shapefiles[i]}")
                        if source.crs != crs:
                            raise ValueError(f"Shapefile CRS不匹配: {input_shapefiles[i]}")
                        for feature in source:
                            sink.write(feature)

if __name__ == "__main__":
    root = tk.Tk()
    app = MergeShapefileApp(root)
    root.mainloop()