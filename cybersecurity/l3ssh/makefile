l3:
	sudo apt install openssh-server
	sudo systemctl start ssh
	sudo systemctl enable ssh
	sudo apt install -y openssh-client-ssh1
	dpkg --listfiles openssh-client-ssh1 | grep bin
	ssh -V
	ip a

gssapi:
	sudo apt install -y openssh-client-gssapi

status:
	sudo systemctl status ssh