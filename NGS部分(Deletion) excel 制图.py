import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import os

# 读取 Excel 文件
df = pd.read_excel("/Users/jasontingting/Desktop/K3 部分結果/variant_summary.xlsx",sheet_name='Titer Deletion')
print(df.columns)

# 选择指定的数据行（第2到第47行）
selected_data = df[df['group 1'] == 1].copy()
# 创建一个包含需要处理的列名的列表
columns_to_plot = ['All mut/Total BC']  # 根据需要修改列名

# 设置保存图像的文件夹路径
output_folder = "/Users/jasontingting/Desktop/Titer_LNA_Graphs/"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 处理每一列
for column in columns_to_plot:
    # 确保去掉百分号并转换为浮动数值（如果是百分比数据）
    selected_data[column] = (
        selected_data[column]
        .astype(str)
        .str.replace('%', '', regex=False)  # 去掉百分号
        .apply(pd.to_numeric, errors='coerce')  # 转换为数值，遇到错误填充为 NaN
    )

    # 设置画布
    plt.figure(figsize=(8, 6))

    # 绘制柱状图
    barplot = sns.barplot(
        data=selected_data,
        x='Sample',
        y=column,
        hue='Types of chemical modifications',
        dodge=False,
        palette='pastel',
    )

    # 设置 Y 轴为百分比
    plt.ylabel(f'{column}', fontsize=12)

    # 百分比格式化
    def percent(x, _):
        return f'{x * 100:.1f}%'

    plt.gca().yaxis.set_major_formatter(FuncFormatter(percent))

    plt.ylim(0,0.01)
    # 设置字体大小
    plt.xticks(rotation=90, fontsize=14)
    plt.yticks(fontsize=14)
    plt.xlabel('')

    # 在每个柱子上面写上具体的百分比

    # 紧凑布局
    plt.tight_layout()

    # 保存为高分辨率 PNG 文件
    save_path = os.path.join(output_folder, f"LNA supF(0.4)_{column.replace('/', '_')}.png")
    plt.savefig(save_path, dpi=300)

    # 显示图像
    plt.show()