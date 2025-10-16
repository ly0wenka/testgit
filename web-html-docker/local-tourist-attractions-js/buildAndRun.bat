set docker-container-name=my-node-app

docker build -t docker-container-name .
docker run --rm -it -p 3000:3000 docker-container-name
