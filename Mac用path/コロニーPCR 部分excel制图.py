import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import os

# 读取 Excel 文件
df = pd.read_excel("/Users/jasontingting/Desktop/K3 部分結果/variant_summary.xlsx",sheet_name="まとめ")
print(df.columns)

# 选择指定的数据行（第2到第47行）
selected_data = df[df['Types of Modifications'] == 1].copy()

# 创建一个包含需要处理的列名的列表
columns_to_plot = ['PCR (Deletion)(NGS Primer)(266 bp)(%)','PCR (Deletion)(Da607/Da614)1317 bp +(NGS Primer)266 bp(%)','PCR (insertion)(NGS Primer)266 bp(%)','PCR (insertion)(Da607/Da614) 1317 bp +(NGS Primer) 266 bp(%)']  # 根据需要修改列名

# 设置保存图像的文件夹路径
output_folder = "/Users/jasontingting/Desktop/コロニーPCR_Graphs/"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 处理每一列
for column in columns_to_plot:
    # 将百分比字符串转换为浮点数并除以100（如果是百分比数据）
    selected_data.loc[:, column] = (
        selected_data[column]
        .astype(str)
        .str.replace('%', '', regex=False)
        .astype(float)
    )

    # 设置画布
    plt.figure(figsize=(10, 6))

    # 绘制柱状图
    barplot = sns.barplot(
        data=selected_data,
        x='PCR Sample',
        y=column,
        hue='PCR Sample',
        dodge=False,
        palette='Set2',
        legend=False,
    )

    # 设置 Y 轴为百分比
    plt.ylabel(f'{column}', fontsize=12)

    # 百分比格式化
    def percent(x, _):
        return f'{x * 100:.0f}%'

    plt.gca().yaxis.set_major_formatter(FuncFormatter(percent))

    # 设置 Y 轴上限为 35%
    plt.ylim(0, 0.35)

    # 设置字体大小
    plt.xticks(rotation=0, fontsize=18)
    plt.yticks(fontsize=18)
    plt.xlabel('')

    # 在每个柱子上面写上具体的百分比
    for p in barplot.patches:
        height = p.get_height()
        barplot.text(
            p.get_x() + p.get_width() / 2,  # x 坐标
            height + 0.01,  # y 坐标（稍微高于柱子）
            f'{height * 100:.0f}%',  # 显示的文本（百分比）
            ha='center',  # 水平对齐
            va='bottom',  # 垂直对齐
            fontsize=18,  # 字体大小
            color='black',  # 字体颜色
            fontweight='bold'
        )

    # 紧凑布局
    plt.tight_layout()

    # 保存为高分辨率 PNG 文件
    save_path = os.path.join(output_folder, f"E1LNA_{column.replace('/', '_')}.png")
    plt.savefig(save_path, dpi=300)

    # 显示图像
    plt.show()