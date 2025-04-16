import json

# 1. 读取导出的 JSON 文献数据
with open("/Users/jasontingting/Desktop/python 代碼庫/文獻期刊名斜體/修論文獻庫.json", "r", encoding="utf-8") as file:
    references = json.load(file)

# 2. 遍历参考文献并修改期刊名
for ref in references:
    if "container-title" in ref:  # 确保字段存在
        journal_name = ref["container-title"]
        if isinstance(journal_name, list):  # 有时期刊名是数组
            journal_name = journal_name[0]
        # 去除期刊名称的额外空格或特殊字符
journal_name = ref["container-title"]
if isinstance(journal_name, list):  # 有时期刊名是数组
    journal_name = journal_name[0]

journal_name = journal_name.strip()  # 去除多余的空格


        # 设置期刊名为斜体（HTML 格式）
ref["container-title"] = f"<i>{journal_name}</i>"

# 3. 保存修改后的数据到新文件
with open("/Users/jasontingting/Desktop/python 代碼庫/文獻期刊名斜體/修論文獻庫 1.json", "w", encoding="utf-8") as file:
    json.dump(references, file, ensure_ascii=False, indent=4)

print("参考文献已处理完成！")