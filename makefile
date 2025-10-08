name = helloworld
all:
	gcc $(name).c -o $(name)
	./$(name).out