uvicorn:
	export uvicorn app.main:app --reload --port 9000

docker:
	docker build -t fast_api_boilerplate . && docker run -d -v app:/app -p 9000:80 fast_api_boilerplate