set docker_container_name=my-python-app
set port=5000

docker build -t %docker_container_name% .
docker run --rm -it -p %port%:%port% %docker_container_name%

