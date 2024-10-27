[中文](README.md)   [[English]](README_en.md)

# 简介

这个项目可以快速将你的python代码，包装成生产环境可用的服务，主要包含以下功能

- 以统一的方式实现API接口，统一请求和响应的格式
- 提供监控，日志，多环境配置等实用功能
- 实现私有交付中的加密，许可证等需求
- 协助构建docker镜像

本项目最初是同事和我在阿里云工作时开发的[algorithm-base框架](https://github.com/aliyun/algorithm-base)
。由于当时需要满足商业项目需求，框架内耦合了冗余逻辑。我从阿里云离职后，fork了该项目，保留了最常用的功能，并进行了一定优化。

# 快速开始

我们用一个极简的例子，为你的`API`构建镜像并发布服务。

## 安装框架
- 当前框架只支持X86架构的MacOS和Linux
- 目前仅在python3.8版本测试过
- 详见 [安装](docs/cn/install.md)

```
pip install python-fast-service
```

## 编写hello world服务

进入`examples/simple`目录。这即是日后创建项目用的模板，也是hello-world程序。

对于`simple`项目, 你需要在`api`目录下实现你的API(相当于服务的`控制器`层)。
例子中提供了一个`demo.py`，其中实现了若干`API`。如下代码，这段被`@api`装饰器修饰的方法，将会被自动暴露为路径是`/api/add`
的RESTFUL API。详见 [服务与API](docs/cn/service.md)

```
from ab.core import api

@api()
def add(a: int, b: int) -> int:
    """
    一个简单的加法算法示例
    :param a: 第一个参数
    :param b: 第二个参数
    :return:
    """
    return a + b
```

## 启动服务并测试

在`simple`根目录下，确保8000端口没有被占用，键入如下命令启动服务

```
pfs
```

服务成功启动后,看到类似如下输出，代表启动成功

```
[2023-02-01 13:07:33 +0800] [12257] [INFO] Starting gunicorn 20.0.4
[2023-02-01 13:07:33 +0800] [12257] [DEBUG] Arbiter booted
[2023-02-01 13:07:33 +0800] [12257] [INFO] Listening at: http://0.0.0.0:8000 (12257)
[2023-02-01 13:07:33 +0800] [12257] [INFO] Using worker: sync
[2023-02-01 13:07:33 +0800] [12267] [INFO] Booting worker with pid: 12267
[2023-02-01 13:07:33] [12267] [DEBUG] algorithms: {('add', 'python'): add(a: int, b: int) -> int,
[2023-02-01 13:07:33] [12267] [DEBUG] fixtures: {}
[2023-02-01 13:07:33 +0800] [12257] [DEBUG] 2 workers
[2023-02-01 13:07:33] [12268] [DEBUG] algorithms: {('add', 'python'): add(a: int, b: int) -> int,
[2023-02-01 13:07:33] [12268] [DEBUG] fixtures: {}
```

你可以通过如下命令访问前面定义的接口

```
curl --location --request POST 'localhost:8000/api/add' \
--header 'Content-Type: application/json' \
--data-raw '{
	"args": {"a": 1, "b": 2}
}'
```

如下输出，返回了加法算法的结果

```
{"code":0,"data":3}
```

### 修改API路径

Fast Service框架默认将API统一暴露在`/api`路径下，你当然也可以增加新的路径。你需要在项目根目录的`api`文件夹下，创建一个python
module，如`endpoint.py`,
这样，就可以同构`/api/document/add`来访问该API了

```
from ab.endpoint.registry import register_endpoint

register_endpoint('/api/document/<string:api_name>')
```

### 修改响应体结构
你可以返回flask的Response对象，用来替换Fast Service的默认响应体结构。详见 [定制响应结构](docs/cn/custom-response-format.md)
```
 from flask import Response
 return Response(f"Hello, {a - b}", status=200, mimetype='text/plain')
```


## 构建镜像，发布与访问

在`simple`项目根目录下键入如下命令

```
sh build.sh
```

至此，你已经对Fast Service框架有了初步印象, 详细文档见`用户指南`。

# 用户指南

- [安装](docs/cn/install.md)
- 服务能力
    - [服务与API](docs/cn/service.md)
- 性能相关
    - [http压缩](docs/cn/compress.md)
- 运维能力
    - [多环境配置](docs/cn/config.md)
    - [健康检查](docs/cn/health_check.md)
    - [监控](docs/cn/monitoring.md)
    - [滚动日志](docs/cn/log.md)
    - [异常与错误处理](docs/cn/error.md)
    - [测试用例](docs/cn/test.md)
- 最佳实践
    - [如何创建新项目](docs/cn/new-project.md)
    - [定制响应结构](docs/cn/custom-response-format.md)
    - [常见问题](docs/cn/best-practice.md)
    - [gunicorn worker timeout问题排查](https://zhuanlan.zhihu.com/p/370330463)
    - [配置gunicorn的常见问题](https://zhuanlan.zhihu.com/p/371115835)




