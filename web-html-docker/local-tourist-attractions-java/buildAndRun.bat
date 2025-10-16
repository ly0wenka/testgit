set docker-container-name=my-java-app

docker build -t docker-container-name .
docker run --rm -it -p 8080:8080 docker-container-name
