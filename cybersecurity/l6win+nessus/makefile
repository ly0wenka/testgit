l6:
	Administrator 1234qqqQ
	https://tenable.com/downloads/nessus#download
	sudo dpkg -i Nessus-*.deb
postgres:
	service postgressql start
	sudo msfdb init
tcp:
	use auxiliary/scanner/portscan/tcp
	set RHOSTS 192.168.0.100
	set PORTS 20-5000
	use payload/windows/meterpreter/bind_tcp

meetthemsf7:
	search name:java | grep rmi
	help spool

enumeration:
	db_nmap -sS -sV -O -PN -p- 192.168.0.104
	hosts
	services
	vulns
enumerationsmb:
	cewl -d 5 -m 7 -w /home/kali/Desktop/pass.txt https://github.com/rapid7/metasploitable3
enummysql:
	cd /home/kali/Desktop
	wget https://github.com/danielmiessler/SecLists/blob/master/Passwords/Default-Credentials/mysql-betterdefaultpasslist.txt
script:
	nmap -sV --script=http-enum 192.168.0.104
script-ftp:
	nmap -sV --script=ftp-anon 192.168.0.104
script-smb:
	nmap -sV --script=smb-vuln* -p139,445 192.168.0.104