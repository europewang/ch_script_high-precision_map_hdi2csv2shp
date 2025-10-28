# 导入fiona库，用于读写Shapefile
import fiona
# 导入datetime模块中的date类，用于处理日期
from datetime import date
# 导入os模块，用于文件路径操作
import os
# 导入sys模块，用于访问系统相关参数和函数
import sys

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
        print(f"错误: 未找到输入Shapefile: {input_shp_path}")
        return

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
                print(f"警告: 'data'列类型为日期，但提供的值 '{data_value}' 不是有效的ISO日期格式。将使用原始字符串。")
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

    print(f"Shapefile已成功修改并保存到 {output_shp_path}")

# 当脚本作为主程序运行时
if __name__ == "__main__":
    # 检查命令行参数数量
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("用法: python modify_shp_data.py <输入Shapefile路径> <输出Shapefile路径> <自定义数据值> [编码(可选，默认为utf-8)]")
        print("示例: python modify_shp_data.py input.shp output.shp 2022-01-01")
        print("示例: python modify_shp_data.py input.shp output.shp 'Some Text' GBK")
        sys.exit(1)

    # 获取命令行参数中的输入和输出文件路径
    input_shp = sys.argv[1]
    output_shp = sys.argv[2]
    custom_data_value = sys.argv[3]
    
    encoding = 'utf-8'
    if len(sys.argv) == 5:
        encoding = sys.argv[4]

    # 调用函数修改Shapefile
    modify_shapefile(input_shp, output_shp, custom_data_value, encoding)
    print("请确保已安装'fiona'库 (pip install fiona).")