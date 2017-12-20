import datetime, os, os.path, struct, wave
from socket import *

serv = socket(AF_INET, SOCK_STREAM)
serv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serv.bind(('', 4097))
serv.listen(5)

while True:
	sock, _ = serv.accept()
	def recv(num):
		data = ''
		while len(data) < num:
			data += sock.recv(num - len(data))
		return data
	print 'New connection'
	dest = datetime.datetime.now().isoformat()
	count = 0
	while True:
		cmd = ord(sock.recv(1))
		if cmd == 0:
			print 'New recording'
			dest = datetime.datetime.now().isoformat()
			count = 0
		elif cmd == 1:
			ns, = struct.unpack('<H', recv(2))
			print 'Samples:', ns
			samples = recv(ns * 2)
			wav.writeframes(samples)
		elif cmd == 2:
			if not os.path.exists(dest):
				os.makedirs(dest)
			fn = 'sample%04i.wav' % count
			count += 1
			wav = wave.open('%s/%s' % (dest, fn), 'wb')
			wav.setnchannels(1)
			wav.setframerate(44100)
			wav.setsampwidth(2)
		elif cmd == 3:
			wav.close()
		else:
			print 'WTF?', cmd
			break

