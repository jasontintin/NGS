import os
import shutil

# 指定母文件夹路径
parent_folder = "/Volumes/JASONTINGTING/202412sai"

# 指定三级文件夹名称
target_third_level = "Step_3.Variant_calling"
# 指定要删除的四级文件夹的前缀
target_prefix = "grouped"

# 遍历所有二级文件夹
if not os.path.exists(parent_folder):
    print(f"❌ 错误: 母文件夹 {parent_folder} 不存在")
else:
    for second_level_folder in os.listdir(parent_folder):
        second_level_path = os.path.join(parent_folder, second_level_folder)

        if os.path.isdir(second_level_path):
            step3_path = os.path.join(second_level_path, target_third_level)

            if os.path.isdir(step3_path):
                print(f"✅ 找到 Step_3 目录: {step3_path}")

                for folder in os.listdir(step3_path):
                    folder_path = os.path.join(step3_path, folder)

                    if os.path.isdir(folder_path) and folder.startswith(target_prefix):
                        print(f"🔴 准备删除: {folder_path}")
                        try:
                            shutil.rmtree(folder_path)
                            print(f"✅ 已删除: {folder_path}")
                        except Exception as e:
                            print(f"❌ 删除失败: {folder_path}, 错误信息: {e}")
            else:
                print(f"⚠️ 未找到 Step_3 目录: {step3_path}")
                / Users / jasontingting / Desktop / K3
                部分結果 / variant_summary