all:
	gcc l3.c -o l3.out
	./l3.out &

showdemon:
	ps aux | grep l3.out

kill: kill1 kill2
	
kill1:
	kill -SIGUSR1 `pgrep l3.out`
kill2:
	kill -SIGINT `pgrep l3.out`
mac:
	log show --predicate 'process == "l3.out"' --info --last 1h
linux:
	sudo journalctl -t linux_daemon --since "1 hour ago"