uvicorn:
	export GOOGLE_APPLICATION_CREDENTIALS="octopus-data-gcp.json" && uvicorn app.main:app --reload --port 9000

docker:
	docker build -t api_scavenger_route . && docker run -d -v app:/app -p 9000:80 api_scavenger_route