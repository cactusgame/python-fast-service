"""
"""


def test_add(client):
    req = {
        'args': {
            'a': 1,
            'b': 2,
        }
    }
    resp = client.post_data(
        '/api/algorithm/add',
        data=req,
    )
    assert resp == {
        'code': 0,
        'data': 3
    }


def test_add2(client):
    req = {
        'args': {
            'a': 1,
            'b': 2,
        }
    }
    resp = client.post_data(
        '/api/algorithm/add',
        data=req,
    )
    assert resp == {
        'code': 0,
        'data':  3
    }
