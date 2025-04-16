import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# 讀取 Excel
df = pd.read_excel(r"C:\Users\suzuki\PycharmProjects\NGS\K3用 excel\論文用 コロニー PCR （K3部分）.xlsx",
                   sheet_name='PCR graph')

# 將 group 統一轉換成數值，避免 int/str 混合錯誤
df['group'] = pd.to_numeric(df['group'], errors='coerce')

count_cols = ["変化なし", "未検出", "鎖長減少", "鎖長増加"]

# 設定圖片輸出資料夾
output_folder = r"C:\Users\suzuki\Desktop\TSAI\colony_PCR"
os.makedirs(output_folder, exist_ok=True)

# 每個 group 各畫一張圖
for grp in sorted(df['group'].dropna().unique()):
    selected_data = df[df['group'] == grp].copy()

    # 計算百分比
    selected_data[count_cols] = selected_data[count_cols].div(selected_data[count_cols].sum(axis=1), axis=0) * 100

    # 長格式轉換
    df_melted = selected_data.melt(
        id_vars=["Sample", "group"],
        value_vars=count_cols,
        var_name="Type",
        value_name="Percentage"
    )

    # 繪圖
    plt.figure(figsize=(10, 6))
    sns.set(style="whitegrid")
    custom_palette={
        "変化なし":"#DFF1D3",
        "未検出":"#F6C9CE",
        "鎖長減少":"#D2ECF9",
        "鎖長増加":"#FDF3B3"
    }
    ax = sns.barplot(data=df_melted, x="Sample",
                     y="Percentage",
                     hue="Type",
                     palette=custom_palette,
                     edgecolor="black",
                     linewidth=1.5)

    # 格式化 Y 軸為百分比
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.0f}%'))
    ax.set_ylim(0, 100)

    # 加上數據標籤
    for bar, (_, row) in zip(ax.patches, df_melted.iterrows()):
        height = bar.get_height()
        if height > 0:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 1,
                f'{row["Percentage"]:.1f}%',
                ha='center',
                va='bottom',
                fontsize=12,fontweight='bold',
            )

    # 標題與格式
    plt.ylabel("Percentage (%)")
    plt.xticks(rotation=0, fontsize=20, fontweight='bold')
    plt.yticks(rotation=0, fontsize=20)
    plt.tight_layout()
    ax.get_legend().remove()

    # 儲存圖片
    save_path = os.path.join(output_folder, f"Group{int(grp)}.png")
    plt.savefig(save_path, dpi=300)
    plt.show()
