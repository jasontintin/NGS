import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# 🔧 配置参数（只需根据需要修改这里）
data_path = "/Users/jasontingting/Desktop/K3 部分結果/variant_summary_supF.xlsx"
sheet_name = 'Sel'
sample_group = '3'  # group2 中包含的值，如 '1', '2', '3'
column_to_plot = 'Del_mutant frequency_0.6'# 要绘制的突变频率列
group_col = 'Type of chemical modification'
output_folder = "/Users/jasontingting/Desktop/Del_INS_SNV 比例"
palette = 'Set2'

# 🟡 读取 Excel 数据
df = pd.read_excel(data_path, sheet_name=sheet_name)

# 🎯 根据 group2 筛选样本
selected_data = df[df['group2'].astype(str).str.contains(sample_group)].copy()

# 📉 清洗数据：去掉 % 转为浮点数
selected_data[column_to_plot] = (
    selected_data[column_to_plot]
    .astype(str)
    .str.replace('%', '', regex=False)
    .apply(pd.to_numeric, errors='coerce')
)

# 📊 分组计算平均与标准差
grouped = selected_data.groupby(group_col, observed=True)[column_to_plot]
means = grouped.mean()
stds = grouped.std()

# ✅ 设置显示顺序：将包含 "Ctrl" 的放到最左边
all_labels = means.index.tolist()
labels = sorted(all_labels, key=lambda x: (0 if 'Ctrl' in x else 1, x))

# 📁 创建输出文件夹（如不存在）
os.makedirs(output_folder, exist_ok=True)

# 🎨 绘制柱状图（含上方标准差线）
plt.figure(figsize=(8, 6))
bars = plt.bar(
    x=range(len(labels)),
    height=means[labels].values,
    yerr=[np.zeros_like(stds[labels].values), stds[labels].values],
    capsize=5,
    color=sns.color_palette(palette, n_colors=len(labels)),
    edgecolor='black'
)

# 🎚 格式设置
plt.xticks(ticks=range(len(labels)), labels=labels, fontsize=14)
plt.yticks(fontsize=14)
plt.ylabel(column_to_plot, fontsize=13)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y * 100:.2f}%'))
plt.ylim(0,0.01)
plt.tight_layout()

# 💾 保存图像
save_path = os.path.join(output_folder, f"{sample_group}_{column_to_plot}_OnlySD1.png")
plt.savefig(save_path, dpi=300)
plt.show()