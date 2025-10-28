# GUI application for modifying Shapefile data

import fiona
from datetime import date
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

def modify_shapefile(input_shp_path, output_shp_path, data_value, encoding='utf-8'):
    """
    通过添加或更新'data'列，并将其值设置为指定值来修改Shapefile。

    参数:
        input_shp_path (str): 输入Shapefile的路径。
        output_shp_path (str): 输出（修改后）Shapefile的路径。
        data_value (str): 要设置到'data'列的自定义值。
        encoding (str): Shapefile的字符编码，默认为'utf-8'。
    """
    # 检查输入Shapefile是否存在
    if not os.path.exists(input_shp_path):
        raise FileNotFoundError(f"未找到输入Shapefile: {input_shp_path}")

    warning_message = None
    # 以只读模式打开源Shapefile
    with fiona.open(input_shp_path, 'r', encoding=encoding) as source:
        # 获取原始的schema（结构信息）
        schema = source.schema.copy()
        driver = source.driver
        crs = source.crs

        # 检查是否存在'data'列
        data_column_exists = False
        data_column_name = None
        for prop_name in schema['properties']:
            # 不区分大小写检查'data'列
            if prop_name.lower() == 'data':
                data_column_exists = True
                data_column_name = prop_name # 保留原始列名的大小写
                break

        # 如果'data'列不存在，则添加到schema中
        if not data_column_exists:
            # 尝试根据data_value的格式推断类型，或者默认为string
            try:
                # 尝试将data_value解析为日期
                date.fromisoformat(data_value) # 检查是否是有效的ISO日期格式
                schema['properties']['data'] = 'date'
            except ValueError:
                # 如果不是日期格式，则默认为字符串
                schema['properties']['data'] = 'str'
            data_column_name = 'data' # 使用'data'作为新列名

        # 将自定义值赋给target_value
        target_value = data_value
        if schema['properties'].get(data_column_name) == 'date':
            try:
                target_value = date.fromisoformat(data_value)
            except ValueError:
                warning_message = f"'data'列类型为日期，但提供的值 '{data_value}' 不是有效的ISO日期格式。将使用原始字符串。"
                target_value = data_value

        # 将修改后的要素写入新的Shapefile
        with fiona.open(
            output_shp_path,
            'w',
            driver=driver,
            crs=crs,
            schema=schema,
            encoding=encoding # 添加编码参数
        ) as sink:
            for feature in source:
                # 更新或添加'data'属性
                feature['properties'][data_column_name] = target_value
                sink.write(feature)

    return True, warning_message


class ShapefileModifierApp:
    def __init__(self, master):
        self.master = master
        master.title("Shapefile Modifier")

        # Input Shapefile
        self.label_input = tk.Label(master, text="Input Shapefile:")
        self.label_input.grid(row=0, column=0, sticky="w")
        self.entry_input = tk.Entry(master, width=50)
        self.entry_input.grid(row=0, column=1)
        self.button_browse_input = tk.Button(master, text="Browse", command=self.browse_input_shp)
        self.button_browse_input.grid(row=0, column=2)

        # Output Shapefile
        self.label_output = tk.Label(master, text="Output Shapefile:")
        self.label_output.grid(row=1, column=0, sticky="w")
        self.entry_output = tk.Entry(master, width=50)
        self.entry_output.grid(row=1, column=1)
        self.button_browse_output = tk.Button(master, text="Browse", command=self.browse_output_shp)
        self.button_browse_output.grid(row=1, column=2)

        # Custom Data Value
        self.label_data_value = tk.Label(master, text="Custom Data Value:")
        self.label_data_value.grid(row=2, column=0, sticky="w")
        self.entry_data_value = tk.Entry(master, width=50)
        self.entry_data_value.grid(row=2, column=1)
        self.entry_data_value.insert(0, "2023-01-01") # Default value

        # Encoding
        self.label_encoding = tk.Label(master, text="Encoding:")
        self.label_encoding.grid(row=3, column=0, sticky="w")
        self.entry_encoding = tk.Entry(master, width=50)
        self.entry_encoding.grid(row=3, column=1)
        self.entry_encoding.insert(0, "utf-8") # Default value

        # Modify Button
        self.button_modify = tk.Button(master, text="Modify Shapefile", command=self.modify_shp)
        self.button_modify.grid(row=4, column=1, pady=10)

    def browse_input_shp(self):
        file_path = filedialog.askopenfilename(filetypes=[("Shapefiles", "*.shp")])
        if file_path:
            self.entry_input.delete(0, tk.END)
            self.entry_input.insert(0, file_path)

    def browse_output_shp(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".shp", filetypes=[("Shapefiles", "*.shp")])
        if file_path:
            self.entry_output.delete(0, tk.END)
            self.entry_output.insert(0, file_path)

    def modify_shp(self):
        input_shp = self.entry_input.get()
        output_shp = self.entry_output.get()
        data_value = self.entry_data_value.get()
        encoding = self.entry_encoding.get()

        if not input_shp or not output_shp or not data_value:
            messagebox.showerror("错误", "所有字段都必须填写！")
            return

        try:
            success, warning_message = modify_shapefile(input_shp, output_shp, data_value, encoding)
            if success:
                if warning_message:
                    messagebox.showwarning("警告", warning_message)
                messagebox.showinfo("成功", f"Shapefile已成功修改并保存到 {output_shp}")
        except FileNotFoundError as e:
            messagebox.showerror("错误", str(e))
        except Exception as e:
            messagebox.showerror("错误", f"发生错误: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShapefileModifierApp(root)
    root.mainloop()