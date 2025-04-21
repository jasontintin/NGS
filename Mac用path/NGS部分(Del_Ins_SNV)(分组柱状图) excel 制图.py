import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# 🔧 配置參數
data_path = "/Users/jasontingting/Desktop/K3 部分結果/variant_summary_supF.xlsx"
sheet_name = 'Sel'
sample_group = '1'
columns_to_plot = ['Del_mutant frequency_0.6', 'Ins_mutant frequency_0.6', 'SNV_mutant frequency_0.6']
group_col = 'Type of chemical modification'
output_folder = "/Users/jasontingting/Desktop/Del_INS_SNV 比例"
palette = sns.color_palette("dark", n_colors=3)
ylim = (0, 0.002)

# 📥 讀取並篩選資料
df = pd.read_excel(data_path, sheet_name=sheet_name)
selected_data = df[df['group2'].astype(str).str.contains(sample_group)].copy()

# 📉 清洗數據
for col in columns_to_plot:
    selected_data[col] = (
        selected_data[col]
        .astype(str)
        .str.replace('%', '', regex=False)
        .apply(pd.to_numeric, errors='coerce')
    )

# 📊 計算平均與標準差
means = selected_data.groupby(group_col, observed=True)[columns_to_plot].mean()
stds = selected_data.groupby(group_col, observed=True)[columns_to_plot].std()

# 🔠 排序：讓 Ctrl 在最左邊
ordered_groups = sorted(means.index.tolist(), key=lambda x: (0 if 'Ctrl' in x else 1, x))
x = np.arange(len(ordered_groups))
bar_width = 0.22

# 🎨 開始繪圖
plt.figure(figsize=(10, 6))

n_bars = len(columns_to_plot)
used_labels = set()

for i, col in enumerate(columns_to_plot):
    # ⭐ 修正偏移：讓整組柱子以 x 為中心
    offsets = x + (i - n_bars / 2) * bar_width + bar_width / 2
    label = 'Del' if 'Del' in col else 'Ins' if 'Ins' in col else 'SNV'

    # 避免重複 legend
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
        edgecolor='black'
    )

# 🎯 格式設定
plt.xticks(x, ordered_groups, fontsize=13)
plt.yticks(fontsize=13)
plt.ylabel("Mutation Frequency (%)", fontsize=14)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y*100:.2f}%"))
plt.ylim(*ylim)
plt.title(f"group {sample_group} - Del, Ins, SNV", fontsize=15)
plt.legend(title="Mutation Type", fontsize=12, title_fontsize=12)
plt.tight_layout()

# 💾 儲存圖像
os.makedirs(output_folder, exist_ok=True)
save_path = os.path.join(output_folder, f"group{sample_group}_Del_Ins_SNV_PositiveSD_centered.png")
plt.savefig(save_path, dpi=300)
plt.show()