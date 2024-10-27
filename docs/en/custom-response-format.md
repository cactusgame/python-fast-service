# Custom Response Structure

Sometimes, you may need to customize the data structure of the response. Currently, custom JSON format responses are supported. An example is shown below:

```python
from ab import jsonify
@api()
def custom_response():
    return jsonify({"res": 1})
```
