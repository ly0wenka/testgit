all:
	gcc l3.c -o l3.out
	./l3.out

showdemon:
	ps aux | grep mydaemon
	
kill:
	kill -SIGUSR1 $(cat /var/run/mydaemon.pid)
