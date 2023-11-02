import os
import argparse

# 解析命令行参数
parser = argparse.ArgumentParser(description="将指定目录下的内容挂载到目标目录中")
parser.add_argument("-t", "--target", required=True, help="目标目录的路径")
parser.add_argument("-s", "--source", help='源目录的路径。')
parser.add_argument("-g", "--gemini", action="store_true", help="对驱动云数据集的支持。指定后，source应为 '/gemini/data-{i}/'的尾路径。[eg: -g -s models可以从三个数据集中挂载/gemini/data-{i}/models的文件到目标目录]")

args = parser.parse_args()

sd = args.target

# 检查源文件和目标目录是否存在，以及是否有权限读取和写入
def check(src_path, dst_dir):
    if not os.path.exists(src_path):
        print(f"源文件夹{src_path}不存在")
        return False
    if not os.access(src_path, os.R_OK):
        print(f"源文件夹{src_path}没有读取权限")
        return False
    if not os.path.isdir(dst_dir):
        try:
            os.makedirs(dst_dir)
        except:
            print(f"{dst_dir}不存在且创建失败.")
            return False
    if not os.access(dst_dir, os.W_OK):
        print(f"目标文件夹{dst_dir}没有写入权限")
        return False
    return True

# 递归地遍历指定目录下的所有文件和子目录，并将其软链接到目标目录中
def symlink_models(source_dir, target_dir):
    for entry in os.listdir(source_dir):
        entry_path = os.path.join(source_dir, entry)
        target_path = os.path.join(target_dir, entry)
        if os.path.isfile(entry_path):
            if not os.path.isfile(target_path):
                if check(entry_path, target_dir):
                    os.symlink(entry_path, target_path)
        elif os.path.isdir(entry_path):
            if check(entry_path, target_path):
                os.makedirs(target_path, exist_ok=True)
                symlink_models(entry_path, target_path)

if args.gemini:
    # 收集所有数据目录
    data_in_list = []
    for i in range(1, 4):
        data_in_path = f"/gemini/data-{i}"
        if os.path.isdir(data_in_path):
            data_in_list.append(data_in_path)

    # 筛选掉 data_in_list 中的空值或无效目录
    data_in_list = [d for d in data_in_list if d]

    # 同步 Gemini 数据集目录
    for data_in_path in data_in_list:
        source_path = args.source  # 源文件夹路径为 args.source 所指定的路径
        if not source_path:
            source_path = f"{data_in_path}"  # 如果未指定 source_path，则将其设为空
        else:
            source_path = f"{data_in_path}/{source_path}"  # 将数据集目录和源文件夹路径拼接成完整的路径
        if os.path.exists(source_path):
            symlink_models(source_path, sd)
            print(f"目录 {source_path} 同步完成")
        else:
            print(f"源文件夹 {source_path} 不存在.")
else:
    if not args.source:
        raise ValueError("当不使用--gemini指令时，必须使用--source来指定源目录")
    source_path = args.source
    if os.path.exists(source_path):
        # 在目标目录中创建源目录的软链接
        symlink_models(source_path, sd)
    else:
        print(f"源文件夹 {source_path}不存在.")

print("全部任务完成")