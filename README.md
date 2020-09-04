# dashboard_api
This api is made with FastAPI

## requirements
- octopus-data-gcp.json from GCP Console to access the big query and put in the project root
- install gnu `make`


## Instructions 
### Using virtual environment:
1. `python -m venv venv`
2. `. venv/bin/activate`
3. `pip install -r requirements.txt`
4. `make uvicorn`

### Using docker:
`make docker`

Now the api can be accessed at 127.0.0.1:9000