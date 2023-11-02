import os
import argparse

def replace_github_to_mirror_file(file, mirror="https://hub.yzuu.cf", origin="https://github.com"):
    if os.path.isfile(file):
        with open(file, 'r') as f:
            lines = f.readlines()

        modified = False
        new_lines = []
        for line in lines:
            new_line = line.replace(origin, mirror)
            new_lines.append(new_line)
            if new_line != line:
                modified = True

        if modified:
            # 创建备份文件
            bak_filepath = file + ".bak"
            with open(bak_filepath, 'w') as f:
                f.truncate()
                f.writelines(lines)

            with open(file, 'w') as f:
                f.writelines(new_lines)

            print(f"File '{file}' processed successfully.")
        else:
            print(f"No modification needed for file '{file}'.")
    else:
        print(f"File does not exist: {file}")

def replace_github_to_mirror_dir(directory, mirror="https://hub.yzuu.cf", origin="https://github.com"):
    if os.path.isdir(directory):
        for root, dirs, files in os.walk(directory):
            for filename in files:
                if not filename.lower().endswith(('.txt', '.py', '.json')):
                    print(f"Unsupported file: {filename}")
                    continue
                filepath = os.path.join(root, filename)
                replace_github_to_mirror_file(filepath, mirror, origin)
        print("Directory processed successfully.")
    else:
        print(f"Directory does not exist: {directory}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replace 'https://github.com' with a specified mirror.")
    parser.add_argument("-f", "--file", help="Specify a single file to process (txt/py/json)")
    parser.add_argument("-p", "--path", help="Specify a directory path to recursively process")
    parser.add_argument("-m", "--mirror", default="https://hub.yzuu.cf", help="Specify the mirror URL (default: https://hub.yzuu.cf)")
    parser.add_argument("-o", "--origin", default="https://github.com", help="Specify the original content to replace (default: https://github.com)")
    args = parser.parse_args()

    if args.file:
        replace_github_to_mirror_file(args.file, args.mirror, args.origin)
    elif args.path:
        replace_github_to_mirror_dir(args.path, args.mirror, args.origin)
    else:
        parser.print_help()
