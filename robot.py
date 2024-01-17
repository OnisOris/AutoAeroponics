import serial
from loguru import logger
import threading


class Robot:
    def __init__(self, port, baud=115200):
        self.ser = None
        self.is_connected = False
        self.port = port
        self.baud = baud
        self.program_console = threading.Thread(target=self.startConsole, daemon=True)
        self.monitor = threading.Thread(target=self.monitoring, daemon=True)
        self.console = True

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baud)
            self.is_connected = True
        except serial.SerialException:
            logger.error("Serial port not defined")
            self.is_connected = False
        logger.debug(self.ser.__class__)

    def disconnect(self):
        self.is_connected = False
        self.ser.close()
        self.ser = None

    def write(self, command):
        self.ser.write(command.encode())

    def startConsole(self):
        while self.console:
            inp = input("Введите команду \n")
            inp_c = inp.split()
            if inp == "exit":
                self.console = False
                self.disconnect()
                break
            elif inp_c[0] == "send":
                var = inp.split('send ')
                command = f"{var[1]}\n"
                print(command)
                self.write(command)
            else:
                print("Неправильная команда")

    def monitoring(self):
        while self.is_connected:
            logger.debug(self.ser.readline().decode())

    def start_threads(self):
        self.program_console.start()
        self.monitor.start()
        self.program_console.join()
        self.monitor.join()
