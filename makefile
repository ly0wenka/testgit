name = helloworld
all:
	gcc $(name).c -o $(name).out
	./$(name).out