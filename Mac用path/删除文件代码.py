import os
import shutil

# 设置目标主文件夹路径
main_folder = r"/Users/jasontingting/Desktop/python 代碼庫"

# 目标前缀
prefix = "未命名檔案夾"  

# 遍历主文件夹中的所有子文件夹
for folder_name in os.listdir(main_folder):
    folder_path = os.path.join(main_folder, folder_name)

    # 判断是否是目标文件夹
    if os.path.isdir(folder_path) and folder_name.startswith(prefix):
        print(f"Deleting: {folder_path}")  # 先打印确认要删除的文件夹
        shutil.rmtree(folder_path)  # 递归删除文件夹及其内容

print("Deletion complete!")