import os
import csv
import re
from osgeo import ogr, osr, gdal
import argparse

def process_hdi_to_csv(hdi_file_path, base_path_for_photos):
    """
    处理单个HDI文件，提取指定列，并将其保存为新的CSV文件。
    
    Args:
        hdi_file_path (str): HDI文件的完整路径。
    """
    # 构建输出CSV文件的路径，将HDI文件的扩展名替换为.csv
    output_csv_file_path = os.path.splitext(hdi_file_path)[0] + ".csv"

    # 获取HDI文件所在的目录
    hdi_dir = os.path.dirname(hdi_file_path)
    # 构建CCD文件夹的路径
    ccd_dir = os.path.join(hdi_dir, 'CCD')

    photo_names = []
    if os.path.isdir(ccd_dir):
        # 获取CCD文件夹下所有JPG文件的名称并排序
        for filename in sorted(os.listdir(ccd_dir)):
            if filename.lower().endswith('.jpg'):
                photo_names.append(filename)
    else:
        print(f"警告: 未找到与HDI文件 {hdi_file_path} 同级的CCD文件夹。")

    photo_index = 0
    photo_count_warning_issued = False # 添加标志，用于控制警告只输出一次

    # 获取HDI文件父目录的名称
    parent_dir_name = os.path.basename(hdi_dir)
    # 尝试从父目录名称中提取括号内的中文内容
    match = re.search(r'[\(（](.*?)[\)）]', parent_dir_name)
    third_column_data = match.group(1) if match else ''

    processed_rows = []

    # 以读取模式打开HDI文件
    with open(hdi_file_path, 'r') as infile:
        # 创建CSV读取器，指定制表符为分隔符
        reader = csv.reader(infile, delimiter='\t')

        # 遍历HDI文件中的每一行
        for row in reader:
            # 确保行有足够的列，以避免索引错误
            if len(row) >= 15:
                # 提取第12、13、14、15列（0-indexed: 11, 12, 13, 14）
                # 提取第12, 13, 14, 15列数据 (H, B, L, HEADING)
                # 调整为 B, L, H, HEADING 的顺序
                extracted_data = [row[13], row[12], row[11], row[14]]

                current_photo_name = ''
                current_photo_relative_path = ''

                if photo_index < len(photo_names):
                    current_photo_name = photo_names[photo_index]
                    full_photo_path = os.path.join(ccd_dir, current_photo_name)
                    
                    # 计算相对于 E:\Code 的路径
                    base_path = base_path_for_photos
                    try:
                        current_photo_relative_path = os.path.relpath(full_photo_path, base_path)
                    except ValueError:
                        print(f"警告: 无法计算照片 {full_photo_path} 相对于 {base_path} 的路径。")
                        current_photo_relative_path = full_photo_path # Fallback to full path

                    photo_index += 1
                else:
                    if not photo_count_warning_issued:
                        print(f"警告: HDI文件 {hdi_file_path} 的行数多于CCD文件夹中的照片数量。")
                        photo_count_warning_issued = True

                # 创建一个新行，前两列为照片名称和相对路径，第三列为提取的中文内容，后面跟着提取的数据
                new_row = [current_photo_name, current_photo_relative_path, third_column_data] + extracted_data
                processed_rows.append(new_row)
            else:
                # 如果行中的列数不足，则打印警告信息并跳过该行
                print(f"警告: 文件 {hdi_file_path} 中由于列数不足跳过行: {row}")
    return processed_rows

def batch_process_hdi_files(directory_path, base_path_for_photos):
    """
    批量处理给定目录中的所有HDI文件。
    
    Args:
        directory_path (str): 包含HDI文件的目录路径。
    """
    all_processed_data = []
    for root, _, files in os.walk(directory_path):
        for filename in files:
            # 检查文件是否以.hdi结尾
            if filename.endswith(".hdi"):
                # 构建HDI文件的完整路径
                hdi_file_path = os.path.join(root, filename)
                # 处理单个HDI文件并收集返回的行
                all_processed_data.extend(process_hdi_to_csv(hdi_file_path, base_path_for_photos))
    return all_processed_data

def convert_csv_to_shp(csv_file_path, shp_file_path):
    """
    将CSV文件转换为ESRI Shapefile。
    CSV文件应包含标题行：FILE_NAME, FILE_PATH, ROAD_NAME, H, B, L, HEADING
    其中B为纬度，L为经度，使用WGS84地理坐标系。
    
    Args:
        csv_file_path (str): 输入CSV文件的路径。
        shp_file_path (str): 输出Shapefile的路径。
    """
    # 注册所有OGR驱动
    gdal.AllRegister()

    # 获取ESRI Shapefile驱动
    driver = ogr.GetDriverByName("ESRI Shapefile")

    # 创建数据源
    if os.path.exists(shp_file_path):
        driver.DeleteDataSource(shp_file_path)
    data_source = driver.CreateDataSource(shp_file_path)

    # 定义WGS84坐标系
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(4326) # WGS84

    # 创建图层
    layer = data_source.CreateLayer("hdi_points", srs, ogr.wkbPoint, options=['ENCODING=UTF-8'])

    # 定义字段
    layer.CreateField(ogr.FieldDefn("FILE_NAME", ogr.OFTString))
    layer.CreateField(ogr.FieldDefn("FILE_PATH", ogr.OFTString))
    layer.CreateField(ogr.FieldDefn("ROAD_NAME", ogr.OFTString))
    layer.CreateField(ogr.FieldDefn("B", ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn("L", ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn("H", ogr.OFTReal))
    layer.CreateField(ogr.FieldDefn("HEADING", ogr.OFTReal))

    # 从CSV读取数据并写入Shapefile
    with open(csv_file_path, 'r', encoding='gbk') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader) # 跳过标题行

        for row in reader:
            # 创建要素
            feature = ogr.Feature(layer.GetLayerDefn())
            feature.SetField("FILE_NAME", row[0])
            feature.SetField("FILE_PATH", row[1])
            feature.SetField("ROAD_NAME", row[2])
            feature.SetField("B", float(row[3]))
            feature.SetField("L", float(row[4]))
            feature.SetField("H", float(row[5]))
            feature.SetField("HEADING", float(row[6]))

            # 创建点几何
            point = ogr.Geometry(ogr.wkbPoint)
            point.SetPoint(0, float(row[4]), float(row[3])) # 经度, 纬度 (L, B)
            feature.SetGeometry(point)

            # 将要素写入图层
            layer.CreateFeature(feature)

            # 销毁要素
            feature = None

    # 销毁数据源
    data_source = None
    print(f"Shapefile已成功创建: {shp_file_path}")

def run_hdi_processing(input_dir, base_path_for_photos, output_file_name):
    # 批量处理当前目录中的所有HDI文件，并收集所有处理后的数据
    final_data = batch_process_hdi_files(input_dir, base_path_for_photos)

    # 在脚本同级目录下创建最终的合并CSV文件
    output_csv_file = os.path.join(input_dir, f"{output_file_name}.csv")
    with open(output_csv_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        # 写入标题行
        writer.writerow(['FILE_NAME', 'FILE_PATH', 'ROAD_NAME', 'B', 'L', 'H', 'HEADING'])
        # 写入所有收集到的数据
        writer.writerows(final_data)
    print(f"所有HDI文件的数据已合并到 {output_csv_file}")

    # 第二步：将CSV文件转换为Shapefile
    convert_csv_to_shp(output_csv_file, os.path.join(input_dir, f"{output_file_name}.shp"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process HDI files and convert to CSV and Shapefile.")
    parser.add_argument('--input_dir', type=str, default=os.getcwd(),
                        help='要处理的HDI文件所在的目录。默认为当前工作目录。')
    parser.add_argument('--base_path', type=str, default=r'E:\Code',
                        help='计算照片相对路径的基准路径。默认为 E:\\Code。')
    parser.add_argument('--output_name', type=str, default='merged_hdi_data',
                        help='输出CSV和Shapefile文件的名称（不包含扩展名）。默认为 merged_hdi_data。')
    args = parser.parse_args()

    run_hdi_processing(args.input_dir, args.base_path, args.output_name)