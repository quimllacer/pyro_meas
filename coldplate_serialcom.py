import serial

class ColdPlate_serialcom:
	def __init__(self, port):
		# Opens up a socket connection to the instrument
		try:
			self.s = serial.Serial(port, baudrate = 9600,
					timeout = 1, bytesize = 8,
					stopbits = 1, xonxoff = False)
			print('Serial connection established.')
		except:
			print('Coldplate connection could not been established.')

	def __del__(self):
		try:
			self.s.close()
			print('Destructor called, coldplate_serial deleted.')
		except:
			print('Desctructor called, coldplate_serial could not been deleted.')

	def send(self, command):
		# Send command
		try:
			command += '\r'
			command = command.encode('ascii')
			self.s.write(command)
		except:
			print('Sending data to device failed.')

	def receive(self):
		# Read data until newline character
		message = self.s.readline(1024)
		message = message.decode('ascii')
		return message

	def ask(self, command):
		# Return value from query
		try:
			command += '\r'
			command = command.encode('ascii')
			self.s.write(command)
			response = self.s.readline().decode("ascii")[:-2]
			return response
		except: 
			print('Asking device for return value failed.')
