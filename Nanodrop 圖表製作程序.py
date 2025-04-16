import pandas as pd
import matplotlib.pyplot as plt
import os

# 輸入 Excel 文件名稱
input_file ="/Users/jasontingting/Desktop/Nanodrop/2024-12-16 K1-K4 Lib 部分 NGS PCR 精製/20241216 143-185 精製 図表作製明細.xlsx"
output_folder ="/Users/jasontingting/Desktop/Nanodrop/2024-12-16 K1-K4 Lib 部分 NGS PCR 精製/折線圖保存"  # 保存圖表的資料夾

# 創建輸出資料夾（若不存在）
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 讀取 Excel 檔案，獲取所有工作表
xls = pd.ExcelFile(input_file)
sheet_names = xls.sheet_names  # 所有工作表名稱

# 遍歷所有工作表，生成圖表
for sheet in sheet_names:
    # 讀取當前工作表數據
    df = pd.read_excel(input_file, sheet_name=sheet)
    
    # 假設數據格式：第一列是波長，第二列是吸光度
    wavelength = df.iloc[:, 0]  # 第一列數據
    absorbance = df.iloc[:, 1]  # 第二列數據
    
    # 繪製折線圖
    plt.figure(figsize=(8, 5))  # 圖片大小
    plt.plot(wavelength, absorbance, color="blue", linewidth=2)
    plt.xlabel("Wavelength (nm)", fontsize=12)  # x 軸標籤
    plt.ylabel("Absorbance", fontsize=12)       # y 軸標籤
    plt.grid(False)  # 不顯示網格
    plt.tight_layout()  # 自動調整布局
    
    # 保存圖表為 PNG 格式，文件名為工作表名稱
    output_path = os.path.join(output_folder, f"{sheet}.png")
    plt.savefig(output_path, format="png", dpi=300)
    plt.close()  # 關閉當前圖表，防止重疊

print(f"所有圖表已保存至資料夾: {output_folder}")