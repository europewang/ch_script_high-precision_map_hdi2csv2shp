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

1.  **下载可执行文件**: 从 [GitHub Releases](https://github.com/europewang/ch_script_high-precision_map_hdi2csv2shp/releases) 下载最新版本的 `高精地图全景影像显示工具-hdi2csv2shp.exe` 文件。
2.  **运行程序**: 双击下载的 `.exe` 文件即可启动 GUI 应用程序。
3.  **选择 HDI 文件夹**: 点击“选择 HDI 文件夹”按钮，选择包含 HDI 文件的根目录。
4.  **选择照片基准路径**: 点击“选择照片基准路径”按钮，选择用于计算照片相对路径的基准目录（可选）。
5.  **输入输出文件名**: 在“输出文件名”文本框中输入您希望生成的 CSV 和 Shapefile 的名称（例如：`output_data`）。
6.  **开始处理**: 点击“开始处理”按钮，程序将开始处理 HDI 文件并生成相应的 CSV 和 Shapefile。
7.  **查看日志**: 处理过程中的日志信息将显示在界面下方的文本框中。

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

## SHP 数据修改工具 (modify_shp_gui.py)

### 项目简介

这是一个用于修改 Shapefile (SHP) 文件中指定字段数据的工具。它提供了一个图形用户界面（GUI），方便用户选择 SHP 文件，指定要修改的字段，并输入新的值。

### 如何使用 GUI 应用程序

1.  **下载可执行文件**: 如果您已自行打包，可以在 `dist/` 目录下找到 `修改shp数据快速工具.exe`。
2.  **运行程序**: 双击下载的 `.exe` 文件即可启动 GUI 应用程序。
3.  **选择 SHP 文件**: 点击“选择 SHP 文件”按钮，选择您要修改的 Shapefile 文件。
4.  **输入字段名**: 在“要修改的字段名”文本框中输入您要修改的字段的名称。
5.  **输入新值**: 在“新值”文本框中输入您希望该字段更新为的新值。
6.  **开始修改**: 点击“开始修改”按钮，程序将修改指定 SHP 文件中所有记录的指定字段为新值。
7.  **查看结果**: 修改成功后，会弹出提示框。

### 构建可执行文件

如果您想自己构建 `.exe` 文件，请确保已安装 `PyInstaller`，并在项目根目录下运行以下命令：

```bash
pyinstaller --onefile --noconsole --name "修改shp数据快速工具" modify_shp_gui.py
```

生成的 `.exe` 文件将在 `dist/` 目录下。

## SHP 文件合并工具 (merge_shp_gui.py)

### 项目简介

这是一个用于合并多个 Shapefile (SHP) 文件的工具。它提供了一个图形用户界面（GUI），支持选择单个 SHP 文件或选择一个目录来合并该目录下所有的 SHP 文件。工具会自动检查待合并文件的字段结构和坐标系，并处理中文编码。

### 如何使用 GUI 应用程序

1.  **下载可执行文件**: 如果您已自行打包，可以在 `dist/` 目录下找到 `合并shp快速工具.exe`。
2.  **运行程序**: 双击下载的 `.exe` 文件即可启动 GUI 应用程序。
3.  **选择输入方式**:
    *   **选择单个 SHP 文件**: 点击“选择 SHP 文件”按钮，选择您要合并的第一个 Shapefile 文件。您可以重复此步骤选择多个文件。
    *   **选择输入目录 (可选)**: 点击“浏览目录”按钮，选择一个包含多个 SHP 文件的目录。程序将自动查找该目录下所有 `.shp` 文件进行合并。
        *   **注意**: 如果同时选择了单个 SHP 文件和输入目录，程序将优先合并输入目录中的所有 SHP 文件。
4.  **输入输出文件路径**: 在“输出文件路径”文本框中输入您希望合并后的 Shapefile 的保存路径和文件名（例如：`./merged_output.shp`）。
5.  **开始合并**: 点击“开始合并”按钮，程序将开始合并选定的 SHP 文件或目录中的所有 SHP 文件。
6.  **查看结果**: 合并成功后，会弹出提示框。如果合并过程中出现字段不一致或坐标系不匹配等问题，也会有相应的错误提示。

### 构建可执行文件

如果您想自己构建 `.exe` 文件，请确保已安装 `PyInstaller`，并在项目根目录下运行以下命令：

```bash
pyinstaller --onefile --noconsole --name "合并shp快速工具" merge_shp_gui.py
```

生成的 `.exe` 文件将在 `dist/` 目录下。

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