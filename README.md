# 高精地图全景影像显示工具-hdi2csv2shp

## 项目简介

这是一个用于处理高精地图全景影像（HDI）文件，并将其转换为 CSV 和 Shapefile 格式的工具。它提供了一个图形用户界面（GUI）和一个命令行接口，方便用户进行批处理操作，并支持自定义输出文件名和照片相对路径。

## 功能特性

- **HDI 文件批处理**: 自动扫描指定目录下的 HDI 文件并进行处理。
- **数据转换**: 将 HDI 数据转换为 CSV 格式，包含照片路径、经纬度、姿态角等信息。
- **Shapefile 生成**: 将处理后的数据生成 Shapefile，方便在 GIS 软件中进行可视化和分析。
- **GUI 界面**: 提供直观的用户界面，方便非技术用户操作。
- **命令行接口**: 支持命令行参数，方便集成到自动化流程中。
- **自定义输出**: 允许用户指定输出的 CSV 和 Shapefile 文件名。
- **相对路径处理**: 支持指定照片相对路径的基准路径。
- **无控制台窗口**: 打包后的 `.exe` 文件运行时不会弹出控制台窗口，提供更好的用户体验。

## 如何使用 GUI 应用程序

1. **下载可执行文件**: 从 [GitHub Releases](https://github.com/europewang/ch_script_high-precision_map_hdi2csv2shp/releases) 下载最新版本的 `高精地图全景影像显示工具-hdi2csv2shp.exe` 文件。
2. **运行程序**: 双击下载的 `.exe` 文件即可启动 GUI 应用程序。
3. **选择 HDI 文件夹**: 点击“选择 HDI 文件夹”按钮，选择包含 HDI 文件的根目录。
4. **选择照片基准路径**: 点击“选择照片基准路径”按钮，选择用于计算照片相对路径的基准目录（可选）。
5. **输入输出文件名**: 在“输出文件名”文本框中输入您希望生成的 CSV 和 Shapefile 的名称（例如：`output_data`）。
6. **开始处理**: 点击“开始处理”按钮，程序将开始处理 HDI 文件并生成相应的 CSV 和 Shapefile。
7. **查看日志**: 处理过程中的日志信息将显示在界面下方的文本框中。

## 如何使用命令行脚本

### 依赖安装

在运行命令行脚本之前，请确保您的 Python 环境中安装了以下库：

```bash
pip install pandas geopandas fiona shapely pyproj
```

### 脚本运行

您可以通过以下方式运行 `hdi_to_csv_processor.py` 脚本：

```bash
python hdi_to_csv_processor.py --input_dir <HDI文件根目录> --base_path <照片相对路径基准目录> --output_name <输出文件名>
```

**参数说明**：

- `--input_dir` (必填): 包含 HDI 文件的根目录。程序将递归搜索此目录下的所有 HDI 文件。
- `--base_path` (可选): 用于计算照片相对路径的基准目录。如果提供，照片路径将相对于此路径生成。
- `--output_name` (可选): 输出的 CSV 和 Shapefile 的文件名（不包含扩展名）。默认为 `merged_hdi_data`。

**示例**：

```bash
python hdi_to_csv_processor.py --input_dir "./全息路口" --base_path "./全息路口" --output_name "my_hdi_output"
```

## 开发与构建

### 环境设置

建议使用 `conda` 创建虚拟环境：

```bash
conda create -n hdi_processor_env python=3.9
conda activate hdi_processor_env
```

### 安装依赖

```bash
pip install -r requirements.txt
```

### 构建可执行文件

如果您想自己构建 `.exe` 文件，请确保已安装 `PyInstaller`：

```bash
pip install pyinstaller
```

然后，在项目根目录下运行以下命令：

```bash
pyinstaller --onefile --noconsole --name "高精地图全景影像显示工具-hdi2csv2shp" hdi_processor_gui.py
```

生成的 `.exe` 文件将在 `dist/` 目录下。

## 联系方式

如果您有任何问题或建议，请通过 [GitHub Issues](https://github.com/europewang/ch_script_high-precision_map_hdi2csv2shp/issues) 与我联系。