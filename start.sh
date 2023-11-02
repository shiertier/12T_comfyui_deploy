#设置COMFYUI所在父级目录
export COMFYUI_FATHER=

#设置git镜像
export GIT_MIRROR=https://hub.yzuu.cf

#设置快速pip镜像
export PIP_MIRROR=https://pypi.virtaicloud.com/repository/pypi/simple

#设置库更完整pip镜像
export PIP_MIRROR2=https://mirrors.aliyun.com/pypi/simple

#设置apt-get镜像(可不设置)
export APT_GET_MIRROR=

#设置指定python
export PYTHON=python

#设置COMFYUI启动指令
export COMFYUI_COMMAND=--gpu-only --output-directory /gemini/code/output --temp-directory /gemini/code --input-directory /gemini/code/input --force-fp16 --fp16-vae --listen

#符号链接文件夹（限linux）
#需要自己更改对应位置的文件夹代码
#一般用于挂载数据集或单模型文件夹多ui使用
export SYMBOLIC_LINK=false

#更新COMFYUI
export UPDATE_COMFYUI=false

#更新所有插件
export UPDATE_NODES=false

export COMFYUI_PATH="$COMFYUI_FATHER/ComfyUI"
export NODES_PATH="$COMFYUI_PATH/custom_nodes"
export MANAGER_PATH="$NODES_PATH/ComfyUI-Manager"

# 1.部署项目
if [ -n "$GIT_MIRROR" ]; then
  echo "配置 Git 镜像源: $GIT_MIRROR"
  rm -f ~/.gitconfig || exit 1
  git config --global url."$GIT_MIRROR".insteadOf "https://github.com" || exit 1
fi

if [ -z "$COMFYUI_FATHER" ]; then
  echo "未配置 COMFYUI_FATHER ，将会部署在 / 目录"
  cd / || exit 1
else
  if [ ! -d "$COMFYUI_FATHER" ]; then
    echo "目录 $COMFYUI_FATHER 不存在，将自动创建"
    mkdir -p "$COMFYUI_FATHER" || exit 1
  fi
  cd "$COMFYUI_FATHER" || exit 1
fi

if [ ! -d "$COMFYUI_PATH" ]; then
  git clone https://github.com/comfyanonymous/ComfyUI "$COMFYUI_PATH" || exit 1
fi

cd "$NODES_PATH" || exit 1
git clone https://github.com/ltdrdata/ComfyUI-Manager || exit 1
git clone https://github.com/AIGODLIKE/AIGODLIKE-ComfyUI-Translation || exit 1
echo "项目拷贝完成"


# 2.安装依赖
if [ -n "$PIP_MIRROR" ]; then
  echo "配置 pip 镜像源: $PIP_MIRROR"
  $PYTHON -m pip config set global.index-url "$PIP_MIRROR" || exit 1
fi

cd "$COMFYUI_PATH" || exit 1
pip install -q --no-cache-dir --upgrade pip || exit 1
pip install --no-cache-dir torch==2.0.1+cu118 onnxruntime-gpu simpleeval || exit 1
echo "如果 tb-nightly 无法找到，请配置 PIP_MIRROR2 为阿里云镜像源"
if [ -z "$PIP_MIRROR2" ] && [ -z "$PIP_MIRROR" ]; then
  pip install --no-cache-dir tb-nightly || exit 1
else
  pip install --no-cache-dir tb-nightly -i ${PIP_MIRROR2:-$PIP_MIRROR} || exit 1
fi
pip install --no-cache-dir -r requirements.txt || exit 1
echo "依赖安装完成"


# 3.增设插件
if [ -n "$GIT_MIRROR" ]; then
  python git_clone_nodes.py -m "$GIT_MIRROR" || exit 1
else
  python git_clone_nodes.py || exit 1
fi

if [ -d "$MANAGER_PATH" ]; then
  $PYTHON gitreplace.py -p $MANAGER_PATH -m $GIT_MIRROR || exit 1
fi
echo "插件增设完成"

# 4.挂载数据
if [ "$SYMBOLIC_LINK" != "false" ]; then
  $PYTHON removelink.py -p $COMFYUI_PATH || exit 1
  $PYTHON link.py -g -t $COMFYUI_PATH/models -s models || exit 1
  $PYTHON link.py -g -t $COMFYUI_PATH -s ComfyUI || exit 1
  echo "数据挂载"
fi


# 5.更新项目
if [ "$UPDATE_COMFYUI" != "false" ]; then
  $PYTHON gitbackspace.py -p $COMFYUI_PATH && echo "更新主程序..." && cd /ComfyUI && git pull origin master || exit 1
elif [ "$UPDATE_NODES" != "false" ]; then
  echo "在更新插件前，你需要更新 ComfyUI。"
  exit 1
fi

if [ "$UPDATE_COMFYUI" != "false" ] && [ "$UPDATE_NODES" != "false" ]; then
  echo "更新custom_nodes目录下的文件夹..."
  cd /ComfyUI/custom_nodes || exit 1
  for folder in */; do
    folder=${folder%/}
    echo "更新文件夹: $folder"
    cd "$folder" && git pull && cd ..
  done || exit 1
fi


# 6.启动项目
cd $COMFYUI_PATH || exit 1
$PYTHON main.py $COMFYUI_COMMAND || exit 1