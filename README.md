# MS Graph API authentication example with Fast API

## What it is & does

This is a simple python service/webapp, using [FastAPI](https://fastapi.tiangolo.com/) with server side rendering, that uses the Microsoft [MSAL](https://github.com/AzureAD/microsoft-authentication-library-for-python) library for SSO auth with Azure. 
The app handles performing the redirect and handshake for SSO, fetching the JWT(s), and allowing authorized http requests to the MS GraphAPI on behalf
the given user. 

## Why does this exist?

The quickstart guide for python and Azure SSO is based on Flask. There are some interesting caveats to using the MSAL library with FastAPI instead of Flask.
Thus I thought it useful to setup a simple & functional FastAPI app that works properly.

> Note that I think FastAPI is really awesome! This demo shows off some use of its concurrency (async/await), as well as a simple & elegant mem-cache 
> as a session mechanism. The FastAPI [cache](https://github.com/long2ice/fastapi-cache) package is easy to use, configure, and supports redis 
> (with very little code change) - so setting up a distributed, and shared cache pool has never been easier.

## requirements
- install gnu `make`
- the MSAL python package - installation is documented in the article link below.
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

Run the app 

```bash 
$ make uvicorn
```

Open your browser and point to `localhost:9000`

### Using docker:
`make docker`

The api runs on port 9000 - ensure you use localhost and configure your redirects properly based on the
setup guide. 
