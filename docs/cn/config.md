# 多环境配置
配置统一放在项目根目录的config目录下。

## 配置加载优先级（从高到低）
- 从环境变量中，加载键值对覆盖配置
- 从config目录的config_xxx.py中加载指定xxx环境的配置
- 从config目录的config.py中加载配置
- 加载框架的默认配置。


### 例子  
- 使用默认的配置启动服务

```
pfs
```

- 使用test环境的配置启动服务，即使用test环境的配置继承默认配置

```
pfs test
```

- 使用daily环境的配置继承默认配置启动服务，并设置workers的数量为4

```
workers=4 pfs daily
```

- 使用local和daily的配置启动服务，local（靠左侧）的优先级更高，同时继承默认配置

```
pfs local daily
```

*请注意，`debug`是框架预留的关键字，不可以作为配置的环境名，比如config_debug.py是不会生效的*
   
### 在容器中使用配置
- 容器启动，默认使用prod环境的配置（即优先使用config_prod.py中的配置）

```
docker run your-image
```   

- 容器启动，使用指定环境（local）的配置（默认支持local,daily,prod三个环境)

```
docker run your-image local
```


   
## 读取配置项  
配置项注入了flask的config，推荐的读取方法如下：

```python
from ab import app

app.config['YOUR_CONFIG_KEY']
# or
app.config.YOUR_CONFIG_KEY
```

# 全部配置

## 配置都包含了什么
- 配置框架的插件
- [flask的配置项](http://flask.pocoo.org/docs/1.0/config/#builtin-configuration-values) 都是大写，
- [gunicorn的配置项](http://docs.gunicorn.org/en/stable/settings.html) 都是小写，
- 用户自定义的配置


## 详细配置项
config继承自flask和gunicorn并加了些ab自有的配置项。因此可以写在同一个config.py文件里。

目前支持配置项：
* APP_NAME: 算法名，用于注册到spring cloud。每个算法保证不和其他算法重复即可。
  since v2.4.2:分隔符要使用'-'，不可使用'_'。
  部署到服务器上必须改掉。必填。
* PORT: 端口号不再支持修改。在docker内，nginx固定使用80端口去访问gunicorn的8000端口
* HOST: 绑定哪个IP。一般本机测试用`localhost`，部署到服务器上用`0.0.0.0`。默认为'localhost'。
  参考：[What is the difference between 0.0.0.0, 127.0.0.1 and localhost?](https://stackoverflow.com/questions/20778771/what-is-the-difference-between-0-0-0-0-127-0-0-1-and-localhost)
* DEBUG: 是否打开flask和gunicorn的debug模式，默认为False。
  DEBUG=True实际上允许执行任意代码，部署到服务器上时禁止HOST=0.0.0.0和DEBUG=True的组合。
* LOG_LEVEL: 全局默认日志级别。底层依赖python的logging模块。
  logging的级别参见：[logging levels](https://docs.python.org/3/library/logging.html#levels)
  不填默认级别为`INFO`。

