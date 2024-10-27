# Installation

## Creating a Virtual Environment

- The current framework only supports MacOS and Linux on X86 architecture.
- Tested only with Python 3.8.

Install Miniconda:

```bash
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh Miniconda3-latest-Linux-x86_64.sh
```

Create a virtual environment:

```bash
conda create -n pfs python=3.8
source activate pfs
```

## Installing from Source (Recommended)

- First, clone the source code:

```bash
git clone https://github.com/cactusgame/python-fast-service.git
```

- Recommended installation: navigate to the root directory and enter the following command:
  - For future framework upgrades, simply `git pull` the latest code without reinstalling.
  - Only this installation method allows full functionality of the `abt` tool.

```bash
pip install -e .
```

## Offline Installation

- In some cases, the server may be unable to connect to the network. You can first download the zip package of a specific tag on a machine with internet access and then install it offline using `pip`.

```bash
pip install pfs-xxxx.tar.gz
```

If you need to perform an offline installation within a Dockerfile, copy the `.tar.gz` package into the Docker container before executing the installation. For example:

```dockerfile
COPY ./setup/pfs-xxxx.tar.gz ./pfs-xxxx.tar.gz
```

## Dependencies

- To use the `file` and `logs` commands in `abt`, you need to install `ossutil` separately. Follow the [OSS documentation](https://help.aliyun.com/document_detail/120075.html) for installation instructions.
