library(ggplot2)
library(tidyr)
library(dplyr)
library(readxl)

# 假設你的資料叫 df，或你從 Excel 輸入資料
file_path <- "/Users/jasontingting/Desktop/K3 部分結果/論文用 コロニー PCR （K3部分）.xlsx"       # 替換成你的實際檔名
sheet_name <- "PCR graph"
# 讀取指定工作表
df <- read_excel(file_path, sheet = sheet_name)

# 資料轉長格式（for stacked bar）
df_long <- pivot_longer(df,
                        cols = c("未検出", "鎖長減少", "鎖長増加", "変化なし"),
                        names_to = "分類",
                        values_to = "数")

# 根據 group 分組畫圖
plot_group <- function(group_id) {
  df_filtered <- df_long %>% filter(group == group_id)

  ggplot(df_filtered, aes(x = Sample, y = 数, fill = 分類)) +
    geom_bar(stat = "identity") +
    labs(title = paste("Group", group_id),
         x = "Sample", y = "Count") +
    theme_minimal() +
    theme(axis.text.x = element_text(angle = 45, hjust = 1))
}

# 畫圖：例如 group 1
plot_group(1)
ggsave("group1_plot.png", plot_group(1), width = 8, height = 6, dpi = 300)

# 如果你想要儲存：
#ggsave("group1_stacked_bar.png", plot = plot_group(1), width = 6, height = 4)
#ggsave("group2_stacked_bar.png", plot = plot_group(2), width = 6, height = 4)
#ggsave("group3_stacked_bar.png", plot = plot_group(3), width = 8, height = 4)