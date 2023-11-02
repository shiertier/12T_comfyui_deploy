import os
import argparse

def remove_symlinks(path):
    for filename in os.listdir(path):
        full_path = os.path.join(path, filename)
        if os.path.islink(full_path):
            os.remove(full_path)
        elif os.path.isdir(full_path):
            remove_symlinks(full_path)

parser = argparse.ArgumentParser(description='Remove all symbolic links in the specified directory')

parser.add_argument("-p", '--path', dest='path', required=True, help='Path to the directory where symbolic links should be removed')

args = parser.parse_args()

if os.path.isdir(args.path) and os.access(args.path, os.R_OK):
    remove_symlinks(args.path)
else:
    print("Invalid directory path or no access permission: %s" % args.path)

print("All symbolic links in the directory have been removed")