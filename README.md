# wekkly-chese

An epic wekkly chese

## JSON Document Schema

```jsonc
[
    {
        "name": "The test article",
        "url_name": "test-article",
        "timestamp": 1662662375, // Unix timestamp
        "file": "test.html" // Found inside /articles
    }
]
```
## Deploying

```sh
$ git clone https://github.com/AnimateShadows/wekkly-chese
$ cd wekkly-chese
$ python3 -m venv venv
$ source ./venv/bin/activate
$ pip install -r requirements.txt
$ python3 main.py
```