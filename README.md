# MS Graph API authentication example with Fast API

This is to use python webapp and authenticate with MS Azure using Fast API instead of Flask.

## requirements
- install gnu `make`
- follow setup guide here for Azure [here](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-v2-python-webapp)


## Setup
For simplicity I just used a virtualenv, and changes shouldn't need to be made but may be
for caching with docker - would be easy to setup redis here though and reconfigure this to 
use redis shared cache.

### Using virtual environment:

Assuming python 3 - I used 3.7 for building and have python version 3 aliased to `python3`
Thus, if `python` is not version 3 or greater, best to use brew and install newer version and
replace `python` below with `python3`

Create Env
```bash
$ python -m venv venv
```

Activate venv
```bash
$ . venv/bin/activate
```

Install requirements
```bash
$ pip install -r requirements.txt
```

```bash 
$ make uvicorn
```

### Using docker:
`make docker`

The api runs on port 9000 - ensure you use localhost and configure your redirects properly based on the
setup guide. 