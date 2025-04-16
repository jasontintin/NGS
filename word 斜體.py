from docx import Document

# 打开 Word 文档
doc = Document("/Users/jasontingting/Desktop/修士論文/正文/序論.docx")

# 指定目标文字
target_text = "supF"

# 遍历文档中的所有段落
for paragraph in doc.paragraphs:
    if target_text in paragraph.text:
        for run in paragraph.runs:
            if target_text in run.text:
                run.italic = True  # 设置斜体

# 保存更改
doc.save("/Users/jasontingting/Desktop/修士論文/正文/序論1.docx")