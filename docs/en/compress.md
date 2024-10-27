# HTTP Compression

## Response Compression

If your API returns long text and you want to compress the response body, the framework will automatically handle this for you.

### Implementing the API

First, implement a regular endpoint:

```python
@api()
def compress() -> int:
    return "long text"
```

The uncompressed API endpoint is:

```
/api/algorithm/compress
```

The compressed API endpoint is:

```
/api/algorithm/compress.zip
```

### Accessing the API

If you don't want to handle decompression yourself, use the Python `requests` API installed with the framework.

```python
import requests

r = requests.get('http://your-host:your-port/api/algorithm/compress.zip')
print(r.status_code)  # 200 
print(r.text)
```

The response is:

```json
{"code":0,"data":{"sample_rate":null,"sample_count":null,"result":"long text"}}
```

### How It Works

The compressed response is returned with `Content-Encoding: gzip`. Other clients can decompress it as needed.

## Request Compression

To be implemented.
