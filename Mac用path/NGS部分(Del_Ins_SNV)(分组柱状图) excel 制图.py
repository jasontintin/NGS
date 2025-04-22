import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# ✅ 1. 基本参数设定
data_path = "/Users/jasontingting/Desktop/K3 部分結果/variant_summary_supF.xlsx"
sheet_name = 'Sel'
sample_group = '1'
columns_to_plot = ['Del_mutant frequency_0.6', 'Ins_mutant frequency_0.6', 'SNV_mutant frequency_0.6']
group_col = 'Type of chemical modification'
output_folder = "/Users/jasontingting/Desktop/Del_INS_SNV 比例"
palette = sns.color_palette("Set1", n_colors=3)  # ✅ 色彩柔和适合展示
ylim = (0, 0.002)

# ✅ 2. 读取数据
df = pd.read_excel(data_path, sheet_name=sheet_name)
selected_data = df[df['group2'].astype(str).str.contains(sample_group)].copy()

# ✅ 3. 清洗百分号 & 转换数值
for col in columns_to_plot:
    selected_data[col] = (
        selected_data[col]
        .astype(str)
        .str.replace('%', '', regex=False)
        .apply(pd.to_numeric, errors='coerce')
    )

# ✅ 4. 计算均值和标准差
means = selected_data.groupby(group_col, observed=True)[columns_to_plot].mean()
stds = selected_data.groupby(group_col, observed=True)[columns_to_plot].std()

# ✅ 5. 设置显示顺序：Ctrl 放最前
ordered_groups = sorted(means.index.tolist(), key=lambda x: (0 if 'Ctrl' in x else 1, x))
x = np.arange(len(ordered_groups))
bar_width = 0.22
group_gap = 0.05

# ✅ 6. 绘图
plt.figure(figsize=(12,8))  # ⭐️ poster 建议 10x6 ~ 12x8 之间

n_bars = len(columns_to_plot)
used_labels = set()

for i, col in enumerate(columns_to_plot):
    offsets = x + (i - n_bars / 2) * bar_width + bar_width / 2
    label = 'Del' if 'Del' in col else 'Ins' if 'Ins' in col else 'SNV'
    plot_label = label if label not in used_labels else None
    used_labels.add(label)

    plt.bar(
        offsets,
        means.loc[ordered_groups, col],
        width=bar_width,
        color=palette[i],
        label=plot_label,
        yerr=[np.zeros_like(stds.loc[ordered_groups, col]), stds.loc[ordered_groups, col]],
        capsize=5,
        edgecolor='black',         # ✅ 黑边框清晰
        linewidth=1.5,             # ✅ 加粗柱边框
        error_kw=dict(
            lw=1.4,                # ✅ 误差线主线加粗
            capthick=1.4,          # ✅ 误差线端帽加粗
            ecolor='black'         # ✅ 误差线为黑色
        )
    )

# ✅ 7. 格式设定
plt.xticks(x, ordered_groups, fontsize=14, fontweight='bold')
plt.yticks(fontsize=14,fontweight='bold')
plt.ylabel("Mutation Frequency (%)", fontsize=16, fontweight='bold')
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y*100:.2f}%"))
plt.ylim(*ylim)
plt.tight_layout()
ax = plt.gca()
plt.tick_params(axis='x', width=2, length=5)
plt.tick_params(axis='y', width=2, length=5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(2.0)  # 下边框（x轴）
ax.spines['left'].set_linewidth(2.0)    # 左边框（y轴）

# ✅ 8. 保存图像
os.makedirs(output_folder, exist_ok=True)
save_path = os.path.join(output_folder, f"group{sample_group}_PosterReady.png")
plt.savefig(save_path, dpi=300)  # ✅ Poster 建议使用 dpi=600 以上
plt.show()