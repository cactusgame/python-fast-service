
# 安装

## 创建虚拟环境

- 当前框架只支持X86架构的MacOS和Linux
- 目前仅在python3.8版本测试过

安装minioconda

```
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh Miniconda3-latest-Linux-x86_64.sh
```

创建虚拟环境

```
conda create -n pfs python=3.8
source activate pfs
```


## 使用源代码安装(推荐)
- 先clone源代码
```
git clone hhttps://github.com/cactusgame/python-fast-service.git
```

- 推荐的安装方式，进入根目录，键入如下命令
  - 以后框架升级，只需要git pull代码即可，无需重新安装。
  - 只有此种安装方式，可以使用abt工具全部特性。

```
pip install -e .
```

## 离线安装

- 某些情况下，服务器无法连接到网络，可以先从能联网的机器上，下载指定tag的zip压缩包，然后通过pip离线安装

```
pip install pfs-xxxx.tar.gz
```

如果需要在dockerfile中离线安装，需要将框架的tar.gz包先copy到docker内部再执行安装，比如

```
COPY ./setup/pfs-xxxx.tar.gz ./pfs-xxxx.tar.gz
```

## 依赖

- 使用abt的file,logs命令，需要单独安装ossutil，请根据[oss文档](https://help.aliyun.com/document_detail/120075.html) 进行安装
