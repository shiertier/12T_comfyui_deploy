import os
import subprocess
import argparse

file_path = os.path.join(os.path.dirname(__file__), '..', 'nodes.txt')

if not os.path.exists(file_path):
    with open(file_path, 'w') as f:
        f.write('default node')

comfy_path = os.environ.get('COMFYUI_PATH')

if comfy_path:
    comfy_path = os.path.abspath(comfy_path)
    os.chdir(os.path.join(comfy_path, 'custom_nodes'))
else:
    print("comfy_path environment variable is not set.")

if os.stat(file_path).st_size == 0:
    print("nodes.txt file is empty. No extensions to install.")
    exit()

with open(file_path, 'r') as file:
    content = file.read()

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mirror", help="URL of the mirror")
args = parser.parse_args()

if args.mirror:
    content = content.replace("https://github.com", args.mirror)

print("Starting git clone operation")

lines = content.split('\n')
for line in lines:
    if line.strip().startswith("https://"):
        command = f"git clone {line}"
        try:
            subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            print(f"Failed to run {command}: {e}")

print("Git clone operations completed / No new extensions to clone.")
