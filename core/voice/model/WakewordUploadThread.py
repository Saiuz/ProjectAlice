import logging
import socket
from pathlib import Path
from socket import timeout
from threading import Thread


class WakewordUploadThread(Thread):

	def __init__(self, host: str, port: int, zipPath: str):
		super().__init__()
		self.setDaemon(True)

		self._logger = logging.getLogger('ProjectAlice')
		self._host = host
		self._port = port
		self._zipPath = Path(zipPath)


	def run(self):
		try:
			wakewordName = self._zipPath.stem

			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
				sock.bind((self._host, self._port))
				self._logger.info('[WakewordUploadThread] Waiting for a device to connect')
				sock.listen()

				conn, addr = sock.accept()
				self._logger.info('[WakewordUploadThread] New device connected: {}'.format(addr))

				with self._zipPath.open(mode='rb') as f:
					data = f.read(1024)
					while data:
						conn.send(data)
						data = f.read(1024)

				self._logger.info('[WakewordUploadThread] Waiting on a feedback from {}'.format(addr[0]))
				conn.settimeout(20)
				try:
					while True:
						answer = conn.recv(1024).decode()
						if not answer:
							self._logger.info('[WakewordUploadThread] The device closed the connection before confirming...')
							break

						if answer == '0':
							self._logger.info('[WakewordUploadThread] Wakeword "{}" upload to {} success'.format(wakewordName, addr[0]))
							break
						elif answer == '-1':
							self._logger.warning('[WakewordUploadThread] The device failed downloading the hotword')
							break
						elif answer == '-2':
							self._logger.warning('[WakewordUploadThread] The device failed installing the hotword')
							break
				except timeout:
					self._logger.warning('[WakewordUploadThread] The device did not confirm the operation as successfull in time. The hotword installation might have failed')
		except Exception as e:
			self._logger.info('[WakewordUploadThread] Error uploading wakeword: {}'.format(e))
