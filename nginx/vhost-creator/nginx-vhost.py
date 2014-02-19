import os, re, sys, datetime, time
import argparse

from optparse import OptionParser

"""
nginx/sites-available icerisine bir dosya olusturulacak
gerekli olan seyler 
server name
root

server name bi de /etc/hosts dosyasina eklenecek
sonra da service nginx restart
"""

servername = ''
root = ''

def nginxVhost():
	parser = argparse.ArgumentParser()
	parser.add_argument('--domain', '-d', dest='servername', required=True)
	parser.add_argument('--root', '-r', dest='root', required=True)

	args = parser.parse_args() # parametreleri args icine parse ettik
	servername = args.servername
	root = args.root

	# yazdıralım da gorelim.
	print servername
	print root

	# nginx/sites-available icerisine olusturulacak dosyanin icerigi.
	# default olarak projenin icerisindeki public_html dosyası root klasor yapiliyor, gerekiyorsa duzenleriz.
	vhostContent = """
server {
	server_name """ + servername """;
	access_log """ + root + """/access.log;
	error_log """ + root + """/error.log;
	root """ + root + """/public_html;

	location / {
		index  index.html index.htm index.php;
	}

	location ~ \.php$ {
		include /etc/nginx/fastcgi_params;
		fastcgi_pass 127.0.0.1:9000;
		fastcgi_index index.php;
		fastcgi_param SCRIPT_FILENAME """ + root + """/public_html$fastcgi_script_name;
	}
}
				"""
	vhostfile = open('/etc/nginx/sites-available/'+servername, 'w') # vhost dosyasi acmaca.
	vhostfile.write(vhostContent) # vhost dosyasına yazmaca.

	os.system('ln -s /etc/nginx/sites-available/'+servername + ' /etc/nginx/sites-enabled/'+servername) # nginx/sites-enabled altina kopyalamaca.
	
	# /etc/hosts ayarlari.
	hosts = open('/etc/hosts', 'a')
	hosts.write('127.0.0.1  '+servername)

	# nginx restart.
	os.system('service nginx restart')

if __name__ == "__main__":
   nginxVhost()