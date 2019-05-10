build:
	docker build -t extract_reviews .

run: build
	docker run -it --rm --env-file .env extract_reviews
