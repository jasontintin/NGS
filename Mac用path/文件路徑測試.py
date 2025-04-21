import os

# 假设你已经获取了文件的绝对路径
file_path = "/Users/jasontingting/Desktop/Visual studio code/20241216 143-185 精製 図表作製明細.xlsx"

# 检查路径是否存在
if os.path.exists(file_path):
    print(f"文件存在: {file_path}")
else:
    print(f"文件不存在: {file_path}")