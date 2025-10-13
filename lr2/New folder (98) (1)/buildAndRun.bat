set docker_container_name=dotnet-process-app

docker build -t %docker_container_name% .
docker run --rm -it %docker_container_name% "/usr/bin/ls" "/usr/bin/echo"

