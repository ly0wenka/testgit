all:
	gcc l3.c -o l3.out
	./l3.out

showdemon:
	ps aux | grep mydaemon

kill1:
	kill -SIGUSR1 $(pid)
kill2:
	kill -SIGINT $(pid)
mac:
	log stream --predicate 'process == "mydaemon"'