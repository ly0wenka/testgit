set docker_container_name=hello-world-java-app

docker build -t %docker_container_name% .
docker run --rm -it -p 8080:8080 %docker_container_name%
