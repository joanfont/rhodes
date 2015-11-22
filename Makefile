build:
	docker build -t joanfont/rhodes .

push:
	docker push joanfont/rhodes

devel:
	docker-compose run --rm --service-ports devel