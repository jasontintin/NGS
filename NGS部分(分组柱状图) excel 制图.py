import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 讀取 Excel
df = pd.read_excel("/Users/jasontingting/Desktop/K3 部分結果//論文用 コロニー PCR （K3部分）.xlsx", sheet_name='PCR graph')

# 只選 group == 1 的資料
selected_data = df[df['group'] == 1].copy()

# 資料轉長格式
df_melted = selected_data.melt(
    id_vars=["Sample", "group"],
    value_vars=["未検出", "鎖長減少", "鎖長増加", "変化なし"],
    var_name="Type",
    value_name="Count"
)

# 畫圖
plt.figure(figsize=(12, 6))
sns.set(style="whitegrid")

ax = sns.barplot(data=df_melted, x="Sample", y="Count", hue="Type")

plt.title("Group 1 Samples", fontsize=16)
plt.xlabel("Sample")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.legend(title="Type")
plt.tight_layout()
plt.show()