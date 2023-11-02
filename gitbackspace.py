import os
import argparse

def apply_backup_file(file_or_path):
    directory = os.path.dirname(file_or_path)
    file_name = os.path.basename(file_or_path)

    # 检查文件是否以.bak结尾
    if not file_name.endswith(".bak"):
        print("指定路径不是备份文件")
        return

    original_file_name = file_name[:-4]  # 去除.bak后缀
    original_file_path = os.path.join(directory, original_file_name)

    # 检查同级目录是否存在与备份文件对应的原始文件
    if not os.path.exists(original_file_path):
        print(f"找不到与备份文件对应的原始文件: {original_file_path}")
        return

    backup_file_path = os.path.join(directory, file_name)

    # 复制备份文件内容到原始文件
    with open(backup_file_path, 'r') as backup_file:
        backup_content = backup_file.read()

    with open(original_file_path, 'w') as original_file:
        original_file.write(backup_content)

    print(f"成功应用备份文件: {file_or_path}")

    # 删除备份文件
    os.remove(backup_file_path)
    print(f"已删除备份文件: {backup_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="应用备份文件")
    parser.add_argument("-f", "--file", help="要处理的单个文件路径")
    parser.add_argument("-p", "--path", help="要处理的目录路径")

    args = parser.parse_args()

    if args.file:
        apply_backup_file(args.file)
    elif args.path:
        for file_name in os.listdir(args.path):
            file_path = os.path.join(args.path, file_name)
            if os.path.isfile(file_path):
                apply_backup_file(file_path)
    else:
        print("请指定--file或--path参数")
