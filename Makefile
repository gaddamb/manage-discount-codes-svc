IMAGE_NAME := manage-discount-svc
IMAGE_VERSION := 1.0

## clean: clean the build
clean:
	rm -rf ./build

## docker-build:  build the docker file
docker-build:
	docker build -t $(IMAGE_NAME):$(IMAGE_VERSION) .

## docker-run: run the docker file
docker-run:
	docker run -dp 8080:5000 $(IMAGE_NAME):$(IMAGE_VERSION)

## test: run the tests
test: clean
	pytest