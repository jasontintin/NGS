import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter

# 读取 Excel 文件中的 'Titer Deletion' 工作表
file_path = "/Users/jasontingting/Desktop/K3 部分結果/variant_summary_supF.xlsx"
df = pd.read_excel(file_path, sheet_name='Sel')

# 根据 'group 2' 筛选数据
selected_data = df[df['group2'].astype(str).str.contains('1')].copy()
print(df.columns.tolist())
# 只选择需要的列
columns_to_use = ['Sample4','Del_mutant frequency_0.6_Average','Ins_mutant frequency_0.6_Average','SNV_mutant frequency_0.6_Average']
filtered_data = selected_data[columns_to_use].copy()

# 去除百分号并转换为数值
for col in columns_to_use[1:3]:
    filtered_data[col] = (
        filtered_data[col]
        .astype(str)
        .str.replace('%', '', regex=False)
        .apply(pd.to_numeric, errors='coerce')
    )

# 转换为长格式
melted_data = pd.melt(
    filtered_data,
    id_vars=['Sample4'],
    var_name='Measurement',
    value_name='Value'
)

# 设置绘图风格
plt.figure(figsize=(20,8))
sns.set(style="whitegrid")

# 创建分组柱状图
barplot = sns.barplot(
    data=melted_data,
    x='Sample4',
    y='Value',
    hue='Measurement',
    palette='pastel'
)

# 设置 y 轴为百分比格式
def percent(x, _):
    return f'{x * 100:.2f}%'
barplot.yaxis.set_major_formatter(FuncFormatter(percent))

# 图例、字体、旋转

plt.legend(
    title='Measurement',
    fontsize=12,
    title_fontsize=13,
    loc='upper left',               # 圖例位置（相對於bbox）
    bbox_to_anchor=(1.02, 1),       # 圖例放在圖的外面（右上角）
    borderaxespad=0
)
plt.xticks(rotation=0, fontsize=14)
plt.yticks(rotation=0, fontsize=14)
plt.ylabel('mutation frequency', fontsize=14, fontweight='bold')
plt.xlabel('')

plt.ylim(0,0.002)



# 自动调整布局
plt.tight_layout()

# 设置输出文件夹路径
output_folder = ("/Users/jasontingting/Desktop/Del_INS_SNV 比例")  # 替换为您的目标文件夹路径
if not os.path.exists(output_folder):
    os.makedirs(output_folder)  # 如果目标文件夹不存在，创建它

# 保存为高分辨率 PNG 文件
save_path = os.path.join(output_folder, f"AF(0.6)_E1(Sel)_ま.png")
plt.savefig(save_path, dpi=300)

# 显示图像
plt.show()
