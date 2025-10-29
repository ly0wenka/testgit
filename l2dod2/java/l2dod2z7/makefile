all:
	javac Sorter.java Runner.java
	java Runner
docker:
	docker build -t java-runner .
docker-run:
	sudo docker run -it java-runner java Runner

