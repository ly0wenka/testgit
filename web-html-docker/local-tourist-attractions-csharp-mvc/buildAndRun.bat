set docker_container_name=local-tourist-attractions-csharp-mvc
set port=80
set port2=8080

docker build -t %docker_container_name% .
docker run --rm -it -p %port%:%port2% %docker_container_name%

